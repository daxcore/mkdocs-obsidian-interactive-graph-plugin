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
```

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
