import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def inspect_nb(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"=== {nb_path} === ({len(nb.get('cells', []))} cells)")
    for idx, cell in enumerate(nb.get('cells', [])):
        ctype = cell.get('cell_type')
        source = "".join(cell.get('source', []))
        first_line = source.split('\n')[0] if source else ''
        lines_count = len(source.split('\n'))
        print(f"[{idx}] {ctype} ({lines_count} lines): {first_line[:60]}")

print("ORIGINAL TEMPLATES:")
inspect_nb('clustering_template.ipynb')
print("\n" + "="*50 + "\n")
inspect_nb('klasifikasi_template.ipynb')

print("\nSUBMISSION FILES:")
if os.path.exists('[Clustering]_Submission_Akhir_BMLP_Muhammad_Arya_Fatthurahman.ipynb'):
    inspect_nb('[Clustering]_Submission_Akhir_BMLP_Muhammad_Arya_Fatthurahman.ipynb')
print("\n" + "="*50 + "\n")
if os.path.exists('[Klasifikasi]_Submission_Akhir_BMLP_Muhammad_Arya_Fatthurahman.ipynb'):
    inspect_nb('[Klasifikasi]_Submission_Akhir_BMLP_Muhammad_Arya_Fatthurahman.ipynb')
