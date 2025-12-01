# Protein Structure Hunter: An MCP-Powered Agent for Automated UniProt, PDB, and AlphaFold Retrieval and Docking Structure Selection

## Problem Statement
Identifying the most appropriate 3D structure of a protein is a critical step in computational drug discovery workflows, especially molecular docking, virtual screening, and structure-based drug design. However, manually navigating biological databases (UniProt, PDB, AlphaFold DB), tracking GO annotations, checking sequence coverage, and selecting the most reliable structure can be tedious, fragmented across multiple resources, and error-prone.

Researchers often struggle with:
- Searching multiple protein databases individually
- Checking many PDB structures for method, resolution, coverage, ligands, and biological relevance
- Evaluating AlphaFold predictions and their confidence scores
- Consolidating this information to select the most suitable structure for docking

This project presents Protein Structure Hunter, an AI agent system that takes a protein name or gene symbol as input, automatically retrieves the corresponding UniProt entry and GO terms, identifies available PDB and AlphaFold structures, evaluates them using a transparent scoring system, and recommends the best structure for docking—through an automated, reproducible, multi-agent pipeline that uses Model Context Protocol (MCP) for typed interaction with biological APIs.

## Solution Overview
Protein Structure Hunter is an AI agent system built using modular MCP tools that integrate:
- UniProt MCP Tool – resolves names → accession IDs, returns sequence + GO terms
- PDB Structure Agent – retrieves experimentally solved structures mapped to the accession
- AlphaFold Agent – retrieves AFDB predicted models and pLDDT confidence
- Structure Scoring Agent – evaluates structures based on experimental quality, coverage, method, confidence, and completeness
- Selection & Explainability Agent – picks the best structure and provides scientific justification

The core problem—identifying and evaluating structural candidates—is solved using a multi-agent workflow that enforces modularity, parallelization, and clear responsibilities between sub-agents. All database interactions use well-defined MCP tools for clean, schema-validated communication rather than ad-hoc API calls.

## Track & Value Proposition
**Track:** Concierge Agents or Enterprise Agents

**Core Value:** The agent automates a workflow every structure-based drug discovery researcher faces. Selecting a structure can take 15–30 minutes per protein; large campaigns involve hundreds of targets. Protein Structure Hunter reduces this process to seconds, standardizes structure quality evaluation, reduces human error, provides transparent rationale and logs, and enables reproducible pipelines.

## Architecture
The architecture follows a multi-agent orchestration pattern with sub-agents and tools:
1. Interface Agent – accepts user queries
2. UniProt Agent (MCP) – returns accession, sequence, GO terms
3. PDB Agent – lists mapped experimental structures and metadata
4. AlphaFold Agent – retrieves AF models and pLDDT
5. Scoring Agent – computes composite scores from normalized metrics
6. Selection & Explainability Agent – uses LLM to generate rationale and preparation checklist
7. Sessions & Memory – stores recent queries and selections
8. Observability – logs requests, latencies, and scores

## Implementation
The repo includes:
- A combined FastAPI MCP tool server (`mcp_server.py`) exposing endpoints:
  - `/uniprot/search`
  - `/uniprot/entry`
  - `/pdb/search_by_uniprot`
  - `/pdb/summary`
  - `/af/prediction`
- MCP descriptor files in `tools/` for UniProt, PDB, and AlphaFold
- A runnable Kaggle notebook (`protein_mcp_full_notebook.ipynb`) demonstrating how to start the server, call MCP tools, and run the orchestrator
- A simple scoring function and docking-prep checklist generator

## Scoring Methodology & Selection Criteria
Metrics considered:
- Sequence coverage
- Resolution (lower is better)
- Experimental method (X-ray > Cryo-EM > NMR)
- R-free when available
- Ligand presence
- Missing regions
- AlphaFold pLDDT

Composite score (example):
score = 0.30 * seq_identity + 0.25 * experimental_quality + 0.15 * completeness + 0.10 * ligand_score + 0.10 * confidence + 0.10 * assembly_score

Decision rules:
- Prefer experimental structures over predicted when quality is adequate
- Avoid structures with resolution > 4.0 Å unless no alternatives
- Prefer structures with native ligand when relevant
- Warn if sequence coverage < 60%

## Demonstration & Notebook
The Kaggle notebook shows:
- Writing the MCP server file
- Writing MCP descriptors
- Starting the server with `nohup` (recommended on Kaggle)
- MCP client wrappers with fallbacks
- Async orchestrator calling UniProt → (PDB + AF) in parallel
- Scoring, ranking, and docking-prep output

## Limitations & Safety
- PDB metadata may be incomplete; scoring transparently accounts for missing data
- AlphaFold predictions may have low-confidence regions
- Binding-site detection and loop modeling are not included
- Recommendations are advisory — experimental validation required

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Start MCP server: `python mcp_server.py`
3. Open the notebook and run cells in order

## Future Work
- Add sequence-identity alignment scoring with Biopython
- Implement site-aware pLDDT scoring at predicted binding pockets
- Integrate Modeller/pdbfixer for loop reconstruction before docking
- Add automated docking pipeline (e.g., AutoDock Vina) as optional downstream tool
