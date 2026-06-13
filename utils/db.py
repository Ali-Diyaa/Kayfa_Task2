# utils/db.py
import streamlit as st
from pymongo import MongoClient
import os, json
from pathlib import Path

@st.cache_resource
def get_client():
    uri = st.secrets.get("MONGO_URI", os.getenv("MONGO_URI", ""))
    if not uri: return None
    return MongoClient(uri, serverSelectionTimeoutMS=3000)

def get_db():
    client = get_client()
    if client is None: return None
    db_name = st.secrets.get("MONGO_DB", os.getenv("MONGO_DB", "Kayfa_database"))
    return client[db_name]

def get_collection(name: str):
    db = get_db()
    if db is None: return None
    return db[name]

def find_all(coll_name: str, query: dict = {}):
    col = get_collection(coll_name)
    if col is not None:
        try: return list(col.find(query, {"_id": 0}))
        except Exception: pass
    p = Path(__file__).resolve().parent.parent / "scripts" / "seed_json" / f"{coll_name}.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    return []

def load_json_fallback(name: str):
    return find_all(name)