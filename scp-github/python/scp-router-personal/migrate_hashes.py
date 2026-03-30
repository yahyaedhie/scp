import sqlite3
import hashlib
import json
from config import Config

def compute_salted_hash(code, definition, domain, version):
    salt = Config.COMPANY_SECRET_SALT
    content = f"{salt}{code}{definition}{domain}{version}"
    return hashlib.sha256(content.encode()).hexdigest()[:8]

def migrate():
    db_path = "anchors.db"
    print(f"Starting Hash Migration for {db_path}...")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all anchors
    cursor.execute("SELECT code, definition, domain, version FROM anchors")
    anchors = cursor.fetchall()
    
    updates = []
    for row in anchors:
        new_hash = compute_salted_hash(row['code'], row['definition'], row['domain'], row['version'])
        updates.append((new_hash, row['code']))
        print(f"Update {row['code']}: NEW HASH -> {new_hash}")

    # Apply updates
    cursor.executemany("UPDATE anchors SET hash = ? WHERE code = ?", updates)
    
    # Update versions table too
    cursor.execute("SELECT code, version FROM versions")
    v_rows = cursor.fetchall()
    v_updates = []
    for v in v_rows:
        # We need the full definition to re-hash versions... 
        # For simplicity, we match the code/version from anchors
        cursor.execute("SELECT hash FROM anchors WHERE code = ?", (v['code'],))
        a_hash = cursor.fetchone()
        if a_hash:
            v_updates.append((a_hash[0], v['code'], v['version']))

    cursor.executemany("UPDATE versions SET hash = ? WHERE code = ? AND version = ?", v_updates)
    
    conn.commit()
    conn.close()
    print("Migration Complete.")

if __name__ == "__main__":
    migrate()
