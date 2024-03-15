FROM squidfunk/mkdocs-material:latest

WORKDIR /notes

COPY ./requirements.txt /notes/requirements.txt

RUN pip install --upgrade -r requirements.txt
