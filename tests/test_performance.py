# Standard libraries
import textwrap
from pathlib import Path

# Third party libraries
from mkdocs.commands.build import build
from mkdocs.config import load_config
from pytest_benchmark.fixture import BenchmarkFixture


def test_build_performance(benchmark: BenchmarkFixture, tmp_path: Path) -> None:
    """
    Measure build latency for a synthetic site with dense circular linking.

    This test constructs a 100-page vault where every page links to the next,
    forcing the plugin to perform path resolution and regex parsing at scale.
    It serves as a regression test for file I/O and graph construction performance.

    Args:
        benchmark: Pytest-benchmark fixture to record execution stats.
        tmp_path: Pytest fixture providing an isolated temporary directory.
    """
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Generate 100 pages with circular dependencies (0 -> 1 ... 99 -> 0)
    for i in range(100):
        target = i + 1 if i < 99 else 0
        (docs_dir / f"page_{i}.md").write_text(
            f"# Page {i}\n\nLink to [[page_{target}]]"
        )

    config_file = tmp_path / "mkdocs.yml"
    config_content = textwrap.dedent(
        f"""
        site_name: PerfTest
        docs_dir: {docs_dir}
        site_dir: {tmp_path / "site"}
        plugins:
          - obsidian-interactive-graph
        """
    )
    config_file.write_text(config_content)

    def run_build():
        cfg = load_config(str(config_file))
        build(cfg)

    benchmark(run_build)
