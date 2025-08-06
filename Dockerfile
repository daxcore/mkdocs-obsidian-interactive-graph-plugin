# Use a slim Python 3.13 image as the base
FROM python:3.13-slim

# The DEV build argument controls the installation source.
# Set to 'ON' for local development. Any other value installs from PyPI.
ARG DEV=ON

# Install uv, the Python package installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set the working directory
WORKDIR /notes

# If building for local development (DEV=ON), install git, which is required
# by hatch-vcs to determine the package version from git history.
RUN if [ "$DEV" = "ON" ]; then \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*; \
  fi

# Copy the entire project context. This is necessary for a local build.
COPY . /plugin

# Install the plugin and its documentation dependencies using uv.
# - If DEV=ON, it installs from the local /plugin directory.
# - Otherwise, it installs the latest version from the PyPI registry.
RUN \
  if [ "$DEV" = "ON" ]; then \
    echo "DEV mode enabled: Installing plugin from local source..."; \
    uv pip install --no-cache "/plugin[docs]"; \
  else \
    echo "Production mode: Installing plugin from PyPI..."; \
    uv pip install --no-cache "mkdocs-obsidian-interactive-graph-plugin[docs]"; \
  fi
