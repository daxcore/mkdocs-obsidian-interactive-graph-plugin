# Interactive Graph for Material for MkDocs
Plugin for Material for MkDocs to draw an interactive graph like Obsidian.
Just available for non-mobile website yet.

# Installation
`pip install mkdocs-obsidian-interactive-graph-plugin`

# Usage
Activate the plugin in mkdocs.yml, but note that this plugin has to be located before plugins, that replace wikilinks to markdown links. Currently just wikilinks like `[[Link]]` are supported.
```
plugins:
  - obsidian-interactive-graph

extra_javascript:
  - https://fastly.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js
  - https://fastly.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js
  - assets/javascripts/graph.js
```
# Graph Javascript
The `graph.js` example can be downloaded from [here](https://raw.githubusercontent.com/daxcore/mkdocs-obsidian-interactive-graph-plugin/main/docs/YourSiteName/assets/javascripts/graph.js) and must be located into the docs directory under `docs/YourSiteName/assets/javascripts/graph.js`.

# Demo
Refer [here](https://daxcore.github.io/mkdocs-obsidian-interactive-graph-plugin/) for a demonstration of the interactive graph in Material for MkDocs.

# Development
Adapt the `.env` and `mkdocs.yml` files to your needs.
Build and start the Docker via `docker compose up --build`.

# References
* https://www.mkdocs.org/
* https://squidfunk.github.io/mkdocs-material/
* https://github.com/ndy2/mkdocs-obsidian-support-plugin/tree/main
* https://github.com/GooRoo/mkdocs-obsidian-bridge
* https://github.com/blueswen/mkdocs-glightbox
* https://echarts.apache.org
