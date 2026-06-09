---
description: Find the shortest warm introduction path from a seed contact to a target person in the ClinGen/VCEP network. Returns path nodes and recommended intro framing.
argument-hint: "[name]"
---

Run the warm path finder:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/warm_path.py" "$ARGUMENTS"
```

Return the full output verbatim.

If the command fails with an import error, tell the user to install dependencies first:
```
pip install networkx pyyaml
```

If `$ARGUMENTS` is empty, explain: "Usage: /warm-path [name] — e.g. /warm-path Andy Drackley"
