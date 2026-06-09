"""
Five test cases for warm_path.py against the seeded known-contacts.yaml.

Test targets chosen to cover all result shapes:
  1. heidi_rehm      — seed contact (0-hop, SEED verdict)
  2. marni_falk      — 1-hop direct from Bryce
  3. andy_drackley   — 2-hop via Pamela Robertson (co-panel FBN1)
  4. christina_hung  — 2-hop via Marni Falk (metabolic disease co-panel)
  5. not_in_graph    — name absent from YAML (COLD verdict)
"""

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from warm_path import find_node_id, find_shortest_path, load_graph, SEED_IDS

CONTACTS = Path(__file__).resolve().parent.parent.parent.parent / "context" / "known-contacts.yaml"


@pytest.fixture(scope="module")
def graph():
    assert CONTACTS.exists(), f"contacts file missing: {CONTACTS}"
    G, nodes = load_graph(CONTACTS)
    return G, nodes


class TestSeedContact:
    """Heidi Rehm is a seed — path should be [heidi_rehm], length 1."""

    def test_found(self, graph):
        G, nodes = graph
        nid = find_node_id("Heidi Rehm", nodes)
        assert nid == "heidi_rehm"

    def test_is_seed(self, graph):
        G, nodes = graph
        assert "heidi_rehm" in SEED_IDS

    def test_path_is_seed(self, graph):
        G, nodes = graph
        result = find_shortest_path(G, "heidi_rehm", SEED_IDS)
        assert result is not None
        path, _ = result
        assert path == ["heidi_rehm"]
        assert len(path) == 1


class TestDirectContact:
    """Marni Falk is a 1-hop direct contact from Bryce."""

    def test_found(self, graph):
        G, nodes = graph
        nid = find_node_id("Marni Falk", nodes)
        assert nid == "marni_falk"

    def test_path_length(self, graph):
        G, nodes = graph
        result = find_shortest_path(G, "marni_falk", SEED_IDS)
        assert result is not None
        path, seed = result
        assert len(path) == 2, f"expected 1-hop path, got {path}"
        assert path[0] == "bryce_daines"
        assert path[-1] == "marni_falk"

    def test_edge_is_direct(self, graph):
        G, nodes = graph
        edge = G.get_edge_data("bryce_daines", "marni_falk")
        assert edge is not None
        assert edge["type"] == "direct"


class TestTwoHopViaCoPanel:
    """Andy Drackley is 2 hops away: Bryce → Pamela Robertson → Andy (FBN1 co-panel)."""

    def test_found(self, graph):
        G, nodes = graph
        nid = find_node_id("Andy Drackley", nodes)
        assert nid == "andy_drackley"

    def test_path_length(self, graph):
        G, nodes = graph
        result = find_shortest_path(G, "andy_drackley", SEED_IDS)
        assert result is not None
        path, _ = result
        assert len(path) == 3, f"expected 2-hop path, got {path}"

    def test_path_via_pamela(self, graph):
        G, nodes = graph
        result = find_shortest_path(G, "andy_drackley", SEED_IDS)
        path, _ = result
        assert "pamela_robertson" in path
        assert path[-1] == "andy_drackley"

    def test_connector_edge_type(self, graph):
        G, nodes = graph
        edge = G.get_edge_data("pamela_robertson", "andy_drackley")
        assert edge is not None
        assert edge["type"] == "co_panel"
        assert "FBN1" in edge.get("panel", "")


class TestTwoHopViaMetabolic:
    """Christina Hung is 2 hops: Bryce → Marni Falk → Christina (metabolic co-panel)."""

    def test_found(self, graph):
        G, nodes = graph
        nid = find_node_id("Christina Hung", nodes)
        assert nid == "christina_hung"

    def test_path_length(self, graph):
        G, nodes = graph
        result = find_shortest_path(G, "christina_hung", SEED_IDS)
        assert result is not None
        path, _ = result
        assert len(path) == 3, f"expected 2-hop path, got {path}"
        assert path[0] in SEED_IDS
        assert path[-1] == "christina_hung"

    def test_path_via_marni(self, graph):
        G, nodes = graph
        result = find_shortest_path(G, "christina_hung", SEED_IDS)
        path, _ = result
        assert "marni_falk" in path


class TestColdTarget:
    """Name not in the YAML — should return None from find_node_id."""

    def test_not_found(self, graph):
        G, nodes = graph
        nid = find_node_id("Dr. NotInGraph Person", nodes)
        assert nid is None

    def test_no_path_when_absent(self, graph):
        G, nodes = graph
        # Confirm graph has no node for this fictional person
        assert "dr_notingraph_person" not in G
        # find_shortest_path on a non-existent node returns None
        result = find_shortest_path(G, "dr_notingraph_person", SEED_IDS)
        assert result is None
