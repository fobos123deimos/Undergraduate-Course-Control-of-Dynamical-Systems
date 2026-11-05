"""Compile refined equipment drawings and every PDF which embeds their TikZ.

Use Tectonic 0.17.0 and Poppler pdftoppm. This does not run laboratory
calculations. The standard-library-only --check verifies committed source and
artifact hashes; visual inspection is still required after diagram changes.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'build/diagram-render'
RECORD=ROOT/'docs/diagram-build.json'


def physical_sources():
    return sorted(ROOT.glob('laboratories/*/figures/physical-system.tikz'))+[ROOT/'problem-sets/integrated-design/figures/interacting-tanks.tikz']


def documents():
    return sorted(p for p in ROOT.rglob('*.tex') if 'build' not in p.relative_to(ROOT).parts and
        any(key in p.read_text(encoding='utf-8') for key in ('physical-system.tikz','interacting-tanks.tikz')))


def sha(path,text=False):
    content=path.read_bytes()
    return hashlib.sha256(content.replace(b'\r\n',b'\n') if text else content).hexdigest()


def source_hashes():
    sources=physical_sources()+sorted(ROOT.glob('laboratories/*/figures/system-diagram.tikz'))+documents()+[Path(__file__)]
    return {p.relative_to(ROOT).as_posix():sha(p,True) for p in sources}


def artifacts():
    return [p.with_suffix(ext) for p in physical_sources() for ext in ('.png','.pdf')]+[p.with_suffix('.pdf') for p in documents()]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tectonic',default='tectonic')
    parser.add_argument('--pdftoppm',default='pdftoppm')
    parser.add_argument('--jobs',type=int,default=3)
    parser.add_argument('--only-cached',action='store_true')
    parser.add_argument('--figures-only',action='store_true')
    parser.add_argument('--documents-only',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:
        record=json.loads(RECORD.read_text(encoding='utf-8'))
        assert record['source_sha256_lf']==source_hashes(),'Changed source: rebuild affected drawings/documents.'
        actual={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts()}
        assert record['artifact_sha256']==actual,'Changed or missing drawing/PDF artifact.'
        print(json.dumps({'status':'passed','physical_drawings':13,'control_diagrams':12,'embedded_documents':len(documents()),'artifacts':len(actual)}))
        return
    BUILD.mkdir(parents=True,exist_ok=True)
    if args.figures_only and args.documents_only:
        parser.error('Choose only one partial build mode.')
    def compile_file(path,outdir):
        command=[args.tectonic,'--keep-logs','--outdir',str(outdir)]
        if args.only_cached:command+=['--only-cached']
        result=subprocess.run(command+[path.name],cwd=path.parent,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        key=path.relative_to(ROOT).as_posix().replace('/','__')
        (BUILD/(key+'.txt')).write_text(result.stdout,encoding='utf-8')
        if result.returncode:raise RuntimeError(path.as_posix()+'\n'+result.stdout[-3000:])
        log=(outdir/path.with_suffix('.log').name).read_text(encoding='utf-8',errors='replace')
        if 'Missing character:' in log or '! LaTeX Error' in log:raise RuntimeError('Typesetting error: '+str(path))
        print('Compiled '+path.relative_to(ROOT).as_posix(),flush=True)
    def figure(source):
        name=source.parent.parent.name
        wrapper=BUILD/(name+'.tex')
        wrapper.write_text(r'\documentclass[tikz,border=6pt]{standalone}'+'\n'+
            r'\usepackage[T1]{fontenc}\usepackage{lmodern,amsmath,amssymb}'+'\n'+
            r'\usetikzlibrary{arrows.meta,positioning,calc,decorations.pathmorphing}'+'\n'+
            r'\definecolor{ink}{RGB}{20,53,78}'+'\n'+
            r'\begin{document}\input{../../'+source.relative_to(ROOT).as_posix()+r'}\end{document}'+'\n',encoding='utf-8')
        compile_file(wrapper,BUILD)
        shutil.copyfile(wrapper.with_suffix('.pdf'),source.with_suffix('.pdf'))
        subprocess.run([args.pdftoppm,'-singlefile','-scale-to','2600','-png',str(source.with_suffix('.pdf')),str(source.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    with ThreadPoolExecutor(max_workers=max(1,min(args.jobs,6))) as executor:
        if not args.documents_only:list(executor.map(figure,physical_sources()))
        if not args.figures_only:list(executor.map(lambda p:compile_file(p,p.parent),documents()))
    if args.figures_only:
        print('Figure previews complete. Inspect them before compiling embedded documents.')
        return
    for source in physical_sources():
        assert source.with_suffix('.pdf').stat().st_mtime>=source.stat().st_mtime,'Stale figure PDF: '+str(source)
        assert source.with_suffix('.png').stat().st_mtime>=source.with_suffix('.pdf').stat().st_mtime,'Stale figure PNG: '+str(source)
    record={'generator':'Tectonic 0.17.0 / TikZ + Poppler pdftoppm','physical_drawings':13,'control_diagrams':12,
        'embedded_documents':len(documents()),'png_long_edge':2600,
        'source_sha256_lf':source_hashes(),'artifact_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in artifacts()},
        'scope':'Original hypothetical equipment and signal diagrams. Numerical curves and laboratory implementations are unchanged.'}
    RECORD.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'built','physical_drawings':13,'embedded_documents':len(documents())}))


if __name__=='__main__':main()
