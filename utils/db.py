import streamlit as st
from pymongo import MongoClient
import os, json
from pathlib import Path

@st.cache_resource
def get_client():
    uri = st.secrets.get("MONGO_URI", os.getenv("MONGO_URI", ""))
    return MongoClient(uri, serverSelectionTimeoutMS=3000) if uri else None

def get_db():
    client = get_client()
    if not client: return None
    db_name = st.secrets.get("MONGO_DB", os.getenv("MONGO_DB", "Kayfa_database"))
    return client[db_name]

def find_all(coll_name: str, query: dict = {}):
    db = get_db()
    if db is not None:
        try: return list(db[coll_name].find(query, {"_id":0}))
        except: pass
    p = Path(__file__).resolve().parent.parent / "scripts" / "seed_json" / f"{coll_name}.json"
    if p.exists():
        import json
        with open(p, encoding="utf-8") as f: d = json.load(f)
        return d if isinstance(d, list) else [d]
    return []