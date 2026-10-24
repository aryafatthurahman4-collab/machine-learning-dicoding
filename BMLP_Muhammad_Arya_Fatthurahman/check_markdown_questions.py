import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_md(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"==================== {nb_path} ====================")
    for idx, cell in enumerate(nb.get('cells', [])):
        ctype = cell.get('cell_type')
        source = "".join(cell.get('source', []))
        if ctype == 'markdown':
            if "JAWAB" in source or "Perhatian" in source or "Interpretasi" in source or "Penting" in source or "Catatan" in source:
                print(f"Cell [{idx}] (MARKDOWN):")
                print(source)
                print("----------------------------------------\n")

check_md('clustering_template.ipynb')
check_md('klasifikasi_template.ipynb')
