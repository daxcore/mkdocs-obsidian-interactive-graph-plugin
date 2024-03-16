from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
 
import os
import json
import re

from urllib.parse import urlparse, urljoin

import logging
logger = logging.getLogger(__name__)

pattern = re.compile(r"(?<!\!)\[\[([^\|^\]^\#]{1,})(?:.*)\]\]")

def page_exists(reverse, wikilink: str) -> bool:
    for k,v in reverse.items():
        if k == wikilink:
            return True
    return False

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
            nodes[name] = {
                "symbolSize": 0
            }
            reverse[urljoin(site_path, file.src_uri.replace(".md", ""))] = name

    for file in files:
        if file.is_documentation_page():
            page = Page(title=None, file=file, config=config)
            page.read_source(config=config)
            name = page.title
            nodes[name]["url"] = urljoin(urlparse(config.site_url).path, file.url)

            for match in re.finditer(pattern, page.markdown):
                target = ""
                wikilink = match.group(match.lastindex)
                # link to self
                if wikilink == "index" and page.is_index:
                    target = name
                else:
                    # link to home if exists
                    if wikilink == "index" and page_exists(reverse, urljoin(site_path, "index")):           
                        wikilink = urljoin(site_path, "index")
                    # try relative
                    elif page_exists(reverse, urljoin(urljoin(site_path, file.src_uri), wikilink)):
                        wikilink = urljoin(urljoin(site_path, file.src_uri), wikilink)

                    # find something that matches, shortest path depth
                    abslen = 9999
                    for k,v in reverse.items():
                        for _ in re.finditer(re.compile(r"(.*" + wikilink + r")"), k):
                            curlen = reverse[k].count('/')
                            if curlen < abslen:
                                target = reverse[k]
                                abslen = curlen
                            elif curlen == abslen:
                                logger.warning("WARNING - [Graph] '" + file.src_uri + "' ambiguous wikilink: [[" + wikilink + "]]")

                link = {
                    "source": name,
                    "target": target
                }
                data["links"].append(link)
                nodes[target]["symbolSize"] = nodes[target].get("symbolSize", 1) + 1

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
