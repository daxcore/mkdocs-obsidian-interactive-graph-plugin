FROM squidfunk/mkdocs-material:latest

WORKDIR /notes

COPY ./obsidian_interactive_graph /plugin/obsidian_interactive_graph

COPY ./setup.py /plugin/setup.py

COPY ./README.md /plugin/README.md

RUN pip install /plugin/

COPY ./requirements.txt /notes/requirements.txt

RUN pip install --upgrade -r requirements.txt
