FROM squidfunk/mkdocs-material:latest

WORKDIR /notes

COPY ./obsidian_interactive_graph /plugin/obsidian_interactive_graph

COPY ./setup.py /plugin/setup.py

COPY ./README.md /plugin/README.md

COPY ./.git/ /plugin/.git/

ARG DEV

RUN if [[ "$DEV" == "ON" ]]; then pip install /plugin/; fi

COPY ./requirements.txt /notes/requirements.txt

RUN pip install --upgrade -r requirements.txt
