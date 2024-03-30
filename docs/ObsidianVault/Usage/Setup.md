# Setup
## Setup in MkDocs

Activate the plugin in `mkdocs.yml`, but **note** that this plugin has to be located **before** plugins, that replace wikilinks by markdown links. Currently just wikilinks like `[[Link#Anchor|Custom Text]]` are supported.

```
plugins:
  - obsidian-interactive-graph

extra_javascript:
  - https://fastly.jsdelivr.net/npm/jquery/dist/jquery.min.js
  - https://fastly.jsdelivr.net/npm/echarts/dist/echarts.min.js
  - assets/javascripts/interactive_graph.js

extra_css:
  - assets/stylesheets/interactive_graph.css
```
