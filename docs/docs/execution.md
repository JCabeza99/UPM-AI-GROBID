# Step by step guide

## Grobid

Even if you execute the script manually or through the docker-compose method you will need the grobid service running in your machine. Check the instructions to run the grobid service [here](https://grobid.readthedocs.io/en/latest/Install-Grobid/). I recommend using docker for the installation process

## Manual execution

The project has been implemented in `Python3.10.6` and therefore this script should work in newer versions of it.

```
certifi==2022.12.7
charset-normalizer==3.0.1
contourpy==1.0.7
cycler==0.11.0
fonttools==4.38.0
idna==3.4
Jinja2==3.1.2
kiwisolver==1.4.4
MarkupSafe==2.1.2
matplotlib==3.7.1
numpy==1.24.2
packaging==23.0
pdfkit==1.0.0
Pillow==9.4.0
pyparsing==3.0.9
python-dateutil==2.8.2
requests==2.28.2
six==1.16.0
urllib3==1.26.14
wordcloud==1.8.2.2
```

These are the python dependencies that the project needs in order to run the script. If you want to install them to run the script manually run the following code in the repository directory:

```bash
pip install -r requirements.txt
```
You will need to install the `wkhtmltopdf` package. You can do that in ubuntu using the following command:

```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf
```

Finally in the script you will need to change the value of the variable `grobid_url`:

```python
#original value
grobid_url = "http://grobid:8070/api/processFulltextDocument"
#new value
grobid_url = "http://localhost:8070/api/processFulltextDocument"
```

Then if you have the grobid service running you should run the following command inside the script directory:

```bash
python3 mama-papers.py 
```

## docker-compose method

This method requires to have docker and docker-compose installed in your machine and running, with the advantage that it won't be necessary to follow the installation guide for the grobid service since the docker-compose file will pull the image from the internet and build it if you don't. Then you only have to run the following command:

```bash
docker-compose up
```

This will build the images and run the script, make sure your input directory is filled with papers since the client image will retrieve the data from there.

If you want to run the script again, just type the command again and docker will run the script.

The output of the scripts will be stored in the `OUTPUT/` directory

