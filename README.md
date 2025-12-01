# Protein Structure Hunter

This package contains the runnable Kaggle notebook and MCP tool server for the Protein Structure Hunter project.

## Contents
- `protein_mcp_full_notebook.ipynb` — Executable Kaggle-style notebook with demo cells.
- `mcp_server.py` — Combined FastAPI MCP server exposing UniProt, PDBe, and AlphaFold endpoints.
- `tools/uniprot/mcp.json`, `tools/pdb/mcp.json`, `tools/af/mcp.json` — MCP descriptors for ADK/tool registration.
- `submission_writeup.md` — Project writeup suitable for Kaggle competition submission.
- `requirements.txt` — Python dependencies.

## Quickstart (local)
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Start MCP server:
```
python mcp_server.py
```
3. Open the notebook (`protein_mcp_full_notebook.ipynb`) and run cells. The notebook will try to use the MCP server at `http://127.0.0.1:9001`. If the server is not running, the notebook falls back to direct REST API calls.

## Quickstart (Kaggle)
- Upload the notebook to a Kaggle notebook, add the files in the repo, and in Cell 5 the notebook starts the MCP server using `nohup` (recommended) to keep it running between cells.

## Notes
- Do not include API keys. All calls are to public, unauthenticated endpoints.
- For production deployment, consider hosting `mcp_server.py` on Cloud Run and updating `tools/*/mcp.json` endpoints.
