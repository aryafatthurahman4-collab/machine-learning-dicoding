import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_cells(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"==================== {nb_path} ====================")
    for idx, cell in enumerate(nb.get('cells', [])):
        ctype = cell.get('cell_type')
        source = "".join(cell.get('source', []))
        has_blank = "________" in source
        if ctype == 'code':
            print(f"Cell [{idx}] (CODE) - Has Blank: {has_blank}")
            print("--- SOURCE ---")
            print(source)
            print("--------------\n")

check_cells('clustering_template.ipynb')
check_cells('klasifikasi_template.ipynb')
