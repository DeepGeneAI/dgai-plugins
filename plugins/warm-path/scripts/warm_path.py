#!/usr/bin/env python3
"""
warm_path.py - Find shortest warm introduction path to a target person.

Usage:
  python3 warm_path.py "Andy Drackley"
  python3 warm_path.py "Andy Drackley" --contacts /path/to/known-contacts.yaml

Returns the shortest path from any seed contact (Bryce, Amanda, Heidi) to the
target, with path nodes and a recommended intro framing based on
introduction_request_email.md.

Exit codes: 0 on success, 1 on missing contacts file, 2 on ambiguous name.
"""

import argparse
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
    import networkx as nx
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install networkx pyyaml")
    sys.exit(1)

DEFAULT_CONTACTS = (
    Path(__file__).resolve().parent.parent.parent.parent / "context" / "known-contacts.yaml"
)

SEED_IDS = ["bryce_daines", "amanda_thomas_wilson", "heidi_rehm"]

# Which connector triggers which intro scenario (from introduction_request_email.md)
SCENARIO_MAP = {
    "amanda_thomas_wilson": "amanda",
    "heidi_rehm": "tier1",
    "melissa_haendel": "tier1",
    "jason_saliba": "tier1",
    "alexander_milosovich": "tier1",
    "bryce_daines": "direct",
}


def _normalize(s: str) -> str:
    """Lowercase and strip accents for fuzzy comparison."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def load_graph(contacts_path: Path) -> tuple[nx.Graph, dict]:
    """Build undirected graph from YAML. Returns (graph, {id: contact_dict})."""
    with open(contacts_path) as f:
        data = yaml.safe_load(f)

    G = nx.Graph()
    nodes = {}

    for contact in data.get("contacts", []):
        nid = contact["id"]
        nodes[nid] = contact
        G.add_node(nid, **{k: v for k, v in contact.items() if k != "id"})

    for rel in data.get("relationships", []):
        G.add_edge(
            rel["from"],
            rel["to"],
            type=rel.get("type", "unknown"),
            panel=rel.get("panel", ""),
            note=rel.get("note", ""),
        )

    return G, nodes


def find_node_id(name: str, nodes: dict) -> str | None:
    """
    Case-insensitive, accent-insensitive name lookup.
    Returns a single node ID, or None if not found or ambiguous.
    Sets find_node_id.candidates on ambiguous match.
    """
    target = _normalize(name)
    find_node_id.candidates = []

    # 1. Exact full-name match (name or name_alt)
    for nid, data in nodes.items():
        if _normalize(data.get("name", "")) == target:
            return nid
        if _normalize(data.get("name_alt", "")) == target:
            return nid

    # 2. Last-name-only match (unique only)
    last_matches = []
    target_last = target.split()[-1] if target.split() else ""
    for nid, data in nodes.items():
        for name_field in ("name", "name_alt"):
            parts = _normalize(data.get(name_field, "")).split()
            if parts and parts[-1] == target_last and nid not in last_matches:
                last_matches.append(nid)
    if len(last_matches) == 1:
        return last_matches[0]

    # 3. Substring match (unique only)
    sub_matches = []
    for nid, data in nodes.items():
        if target in _normalize(data.get("name", "")):
            sub_matches.append(nid)
    if len(sub_matches) == 1:
        return sub_matches[0]
    if len(sub_matches) > 1:
        find_node_id.candidates = sub_matches
        return None

    return None


find_node_id.candidates = []  # populated on ambiguous match


def find_shortest_path(
    G: nx.Graph, target_id: str, seeds: list[str]
) -> tuple[list[str], str] | None:
    """
    Shortest path from any seed to target.
    Returns (path_node_ids, seed_id_used), or None if no path.
    When target IS a seed, returns ([target_id], target_id).
    """
    if target_id in seeds:
        return [target_id], target_id

    best: list[str] | None = None
    best_seed = None

    for seed in seeds:
        if seed not in G or target_id not in G:
            continue
        try:
            p = nx.shortest_path(G, seed, target_id)
            if best is None or len(p) < len(best):
                best = p
                best_seed = seed
        except nx.NetworkXNoPath:
            continue

    if best is None:
        return None
    return best, best_seed


def _edge_label(G: nx.Graph, a: str, b: str, nodes: dict) -> str:
    """One-line description of the edge between a and b."""
    data = G.get_edge_data(a, b, {})
    etype = data.get("type", "unknown")
    panel = data.get("panel", "")
    note = data.get("note", "")

    if etype == "direct":
        return f"direct relationship" + (f" ({note})" if note else "")
    if etype == "co_panel":
        return f"co-panel: {panel}" if panel else "co-panel (shared VCEP)"
    if etype == "co_author":
        return f"co-author" + (f" — {note}" if note else "")
    return note or etype


def _intro_framing(path: list[str], nodes: dict, G: nx.Graph) -> str:
    """
    Return recommended intro scenario text.
    Based on introduction_request_email.md scenarios 1–3.
    """
    target_id = path[-1]
    target_name = nodes[target_id]["name"]

    if len(path) == 1:
        return f"{target_name} is a seed contact — reach out directly."

    if len(path) == 2:
        start_id = path[0]
        start_name = nodes[start_id]["name"]
        if start_id == "bryce_daines":
            return (
                f"Direct outreach — Bryce reaches out to {target_name} directly.\n"
                f"  Use the outreach-email skill to draft."
            )
        # Seed is Amanda or Heidi: ask them for the intro
        scenario = SCENARIO_MAP.get(start_id, "other")
        edge_data = G.get_edge_data(start_id, target_id, {})
        edge_type = edge_data.get("type", "unknown")
        panel = edge_data.get("panel", "")
        connection_note = ""
        if edge_type == "co_panel" and panel:
            connection_note = f" {start_name} and {target_name} are both on the {panel}."

        if scenario == "amanda":
            return (
                f"Scenario 1 — Ask Amanda Thomas-Wilson for a warm intro to {target_name}.{connection_note}\n"
                f"  See introduction_request_email.md § Scenario 1 for the full template."
            )
        if scenario == "tier1":
            first = start_name.split()[0]
            return (
                f"Scenario 2 — Ask {start_name} for a warm intro to {target_name}.{connection_note}\n"
                f"  Suggested ask: \"Hi {first}, would you be open to a quick intro? "
                f"I've written a forwardable blurb.\"\n"
                f"  See introduction_request_email.md § Scenario 2 for the full template."
            )
        return (
            f"Ask {start_name} for a warm intro to {target_name}.{connection_note}\n"
            f"  Provide a forwardable blurb they can adapt."
        )

    connector_id = path[-2]
    connector_name = nodes[connector_id]["name"]
    connector_first = connector_name.split()[0]
    edge_data = G.get_edge_data(connector_id, target_id, {})
    edge_type = edge_data.get("type", "unknown")
    panel = edge_data.get("panel", "")

    connection_note = ""
    if edge_type == "co_panel" and panel:
        connection_note = f" You're both on the {panel}."
    elif edge_type == "co_author":
        connection_note = f" You've co-authored work together."

    scenario = SCENARIO_MAP.get(connector_id, "other")

    if scenario == "amanda":
        return (
            f"Scenario 1 — Ask Amanda Thomas-Wilson for a warm intro to {target_name}.\n"
            f"  Suggested ask: \"Amanda, hoping to connect with {target_name}.{connection_note} "
            f"Would you be comfortable making an intro? I've written a blurb below you can forward as-is.\"\n"
            f"  See introduction_request_email.md § Scenario 1 for the full template."
        )

    if scenario == "tier1":
        return (
            f"Scenario 2 — Ask {connector_name} for a warm intro to {target_name}.\n"
            f"  Suggested ask: \"Hi {connector_first}, I'd love to connect with {target_name}.{connection_note} "
            f"If you know them well enough, would you be open to a quick intro? I've written a forwardable blurb.\"\n"
            f"  See introduction_request_email.md § Scenario 2 for the full template."
        )

    return (
        f"Ask {connector_name} for a warm intro to {target_name}.{connection_note}\n"
        f"  Provide a forwardable blurb they can adapt."
    )


def render_result(path: list[str], nodes: dict, G: nx.Graph) -> str:
    lines = []
    target_name = nodes[path[-1]]["name"]

    if len(path) == 1:
        lines.append(f"SEED  {target_name}")
        lines.append(f"  {nodes[path[0]].get('role','')}, {nodes[path[0]].get('org','')}")
        lines.append("")
        lines.append(_intro_framing(path, nodes, G))
        return "\n".join(lines)

    hops = len(path) - 1
    lines.append(f"WARM  {target_name}  ({hops} hop{'s' if hops != 1 else ''})")
    lines.append("")
    lines.append("Path:")
    for i, nid in enumerate(path):
        name = nodes[nid]["name"]
        tag = " [seed]" if nid in SEED_IDS else ""
        lines.append(f"  {i}. {name}{tag}")
        if i < len(path) - 1:
            label = _edge_label(G, nid, path[i + 1], nodes)
            lines.append(f"     └─ {label}")

    lines.append("")
    lines.append("Recommended approach:")
    lines.append(f"  {_intro_framing(path, nodes, G)}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find shortest warm intro path to a target person."
    )
    parser.add_argument("target", nargs="+", help="Target person name")
    parser.add_argument(
        "--contacts",
        type=Path,
        default=DEFAULT_CONTACTS,
        help="Path to known-contacts.yaml (default: context/known-contacts.yaml in repo root)",
    )
    args = parser.parse_args()

    target_name = " ".join(args.target)

    if not args.contacts.exists():
        print(f"ERROR: contacts file not found: {args.contacts}")
        sys.exit(1)

    G, nodes = load_graph(args.contacts)
    target_id = find_node_id(target_name, nodes)

    if target_id is None:
        candidates = find_node_id.candidates
        if candidates:
            print(f"Ambiguous — '{target_name}' matches multiple people:")
            for cid in candidates:
                print(f"  {nodes[cid]['name']} ({nodes[cid].get('org','')})")
            sys.exit(2)
        print(f"COLD  '{target_name}' — not found in known-contacts.yaml.")
        print("No warm path available.")
        print("Consider direct cold outreach using the Ferriss pattern (outreach-email skill).")
        return

    result = find_shortest_path(G, target_id, SEED_IDS)

    if result is None:
        name = nodes[target_id]["name"]
        print(f"COLD  {name} — in graph but not reachable from any seed contact.")
        print("Consider direct cold outreach using the Ferriss pattern (outreach-email skill).")
        return

    path, _ = result
    print(render_result(path, nodes, G))


if __name__ == "__main__":
    main()
