import json
import os
from datetime import datetime

KB_FILE = os.path.join(os.path.dirname(__file__), '../../kb_data.json')

# Ensure file exists
if not os.path.exists(KB_FILE):
    with open(KB_FILE, 'w') as f:
        json.dump([], f)

def add_kb_entry(tag, filename, text):
    entry = {
        'tag': tag,
        'filename': filename,
        'text': text,
        'uploaded_at': datetime.utcnow().isoformat()
    }
    kb = list_kb_entries()
    kb.append(entry)
    with open(KB_FILE, 'w') as f:
        json.dump(kb, f, indent=2)

def list_kb_entries():
    with open(KB_FILE, 'r') as f:
        return json.load(f)

def get_text_by_tag(tag):
    kb = list_kb_entries()
    texts = [entry['text'] for entry in kb if entry['tag'] == tag]
    return '\n\n'.join(texts)

def delete_kb_entry(tag, filename):
    kb = list_kb_entries()
    kb = [entry for entry in kb if not (entry['tag'] == tag and entry['filename'] == filename)]
    with open(KB_FILE, 'w') as f:
        json.dump(kb, f, indent=2) 