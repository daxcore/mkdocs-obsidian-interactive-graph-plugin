import json
import os
import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files as MkDocsFiles
from mkdocs.structure.pages import Page as MkDocsPage
from mkdocs.structure.nav import Navigation as MkDocsNav


class ObsidianInteractiveGraphPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.logger = get_plugin_logger(__name__)
        self.nodes = {}
        self.site_path = ""
        self.current_id = 0
        self.data = json.loads('{ "nodes": [], "links": [] }')

    @property
    def id(self):
        current_id = self.current_id
        self.current_id += 1
        return current_id

    def get_path(self, base: str, *argv: list[str]) -> str:
        from urllib.parse import urljoin
        result = base
        for path in argv:
            result = urljoin(result, path)
        return result

    def get_page_path(self, page: MkDocsPage) -> str:
        return self.get_path(self.site_path, page.file.src_uri).replace(".md", "")

    def page_if_exists(self, page: str) -> str:
        page = self.get_path(self.site_path, page)
        for k,_ in self.nodes.items():
            if k == page:
                return page
        return None

    def collect_pages(self, nav: MkDocsNav, config: MkDocsConfig):
        for page in nav.pages:
            page.read_source(config=config)
            self.nodes[self.get_page_path(page)] = {
                "id": self.id,
                "title": page.title,
                "url": page.abs_url,
                "symbolSize": 0,
                "markdown": page.markdown,
                "is_index": page.is_index
            }

    def parse_markdown(self, markdown: str, page: MkDocsPage):
        # wikilinks: [[Link#Anchor|Custom Text]], just the link is needed
        WIKI_PATTERN = re.compile(r"(?<!\!)\[\[(?P<wikilink>[^\|^\]^\#]{1,})(?:.*?)\]\]")
        for match in re.finditer(WIKI_PATTERN, markdown):
            wikilink = match.group('wikilink')

            # get the nodes key
            page_path = self.get_page_path(page)

            # search page path of target page
            target_page_path = ""

            # link to self if wikilink is index and current page is index
            if wikilink == "index" and self.nodes[page_path]["is_index"]:
                target_page_path = page_path
            else:
                # 1st: link to global page if exists
                # 2nd: search relative
                wikilink = self.page_if_exists(wikilink) or self.page_if_exists(self.get_path(page_path, wikilink)) or wikilink

                # find something that matches: shortest path depth
                abslen = None
                for k,_ in self.nodes.items():
                    for _ in re.finditer(re.compile(r"(.*" + wikilink + r")"), k):
                        curlen = k.count('/')
                        if abslen == None or curlen < abslen:
                            target_page_path = k
                            abslen = curlen

            if target_page_path == "":
                self.logger.warning(page.file.src_uri + ": no target page found for wikilink: " + wikilink)
                continue

            link = {
                "source": str(self.nodes[page_path]["id"]),
                "target": str(self.nodes[target_page_path]["id"])
            }
            self.data["links"].append(link)

            # rate +1 if page has link of is linked
            self.nodes[page_path]["symbolSize"] = self.nodes[page_path].get("symbolSize", 1) + 1
            self.nodes[target_page_path]["symbolSize"] = self.nodes[target_page_path].get("symbolSize", 1) + 1

    def create_graph_json(self, config: MkDocsConfig):
        for i, (k,v) in enumerate(self.nodes.items()):
            node = {
                    "id": str(i),
                    "name": v["title"],
                    "symbolSize": v["symbolSize"],
                    "value": v["url"]
            }
            self.data["nodes"].append(node)

        filename = os.path.join(config['site_dir'], 'assets', 'javascripts', 'graph.json')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(self.data, file, sort_keys=False, indent=2)

    def on_config(self, config: MkDocsConfig, **kwargs):
        self.site_path = config.site_name + "/"

    def on_nav(self, nav: MkDocsNav, files: MkDocsFiles, config: MkDocsConfig, **kwargs):
        self.collect_pages(nav, config)

    def on_page_markdown(self, markdown: str, page: MkDocsPage, config: MkDocsConfig, files: MkDocsFiles, **kwargs):
        self.parse_markdown(markdown, page)

    def on_env(self, env, config: MkDocsConfig, files: MkDocsFiles):
        self.create_graph_json(config)
