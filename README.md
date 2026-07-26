# Neo0 MCP

### 🚀 [Try the live demo](https://neo0ai.github.io/neo0-mcp/) · 📄 [Read the whitepaper](WHITEPAPER.md)
<img width="1342" height="1141" alt="neo0mcp" src="https://github.com/user-attachments/assets/11e7ee2e-d4ca-4f4b-abbf-bbd0c0044530" />

Coordinate-based semantic addressing for AI agents, exposed over the **Model Context Protocol (MCP)**.

Neo0 assigns every concept an **immutable coordinate address** in a recursively partitioned semantic space. Concepts that are close in meaning share a coordinate prefix, so the address itself encodes meaning, location, and routing — no separate ontology graph required.

This repository is the **open MCP shell**. It exposes Neo0's tools to any MCP client (Claude and others) and forwards each call to the Neo0 engine API. The engine itself — coordinate derivation, the immutable registry, persona control — runs as a hosted service and is **not** included here.

## Architecture

```
MCP client (Claude)  ─▶  neo0-mcp (this repo, :8000)  ──HTTP──▶  Neo0 engine API (hosted)
```

The shell holds no engine logic, model weights, or data. It only formats requests and responses; all computation happens behind the engine API. Forking this repository gives you the interface, not the engine.

## Tools

| Tool | Description |
|---|---|
| `neo0_info` | Engine overview and load status |
| `derive_address` | Immutable coordinate address + prefix region for a concept |
| `search` | k nearest concepts, each with its address |
| `semantic_region` | Members of a prefix region |
| `verify_address` | Tamper check by re-deriving from the minting-time basis |
| `prefix_proximity` | Prefix-match length + cosine similarity between two concepts |
| `persona` | Region characteristic concepts + coherence-based control parameters |
| `compose_persona` | Model × persona composition — *coming soon* |

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env        # then set NEO0_API_URL and NEO0_API_KEY
python server.py
```

The server speaks streamable-HTTP MCP on port `8000` at path `/mcp`.

### Use with Claude

In Claude: **Settings → Connectors → Add custom connector**, then enter your server URL ending in `/mcp`.

## Configuration

| Variable | Description |
|---|---|
| `NEO0_API_URL` | Neo0 engine API base URL |
| `NEO0_API_KEY` | Engine API key |

## License

This MCP shell is provided for **evaluation only** — see [LICENSE](LICENSE).
**No patent license is granted by this repository; rights are reserved.**

The Neo0 coordinate engine is patent-pending and provided as a hosted API
under separate terms. Use of the API may include a limited patent license;
independently reimplementing the engine is not covered.

© 2026 Seungchul Lee — https://neo0.ai
