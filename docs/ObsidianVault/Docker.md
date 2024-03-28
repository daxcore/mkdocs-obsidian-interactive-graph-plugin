# Docker
## Development

Adapt the `.env` and `mkdocs.yml` files to your needs. `DEV=ON` will rebuild the `mkdocs-obsidian-interactive-graph-plugin` from local files.

## Productive

If `DEV != ON` is set in `mkdocs.yml` the upstream packages of #PyPI will be used.

## Start

Build and start the Docker container via `docker compose up --build [-d]`.
