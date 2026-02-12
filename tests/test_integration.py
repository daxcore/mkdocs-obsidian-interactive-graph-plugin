# Standard libraries
import json
import textwrap
from pathlib import Path
from typing import Any, Dict

# Third party libraries
import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config


def validate_graph_match(
    generated_data: Dict[str, Any], reference_data: Dict[str, Any]
):
    """
    Compare the generated graph artifact against a strict reference dataset.

    This helper asserts that:
    1. Node counts match.
    2. Node properties (Symbol Size, URL value) match exactly.
    3. The topology (Links) matches, using node Names for stability instead of internal IDs.

    Args:
        generated_data: The actual content parsed from graph.json.
        reference_data: Reference dict using node names for link definitions.
    """
    gen_nodes, ref_nodes = (
        generated_data.get("nodes", []),
        reference_data.get("nodes", []),
    )
    gen_links, ref_links = (
        generated_data.get("links", []),
        reference_data.get("links", []),
    )

    assert len(gen_nodes) == len(ref_nodes), (
        f"Mismatch in # of nodes. Expected {len(ref_nodes)}, got {len(gen_nodes)}"
    )
    assert len(gen_links) == len(ref_links), (
        f"Mismatch in # of links. Expected {len(ref_links)}, got {len(gen_links)}"
    )

    # Create Lookup Map for generated data to ease validation
    gen_name_to_node = {n["name"]: n for n in gen_nodes}

    # Validate Node Properties
    for ref_node in ref_nodes:
        name = ref_node["name"]
        assert name in gen_name_to_node, f"Missing expected node: {name}"

        gen_node = gen_name_to_node[name]

        assert gen_node["symbolSize"] == ref_node["symbolSize"], (
            f"Node '{name}' symbolSize mismatch. "
            f"Expected {ref_node['symbolSize']}, got {gen_node['symbolSize']}"
        )

        assert gen_node["value"] == ref_node["value"], (
            f"Node '{name}' value (URL) mismatch. "
            f"Expected {ref_node['value']}, got {gen_node['value']}"
        )

    # Validate Topology
    # We map the generated ID-based links to a set of tuples for O(1) lookups.
    actual_connections = set()
    for link in gen_links:
        actual_connections.add((link["source"], link["target"]))

    for ref_link in ref_links:
        ref_src_name = ref_link["source"]
        ref_tgt_name = ref_link["target"]

        # Ensure reference names exist in the generated map before proceeding
        if ref_src_name not in gen_name_to_node or ref_tgt_name not in gen_name_to_node:
            pytest.fail(
                f"Reference link uses unknown nodes: {ref_src_name} -> {ref_tgt_name}"
            )

        src_id = gen_name_to_node[ref_src_name]["id"]
        tgt_id = gen_name_to_node[ref_tgt_name]["id"]

        if (src_id, tgt_id) not in actual_connections:
            pytest.fail(f"Missing expected link: {ref_src_name} -> {ref_tgt_name}")


def test_build_reproduces_demo_topology(tmp_path: Path):
    """
    Build the full demo site and assert the output matches our reference topology.

    This ensures the plugin correctly calculates symbol sizes (based on connection density),
    resolves internal wikilinks, and generates the valid JSON structure expected by the frontend.
    """
    # 1. Scaffold the demo file structure
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "Usage").mkdir()

    (docs_dir / "index.md").write_text(
        textwrap.dedent("""
        # Welcome
        - [[Concept]]
        - [[Docker]]
        - [[Installation]]
        - [[References]]
        - [[Usage/ECharts]]
        - [[Setup]]
        """)
    )
    (docs_dir / "Concept.md").write_text("# Concept\nSee [[Usage/ECharts]]")
    (docs_dir / "Docker.md").write_text("# Docker")
    (docs_dir / "Installation.md").write_text("# Installation")
    (docs_dir / "References.md").write_text("# References")
    (docs_dir / "Usage/ECharts.md").write_text("# ECharts")
    (docs_dir / "Usage/Setup.md").write_text("# Setup")

    # 2. Configure MkDocs
    # Note: We enforce a specific site_url to make 'value' properties deterministic.
    config_file = tmp_path / "mkdocs.yml"
    config_content = textwrap.dedent(
        f"""
        site_name: Interactive Graph Demo
        site_url: https://example.com/
        docs_dir: {docs_dir}
        site_dir: {tmp_path / "site"}
        plugins:
          - obsidian-interactive-graph
        """
    )
    config_file.write_text(config_content)

    # 3. Execution
    cfg = load_config(str(config_file))
    build(cfg)

    # 4. Verification
    json_path = tmp_path / "site/assets/javascripts/graph.json"
    assert json_path.exists()

    with open(json_path) as f:
        actual_graph = json.load(f)

    # Reference data mirroring the expected "Interactive Graph Demo" structure.
    # Symbol Size = Sum of Incoming + Outgoing links.
    reference_graph = {
        "nodes": [
            {"name": "Welcome", "symbolSize": 6, "value": "/"},
            {"name": "Concept", "symbolSize": 2, "value": "/Concept/"},
            {"name": "Docker", "symbolSize": 1, "value": "/Docker/"},
            {"name": "Installation", "symbolSize": 1, "value": "/Installation/"},
            {"name": "References", "symbolSize": 1, "value": "/References/"},
            {"name": "ECharts", "symbolSize": 2, "value": "/Usage/ECharts/"},
            {"name": "Setup", "symbolSize": 1, "value": "/Usage/Setup/"},
        ],
        "links": [
            {"source": "Welcome", "target": "Concept"},
            {"source": "Welcome", "target": "Docker"},
            {"source": "Welcome", "target": "Installation"},
            {"source": "Welcome", "target": "References"},
            {"source": "Welcome", "target": "ECharts"},
            {"source": "Welcome", "target": "Setup"},
            {"source": "Concept", "target": "ECharts"},
        ],
    }

    validate_graph_match(generated_data=actual_graph, reference_data=reference_graph)
