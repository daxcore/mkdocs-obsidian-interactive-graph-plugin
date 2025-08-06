# Docker

The Docker setup provides two modes for running the environment, controlled by the `DEV` flag in the `.env` file.

## Development Mode

When `DEV=ON` is set in your `.env` file, the Docker container installs the plugin from your local source code. This is ideal for development, as it allows you to test your changes in a containerized environment.

## Production Mode

If `DEV` is set to any other value (or is not set), the container will install the latest version of the plugin from PyPI. This simulates a production environment.

## Usage

1.  Configure your environment by adapting the `.env` and `mkdocs.yml` files.
2.  Use Docker Compose to build and run the container:

```bash
docker compose up --build -d
```

