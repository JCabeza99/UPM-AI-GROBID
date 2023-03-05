import os
import glob
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def processFile(pdf_file):
    with open(pdf_file, "rb") as data:
        response = requests.post(grobid_url, files={'input': data})
        return response


def getAbstract(root):
    for elemento in root.iter():
        if (elemento.tag == "{http://www.tei-c.org/ns/1.0}abstract"):
            result = elemento.find("{http://www.tei-c.org/ns/1.0}p")
            return result.text


# Set grobid URL
grobid_url = "http://localhost:8070/api/processFulltextDocument"

# Search for any PDF file in the input folder
input_path = "INPUT/"

# Get all the PDF files inside the input folder
pdf_files = glob.glob(os.path.join(input_path, "*.pdf"))


for pdf_file in pdf_files:
    response = processFile(pdf_file)
    root = ET.fromstring(response.content)
    abstract = getAbstract(root)
    wordcloud = WordCloud().generate(abstract)
    
