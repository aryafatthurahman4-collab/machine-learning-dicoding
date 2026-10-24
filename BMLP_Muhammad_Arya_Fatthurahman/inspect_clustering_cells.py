import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('clustering_template.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb.get('cells', [])):
    ctype = cell.get('cell_type')
    source = "".join(cell.get('source', []))
    if ctype == 'code':
        print(f"=== CELL [{idx}] ===")
        print(source)
        print()
