# mcp_server.py
# Combined MCP server: UniProt, PDBe mapping/metadata, AlphaFold prediction endpoint wrappers.
import uvicorn
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Bio MCP Tools (UniProt, PDBe, AlphaFold)")

# --- UniProt endpoints ---
UNIPROT_SEARCH = "https://rest.uniprot.org/uniprotkb/search"
UNIPROT_ENTRY = "https://rest.uniprot.org/uniprotkb/{}.json"

@app.get("/uniprot/search")
def search_uniprot(query: str, limit: int = 5):
    params = {"query": query, "format": "json", "size": limit}
    r = requests.get(UNIPROT_SEARCH, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return {"results": [item.get("primaryAccession") for item in data.get("results", [])]}

@app.get("/uniprot/entry")
def get_uniprot_entry(accession: str):
    r = requests.get(UNIPROT_ENTRY.format(accession), timeout=30)
    r.raise_for_status()
    raw = r.json()
    go_terms = []
    for xref in raw.get("uniProtKBCrossReferences", []):
        if xref.get("database") == "GO":
            for prop in xref.get("properties", []):
                val = prop.get("value")
                if val:
                    go_terms.append(val)
    seq = raw.get("sequence", {}).get("value")
    name = raw.get("proteinDescription", {})\
        .get("recommendedName", {})\
        .get("fullName", {})\
        .get("value")
    return {"accession": accession, "name": name, "sequence": seq, "length": len(seq) if seq else None, "go_terms": sorted(list(set(go_terms)))}

# --- PDBe mapping and summary endpoints ---
PDBe_MAP = "https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{}"
PDBe_SUMMARY = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/{}"

@app.get("/pdb/search_by_uniprot")
def pdb_search_by_uniprot(accession: str):
    r = requests.get(PDBe_MAP.format(accession), timeout=30)
    if r.status_code == 404:
        return {"mappings": []}
    r.raise_for_status()
    data = r.json().get(accession, {}).get("mappings", [])
    return {"mappings": data}

@app.get("/pdb/summary")
def pdb_summary(pdb_id: str):
    r = requests.get(PDBe_SUMMARY.format(pdb_id), timeout=30)
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="PDB ID not found")
    r.raise_for_status()
    items = r.json().get(pdb_id, [])
    if not items:
        raise HTTPException(status_code=404, detail="No summary for pdb_id")
    return items[0]

# --- AlphaFold API wrapper (EMBL-EBI Alphafold) ---
ALPHAFOLD_API = "https://alphafold.ebi.ac.uk/api/prediction/{}"

@app.get("/af/prediction")
def af_prediction(accession: str):
    r = requests.get(ALPHAFOLD_API.format(accession), timeout=30)
    if r.status_code == 404:
        return {"present": False, "data": None}
    r.raise_for_status()
    data = r.json()
    return {"present": True, "data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9001)
