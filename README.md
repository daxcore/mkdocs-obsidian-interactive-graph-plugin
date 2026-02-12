# Interactive Graph for Material for MkDocs
Plugin for Material for MkDocs to draw an interactive graph like Obsidian.
The graph inside the sidebar is just available for non-mobile website. The modal view via the button next to the light/dark mode switch shall work on all devices.

Refer [Github Pages](https://daxcore.github.io/mkdocs-obsidian-interactive-graph-plugin/) for a **demonstration** of the interactive graph in Material for MkDocs.

[![Build Status](https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/mkdocs-obsidian-interactive-graph-plugin)](https://pypi.org/project/mkdocs-obsidian-interactive-graph-plugin/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/mkdocs-obsidian-interactive-graph-plugin.svg)](https://pypi.org/project/mkdocs-obsidian-interactive-graph-plugin/)
[![GitHub License](https://img.shields.io/github/license/daxcore/mkdocs-obsidian-interactive-graph-plugin)](https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin/blob/main/LICENSE)

# Installation
Available on [PyPI](https://pypi.org/project/mkdocs-obsidian-interactive-graph-plugin/).
Install via `pip install mkdocs-obsidian-interactive-graph-plugin` or add it to your `requirements.txt`.

# Usage
## Setup in MkDocs
Activate the plugin in `mkdocs.yml`, but **note** that this plugin has to be located before plugins, that replace wikilinks by markdown links. Currently just wikilinks like `[[Link#Anchor|Custom Text]]` are supported.
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

## Graph Javascript by Apache ECharts
A `interactive_graph.js` example can be downloaded from [here](https://raw.githubusercontent.com/daxcore/mkdocs-obsidian-interactive-graph-plugin/main/docs/ObsidianVault/assets/javascripts/interactive_graph.js) and must be located into the docs directory under `docs/YourSiteName/assets/javascripts/interactive_graph.js`.

Beginning from version `0.3.0` the default graph inside the sidebar was minimized to edges related to the current page only. The previous behavior can be restored by setting `global` to `true` at line `draw_graph_sidebar(myChart, global=false)` at top of javascript file.

# Development
## Testing
To contribute to the project, please ensure all tests pass. We use `pytest` for unit and integration testing.

1.  **Install Dependencies:**
    Install the package in editable mode along with testing requirements:
    ```bash
    pip install -e .
    pip install pytest pytest-benchmark
    ```

2.  **Run Tests:**
    Run the full suite from the root directory:
    ```bash
    pytest
    ```

    You can also run specific categories of tests:
    ```bash
    # Run only integration tests (full build cycle)
    pytest tests/test_integration.py

    # Benchmark performance
    pytest tests/test_performance.py
    ```

# Docker
Adapt the `.env` and `mkdocs.yml` files to your needs. `DEV=ON` will rebuild the `mkdocs-obsidian-interactive-graph-plugin` from local files. If `DEV != ON` the upstream packages of PyPI will be used. Build and start the Docker container via `docker compose up --build [-d]`.

# Limitations
There is a bug in ECharts library in pinch to zoom feature (https://github.com/apache/echarts/pull/21068), but it seems like they will not fix it. Anybody can fix it by its own, by downloading the current version of the javascript library and patching via diff of the pull-request and use this in the mkdocs configuration. May another good idea could be, to not use the ECharts library... There is another project like this, that uses D3 library instead of ECharts: https://github.com/develmusa/mkdocs-network-graph-plugin including some more improvements.

# References
* https://www.mkdocs.org/
* https://squidfunk.github.io/mkdocs-material/
* https://github.com/ndy2/mkdocs-obsidian-support-plugin/tree/main
* https://github.com/GooRoo/mkdocs-obsidian-bridge
* https://github.com/blueswen/mkdocs-glightbox
* https://echarts.apache.org
* https://github.com/mkdocs/catalog
