from obsidian_interactive_graph.plugin import find_best_target


def test_find_best_target_normal():
    nodes = {
        "Example page/docs/optional/Test": {},
        "Example page/docs/Test": {},
        "Example page/docs/Example": {},
        "Example page/index": {}
    }
    best_target = find_best_target(nodes, "Test")
    assert best_target == "Example page/docs/Test"

    best_target = find_best_target(nodes, "Example")
    assert best_target == "Example page/docs/Example"

    best_target = find_best_target(nodes, "index")
    assert best_target == "Example page/index"

    best_target = find_best_target(nodes, "index")
    assert best_target == "Example page/index"
