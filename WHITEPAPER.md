# Neo0 Whitepaper

**Infrastructure that gives meaning an immutable coordinate address**
— AI memory, knowledge, and privacy as coordinates, not vectors.

> 한국어 백서: [WHITEPAPER.ko.md](WHITEPAPER.ko.md)

---

## One-line summary

Neo0 assigns every concept an **immutable address on a recursively partitioned coordinate lattice**. Concepts close in meaning share a coordinate prefix and gather in the same "territory," and that coordinate becomes the unit of meaning, address, routing, and governance. With no separate ontology graph and no opaque vectors recomputed every time, meaning is computed once and **fixed into a readable coordinate**.

---

## 1. The problem — meaning is hard to handle

Today's LLMs represent meaning as high-dimensional vectors. Powerful, but the following are hard:

- **Persistence**: vectors are regenerated per session and per model, and on their own are not stable identifiers.
- **Sharing**: model A's vector space and model B's vector space are incompatible, making it hard to share memory between AIs.
- **Explainability**: a 1,536-dimensional vector is not human-readable. There is no address to show "why is this here."
- **Right to be forgotten**: there is no mechanism to *verifiably* delete a specific meaning.

Vector databases make search fast but do not solve these four — they index location but do not assign an **immutable address and hierarchy**.

---

## 2. Neo0 — crystallizing meaning into coordinates

Neo0 converts a meaning vector into an **immutable address on a recursively partitioned coordinate lattice**.

- Close meaning → close coordinate (shared prefix = same territory)
- Once issued, an address never changes (immutable registry, zero drift)
- The coordinate itself is meaning, address, routing path, and governance unit

In short, it turns meaning from a "searchable point" into a **readable, shareable, controllable address**.

---

## 3. How it works

```
embedding   →  density-aligned partition  →  recursive coordinate  →  immutable registry
(meaning vec)   (spherical Voronoi)           (hierarchical address)    (zero drift)
```

### Prefix Sharing

Concepts close in meaning share a coordinate prefix and gather in the
same region. Concepts belonging to nature and matter form one region,
people and places another, emotion and morality yet another.

How many digits of the prefix you read determines the scope of a query.
A short prefix designates a broad area; a long prefix, a narrow one.

*Actual coordinate values and lattice parameters are not published.
Evaluation access is provided through the engine API.*

---

## 4. What makes it different

**Versus vector databases** — a vector DB offers similarity search but gives concepts no stable address and is internally opaque. Neo0 adds an immutable address plus a human-readable hierarchy.

**Versus ontologies (knowledge graphs)** — an ontology is built by hand, one concept and relation at a time. Neo0 builds the coordinate structure **automatically** from embeddings, and the prefix hierarchy effectively serves as a geometric ontology.

In one line: where competing approaches *connect or search* meaning, Neo0 *fixes meaning into coordinates*, unifying representation, addressing, and governance.

---

## 5. Use cases

- **Instant connection as an MCP plugin** — heterogeneous LLMs, Claude included, connect to the Neo0 MCP server and immediately share coordinate memory and switch territory personas, with no change to internal weights
- **Persistent, shared AI memory** — heterogeneous models share the same numeric coordinates to exchange memory
- **Verifiable right to be forgotten** — cryptographic erasure by coordinate zone, giving unrecoverable and auditable deletion
- **Explainable search and routing** — the coordinate prefix directly reveals "which region of meaning"
- **Per-model persona control** — expression strength and temperature adjusted by the coherence of a coordinate territory

---

## 6. Technical validation

- **Measured advantage**: density-aligned partitioning outperforms random partitioning in bucket recall (recall@bucket 0.47 vs 0.18)
- **Immutability**: zero percent address drift in the registry
- **Live operation**: an MCP server wrapping the coordinate engine is running and callable directly from MCP clients including Claude
- **Separation verified**: the engine (private) and the public interface are separated, and external calls are confirmed to work end to end through the full path

---

## 7. Intellectual property

Neo0's coordinate infrastructure originates from a recursive spatial
partitioning patent granted in 2002 (KR 10-0560735), extended through
2026 by 58 subsequent patent applications. All subsequent filings
remain pending; none have yet been granted.

---

## 8. Status and roadmap

- **Now** — a live coordinate engine plus a public MCP interface (open-core)
- **Next** — wider adoption via connector directory listing, partnerships, and a reasoning layer on top of coordinates

---

*Neo0 — https://neo0.ai*
