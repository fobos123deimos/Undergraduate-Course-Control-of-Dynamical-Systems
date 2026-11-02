"""Execute the original computational collection in clean processes/kernels."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import os
import subprocess
import sys
import nbformat
from nbclient import NotebookClient

parser=argparse.ArgumentParser()
parser.add_argument('--notebooks',action='store_true')
parser.add_argument('--module')
parser.add_argument('--workers',type=int,default=2)
arguments=parser.parse_args()
root=Path(__file__).resolve().parents[1]

def validate(script):
    environment=dict(os.environ,MPLBACKEND='Agg',PYTHONIOENCODING='utf-8')
    run=subprocess.run([sys.executable,str(script)],cwd=script.parent,env=environment,capture_output=True,text=True,encoding='utf-8',timeout=240)
    (script.parent/'results.txt').write_text(run.stdout,encoding='utf-8')
    result={'module':script.parent.name,'script_passed':run.returncode==0}
    if run.returncode:
        result['error']=run.stderr
        print(script.parent.name,'FAIL',run.stderr,flush=True)
        return result
    notebook_path=script.with_name('notebook.ipynb')
    notebook=nbformat.read(notebook_path,as_version=4)
    nbformat.validate(notebook)
    if arguments.notebooks:
        installers=[(i,c) for i,c in enumerate(notebook.cells) if 'dependency-install' in c.get('metadata',{}).get('tags',[])]
        notebook.cells=[c for c in notebook.cells if 'dependency-install' not in c.get('metadata',{}).get('tags',[])]
        try:
            NotebookClient(notebook,timeout=240,kernel_name='python3',resources={'metadata':{'path':str(script.parent)}}).execute()
            figures=[o for c in notebook.cells for o in c.get('outputs',[]) if 'image/png' in o.get('data',{})]
            assert figures,'No saved figure output'
            for i,c in installers: notebook.cells.insert(i,c)
            nbformat.validate(notebook); nbformat.write(notebook,notebook_path)
            result.update(notebook_passed=True,saved_figures=len(figures))
        except Exception as error:
            result.update(notebook_passed=False,error=str(error))
    print(script.parent.name,'PASS' if result.get('notebook_passed',True) else 'NOTEBOOK FAIL',flush=True)
    return result

scripts=[p for p in sorted((root/'laboratories').glob('*/analysis.py')) if not arguments.module or p.parent.name==arguments.module]
assert scripts,'No matching module'
with ThreadPoolExecutor(max_workers=arguments.workers) as pool:
    records=list(pool.map(validate,scripts))
destination=root/'docs/validation.json'
if arguments.module and destination.exists():
    previous=json.loads(destination.read_text(encoding='utf-8'))
    records=[r for r in previous if r['module']!=arguments.module]+records
destination.write_text(json.dumps(records,indent=2),encoding='utf-8')
assert all(r['script_passed'] and r.get('notebook_passed',True) for r in records), 'Validation failures; see docs/validation.json'
print(f'Validated {len(records)} original computational modules.',flush=True)
