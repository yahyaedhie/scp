import sqlite3
import json
import hashlib
from typing import Optional, Dict, List
from contextlib import contextmanager
import re

class AnchorStore:
    def __init__(self, db_path: str = "anchors.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS anchors (
                    code TEXT PRIMARY KEY,
                    expansion TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    version TEXT NOT NULL,
                    constraints TEXT,
                    keywords TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS versions (
                    code TEXT,
                    version TEXT,
                    hash TEXT,
                    previous_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (code, version)
                )
            """)
    
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def _compute_hash(self, code: str, definition: str, domain: str, version: str) -> str:
        """Compute 8-character hash for anchor"""
        content = f"{code}{definition}{domain}{version}"
        full_hash = hashlib.sha256(content.encode()).hexdigest()
        return full_hash[:8]
    
    def _clean_code(self, code: str) -> str:
        """Ensure code has brackets"""
        if not code.startswith('['):
            code = f'[{code}]'
        return code.upper()
    
    def create(self, code: str, expansion: str, definition: str, domain: str,
               constraints: List[str] = None, keywords: List[str] = None) -> Dict:
        """Create a new anchor"""
        code = self._clean_code(code)
        version = "1.0"
        hash_val = self._compute_hash(code, definition, domain, version)
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO anchors (code, expansion, definition, domain, hash, version, constraints, keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, expansion, definition, domain, hash_val, version,
                  json.dumps(constraints or []), json.dumps(keywords or [])))
            
            conn.execute("""
                INSERT INTO versions (code, version, hash)
                VALUES (?, ?, ?)
            """, (code, version, hash_val))
            
            conn.commit()
        
        return self.get(code)
    
    def get(self, code: str, domain: str = None) -> Optional[Dict]:
        """Get anchor by code, optionally filtered by domain"""
        code = self._clean_code(code)
        
        with self._get_connection() as conn:
            if domain:
                cursor = conn.execute(
                    "SELECT * FROM anchors WHERE code = ? AND domain = ?",
                    (code, domain)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM anchors WHERE code = ?",
                    (code,)
                )
            row = cursor.fetchone()
            
            if row:
                return {
                    "code": row["code"],
                    "expansion": row["expansion"],
                    "definition": row["definition"],
                    "domain": row["domain"],
                    "hash": row["hash"],
                    "version": row["version"],
                    "constraints": json.loads(row["constraints"]) if row["constraints"] else [],
                    "keywords": json.loads(row["keywords"]) if row["keywords"] else []
                }
        return None
    
    def search_by_keyword(self, keyword: str, domain: str = None) -> List[Dict]:
        """Search anchors by keyword"""
        with self._get_connection() as conn:
            query = """
                SELECT * FROM anchors 
                WHERE keywords LIKE ? OR expansion LIKE ? OR definition LIKE ?
            """
            params = [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
            
            if domain:
                query += " AND domain = ?"
                params.append(domain)
            
            cursor = conn.execute(query, params)
            
            return [{
                "code": row["code"],
                "expansion": row["expansion"],
                "definition": row["definition"],
                "domain": row["domain"],
                "hash": row["hash"],
                "version": row["version"]
            } for row in cursor.fetchall()]
    
    def list_by_domain(self, domain: str) -> List[Dict]:
        """List all anchors in a domain"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM anchors WHERE domain = ?",
                (domain,)
            )
            return [{
                "code": row["code"],
                "expansion": row["expansion"],
                "definition": row["definition"],
                "domain": row["domain"],
                "hash": row["hash"],
                "version": row["version"]
            } for row in cursor.fetchall()]