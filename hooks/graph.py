from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
 
import os
import json
import re

from urllib.parse import urlparse, urljoin
 

pattern = re.compile(r"(?<!\!)\[\[([^\|^\]^\#]{1,})(?:.*)\]\]")

def create_graph_json(files: Files, config: MkDocsConfig):
    data = json.loads('{ "nodes": [], "links": [] }')
    nodes = {}
    reverse = {}
    site_path = config.site_name + "/"

    for file in files:
        if file.is_documentation_page():
            page = Page(title=None, file=file, config=config)
            page.read_source(config=config)
            name = page.title
            reverse[site_path + file.url + file.name] = name

    for file in files:
        if file.is_documentation_page():
            page = Page(title=None, file=file, config=config)
            page.read_source(config=config)
            name = page.title
            url = urljoin(urlparse(config.site_url).path, file.url)
            nodes[name] = {
                "url": url
            }
            nodes[name]["symbolSize"] = nodes[name].get("symbolSize", 0)

            for match in re.finditer(pattern, page.markdown):
                target = ""
                for k,v in reverse.items():
                    for x in re.finditer(re.compile(r"(.*" + match.group(match.lastindex) + r")"), k):
                        target = k
                        break
                if target == "":
                    print("SKIP")
                    continue

                link = {
                    "source": name,
                    "target": reverse[target]
                }
                data["links"].append(link)
                nodes[name]["symbolSize"] = nodes[name].get("symbolSize", 1) + 1

    for k,v in nodes.items():
        node = {
                "name": k,
                "symbolSize": v["symbolSize"],
                "value": v["url"]
        }
        data["nodes"].append(node)

    filename = os.path.join(config['site_dir'], 'assets', 'javascripts', 'graph.json')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=False, indent=2)

def on_files(files: Files, config: MkDocsConfig, **kwargs):
    create_graph_json(files, config)
