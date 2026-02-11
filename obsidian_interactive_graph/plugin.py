import json
import os
import re
from urllib.parse import unquote

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
        return page if page in self.nodes else None

    def add_graph_link(self, source_page_path: str, target_page_path: str):
        link = {
            "source": str(self.nodes[source_page_path]["id"]),
            "target": str(self.nodes[target_page_path]["id"])
        }
        self.data["links"].append(link)

        # rate +1 if page has link or is linked
        self.nodes[source_page_path]["symbolSize"] = self.nodes[source_page_path].get("symbolSize", 1) + 1
        self.nodes[target_page_path]["symbolSize"] = self.nodes[target_page_path].get("symbolSize", 1) + 1

    def parse_markdown_link_target(self, target: str) -> str:
        parsed_target = target.strip()
        if not parsed_target:
            return None

        # Inline markdown links may include an optional title after URL.
        # Keep URLs containing spaces, only trimming a valid trailing title token.
        title_match = re.match(r"^(?P<url>.+?)\s+(?:\"[^\"]*\"|'[^']*'|\([^\)]*\))\s*$", parsed_target)
        if title_match:
            parsed_target = title_match.group("url").strip()

        if parsed_target.startswith("<") and parsed_target.endswith(">"):
            parsed_target = parsed_target[1:-1].strip()

        parsed_target = unquote(parsed_target)
        parsed_target = parsed_target.split("#", 1)[0].split("?", 1)[0].strip()
        if not parsed_target:
            return None

        if parsed_target.startswith(("/", "\\")):
            parsed_target = parsed_target.lstrip("/\\")

        # Skip external/resource schemes and in-page anchors.
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", parsed_target):
            return None

        if parsed_target.endswith(".md"):
            parsed_target = parsed_target[:-3]

        return parsed_target or None

    def iter_target_candidates(self, target: str):
        normalized = target.strip()
        if not normalized:
            return

        if normalized.startswith(("/", "\\")):
            normalized = normalized.lstrip("/\\")

        normalized = normalized.rstrip("/")
        if not normalized:
            return

        yield normalized
        if not normalized.endswith("/index"):
            yield normalized + "/index"

    def resolve_target_page_path(self, page_path: str, target: str) -> str:
        for candidate in self.iter_target_candidates(target):
            resolved_target = (
                self.page_if_exists(candidate)
                or self.page_if_exists(self.get_path(page_path, candidate))
            )
            if resolved_target:
                return resolved_target

        for candidate in self.iter_target_candidates(target):
            resolved_target = find_best_target(self.nodes, candidate)
            if resolved_target:
                return resolved_target

        return ""

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
        MARKDOWN_LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]+\]\((?P<link_target>[^)]+)\)")
        page_path = self.get_page_path(page)

        for match in re.finditer(WIKI_PATTERN, markdown):
            wikilink = match.group('wikilink')

            # search page path of target page
            target_page_path = ""

            # link to self if wikilink is index and current page is index
            if wikilink == "index" and self.nodes[page_path]["is_index"]:
                target_page_path = page_path
            else:
                target_page_path = self.resolve_target_page_path(page_path, wikilink)

            if target_page_path == "":
                self.logger.warning(page.file.src_uri + ": no target page found for wikilink: " + wikilink)
                continue

            self.add_graph_link(page_path, target_page_path)

        for match in re.finditer(MARKDOWN_LINK_PATTERN, markdown):
            markdown_target = self.parse_markdown_link_target(match.group("link_target"))
            if markdown_target is None:
                continue

            target_page_path = self.resolve_target_page_path(page_path, markdown_target)
            if target_page_path == "":
                self.logger.warning(page.file.src_uri + ": no target page found for markdown link: " + markdown_target)
                continue

            self.add_graph_link(page_path, target_page_path)

    def create_graph_json(self, config: MkDocsConfig):
        for i, (k, v) in enumerate(self.nodes.items()):
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


def find_best_target(nodes, wikilink: str) -> str:
    abslen = None
    target_page_path = ""
    for k in nodes.keys():
        for _ in re.finditer(re.compile(r"(.*" + wikilink + r"[^/]*$)"), k):
            curlen = k.count('/')
            if abslen is None or curlen < abslen:
                target_page_path = k
                abslen = curlen
    return target_page_path
