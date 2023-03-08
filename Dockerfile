FROM python:3.10-buster

COPY . /UPM-AI-GROBID/

WORKDIR /UPM-AI-GROBID/

RUN apt-get update

RUN apt-get install -y wkhtmltopdf

RUN pip install -r requirements.txt

VOLUME /UPM-AI-GROBID/INPUT/

ENTRYPOINT [ "python", "upm_ai_grobid/mama-papers.py" ]