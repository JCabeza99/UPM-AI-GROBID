import os
import glob
import requests
import pdfkit
import jinja2
import time
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime

# Set grobid URL
GROBID_URL = "http://grobid:8070/api/processFulltextDocument"


def processFile(pdf_file):
    try:
        with open(pdf_file, "rb") as data:
            response = requests.post(GROBID_URL, files={'input': data})
            counter = 1
            while (response.status_code != 200):
                time.sleep(5)
                response = requests.post(GROBID_URL, files={'input': data})
                counter += 1
                if(counter == 10):
                    raise Exception("Server is not responding, check if the service is up and running")
            return response
    #Catch            
    except requests.exceptions.RequestException as e:
        print(f"{GROBID_URL}: is not reachable \nErr: {e}")
        exit(-1)
        


def getAbstract(root: ET.Element):
    for element in root.iter():
        if (element.tag == "{http://www.tei-c.org/ns/1.0}abstract"):
            for abstractElem in element.iter():
                if (abstractElem.tag == '{http://www.tei-c.org/ns/1.0}p'):
                    return abstractElem.text
    return ""

def getFigures(root: ET.Element):
    result = 0
    for element in root.iter():
        if(element.tag == "{http://www.tei-c.org/ns/1.0}figure"):
            result += 1
    return result

def getLinks(root: ET.Element):
    links = []
    for element in root.iter():
        if(element.tag == "{http://www.tei-c.org/ns/1.0}ptr"):
            links.append(element.attrib["target"])
    return  '<br>- '.join(links)

def main():
    time.sleep(2)

    # Search for any PDF file in the input folder
    input_path = "INPUT/"

    # Get all the PDF files inside the input folder
    pdf_files = glob.glob(os.path.join(input_path, "*.pdf"))

    # Check if there are files inside the folder 
    if(len(pdf_files) == 0):
        print("There are no files inside the input folder.")
        exit(-1)


    # Hold the number of figures per article
    figures = []
    paper = 1
    x_axis = []

    # stopwords for the wordcloud generation
    stopwords = STOPWORDS
    stopwords.add('et')
    stopwords.add('al')

    # load templates
    template_loader = jinja2.FileSystemLoader('./Template')
    template_env = jinja2.Environment(loader=template_loader)
    report_template = template_env.get_template('report.html')
    histogram_template = template_env.get_template('histogram.html')
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    output = ""

    # get date and time of fenerated time
    now = datetime.now()


    for pdf_file in pdf_files:
        x_axis.append(f"paper_{paper}")
        paper += 1
        response = processFile(pdf_file)
        root = ET.fromstring(response.content)
        abstract = getAbstract(root)
        
        generated_wordcloud = WordCloud(width= 700, height= 400,stopwords=stopwords, background_color='white', min_font_size=10).generate(abstract)
        
        figures.append(getFigures(root))
        
        
        obtainedLinks = getLinks(root)
        
        if(obtainedLinks == ""):
            obtainedLinks = "No link were found in this paper<br>"
        else :
            obtainedLinks = "- " + obtainedLinks
        
        wordcloud_image_name =  f"paper_{paper}.png"
        generated_wordcloud.to_image().save(wordcloud_image_name)

        
        content= {'title' : os.path.basename(pdf_file).split(".")[0], 'image': f"./{wordcloud_image_name}", 'links': obtainedLinks}
        
        output += "\n" + report_template.render(content)
        
    # Create the histogram plot
    plt.bar(x_axis, figures)
    plt.title('Graph of the figures found in each paper')

    figure_name = "figure.png"
    plt.savefig(figure_name)

    histogram_content = {'image' : f"./{figure_name}"}

    output += histogram_template.render(histogram_content)

    with open("output.html", "w") as html:
        html.write(output)
        
    pdfkit.from_file("output.html", f"./OUTPUT/report-{now}.pdf", configuration= config, options={"enable-local-file-access": ""})

    os.remove("output.html")

    image_files = glob.glob(os.path.join("./", "*.png"))

    for image in image_files:
        os.remove(image)

if __name__ == '__main__':
    main()

    
    

