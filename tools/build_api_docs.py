"""Build an illustrated pdoc reference for the actual laboratory scripts.

The twelve files share the basename analysis.py. Importlib gives each a unique
documentation name; pdoc still reads source, signatures and docstrings from
the original file. Importing these guarded modules does not run a laboratory.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
from html.parser import HTMLParser
import importlib.util
from importlib.metadata import version
import io
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems'


class Page(HTMLParser):
    """Collect anchors, links and image references from rendered HTML."""
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.images = set(), [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'img' and 'src' in attrs:
            self.images.append(attrs['src'])


def inventory():
    records = json.loads((ROOT / 'docs/api-sources.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'laboratories').glob('*/analysis.py')}
    if actual != {r['source'] for r in records} or len(records) != 12:
        raise ValueError('Documentation must cover the exact twelve laboratory scripts.')
    modules = {'course_guide': {'source': 'docs/api_index.py', 'public_definitions': []}}
    for record in records:
        tree = ast.parse((ROOT / record['source']).read_text(encoding='utf-8'))
        public = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith('_')]
        if not ast.get_docstring(tree) or any(not ast.get_docstring(n) for n in public):
            raise ValueError('Missing public documentation: ' + record['source'])
        if [n.name for n in public] != ['run']:
            raise ValueError('Review the new public interface: ' + record['source'])
        # The module contains documentation, a function definition and a guarded
        # direct-execution call only; importing cannot perform numerical work.
        statements = tree.body[1:]
        if len(statements) != 2 or not isinstance(statements[0], ast.FunctionDef):
            raise ValueError('Unexpected import-time statement: ' + record['source'])
        guard = ast.parse('if __name__ == "__main__":\n    run()').body[0]
        if ast.dump(statements[1], include_attributes=False) != ast.dump(guard, include_attributes=False):
            raise ValueError('Expected a standard main guard: ' + record['source'])
        modules[record['module']] = {'source': record['source'], 'public_definitions': ['run'], 'title': record['title']}
    return modules


def assets():
    images = {}
    for number, path in enumerate(sorted((ROOT / 'laboratories').glob('*/analysis.py')), 1):
        for name in ('physical-system', 'system-diagram'):
            images[f'{number:02d}-{name}.png'] = path.parent / 'figures' / f'{name}.png'
        images[f'{number:02d}-response.png'] = path.parent / 'response.png'
    images['interacting-tanks.png'] = ROOT / 'problem-sets/integrated-design/figures/interacting-tanks.png'
    images['diagram-atlas.pdf'] = ROOT / 'docs/diagram-atlas.pdf'
    if any(not p.is_file() for p in images.values()):
        raise ValueError('A required equipment, signal or response figure is missing.')
    return images


def source_hashes(modules):
    sources = [ROOT / info['source'] for info in modules.values()]
    sources += list((ROOT / 'docs/pdoc-template').glob('*'))
    sources += [ROOT / 'tools/build_api_docs.py', ROOT / 'requirements-docs.txt', ROOT / 'docs/api-sources.json']
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
            for p in sorted(sources)}


def asset_hashes():
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in assets().values()}


def validate_site(output, modules):
    pages = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in output.glob('*.html')}
    expected = {output / (name + '.html') for name in modules} | {output / 'index.html'}
    if set(pages) != expected:
        raise ValueError('Rendered page set differs from the full module inventory.')
    for name, info in modules.items():
        page = pages[output / (name + '.html')]
        if not set(info['public_definitions']).issubset(page.ids):
            raise ValueError('Missing function anchors: ' + name)
        expected_images = 3 if name.startswith('lab') else 1
        if len([x for x in page.images if x.startswith('assets/')]) != expected_images:
            raise ValueError('Missing illustrated content: ' + name)
    checked = 0
    for source, parsed in pages.items():
        text = source.read_text(encoding='utf-8')
        if re.search(r'file:///|[A-Za-z]:[\\/](?:Users|home|runner)[\\/]', text):
            raise ValueError('Machine-specific path found: ' + source.name)
        for value in parsed.links:
            target = urlsplit(value)
            if target.scheme or target.netloc:
                continue
            destination = (source.parent / unquote(target.path)).resolve() if target.path else source
            if not destination.is_relative_to(output) or not destination.is_file():
                raise ValueError(f'Broken local link in {source.name}: {value}')
            if target.fragment and destination in pages and unquote(target.fragment) not in pages[destination].ids:
                raise ValueError(f'Broken local anchor in {source.name}: {value}')
            checked += 1
    if not (output / 'search.js').is_file() or (output / 'search.js').stat().st_size < 100:
        raise ValueError('Missing pdoc search index.')
    expected_assets = set(assets())
    if {p.name for p in (output / 'assets').iterdir()} != expected_assets:
        raise ValueError('Published asset inventory differs from the figures and vector atlas.')
    return {'status': 'passed', 'laboratories': 12, 'module_pages': len(modules),
            'html_files_including_redirect': len(pages), 'public_entry_points': 12,
            'local_images': sum(name.endswith('.png') for name in expected_assets),
            'local_documents': sum(name.endswith('.pdf') for name in expected_assets),
            'local_links_and_anchors_checked': checked}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/api')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = (ROOT / args.output).resolve() if not args.output.is_absolute() else args.output.resolve()
    if output != ROOT / 'docs/api' and not output.is_relative_to(ROOT / 'build'):
        raise ValueError('Output must be docs/api or a directory under build/.')
    modules = inventory()
    if args.check:
        record = json.loads((output / 'build.json').read_text(encoding='utf-8'))
        if record['source_sha256_lf'] != source_hashes(modules) or record['source_image_sha256'] != asset_hashes():
            raise ValueError('Documentation is stale; rebuild from the changed source or images.')
        actual = {p.relative_to(output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in output.rglob('*') if p.is_file() and p.name != 'build.json'}
        if actual != record['artifact_sha256']:
            raise ValueError('Generated files changed or the artifact set differs.')
        checks = validate_site(output, modules)
    else:
        import pdoc
        if pdoc.__version__ != '16.0.0':
            raise RuntimeError('Install requirements-docs.txt; pdoc 16.0.0 is required.')
        documents = {}
        for name, info in modules.items():
            spec = importlib.util.spec_from_file_location(name, ROOT / info['source'])
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                spec.loader.exec_module(module)
            if captured.getvalue():
                raise ValueError('A laboratory unexpectedly ran while importing: ' + name)
            documents[name] = pdoc.doc.Module(module)
        favicon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#185a69"/><text x="32" y="43" fill="white" text-anchor="middle" font-size="32" font-family="sans-serif">CS</text></svg>'
        pdoc.render.configure(docformat='markdown', math=True, search=True, show_source=True,
            template_directory=ROOT / 'docs/pdoc-template',
            edit_url_map={name: REPOSITORY + '/blob/main/' + info['source'][:-3] for name, info in modules.items()},
            favicon='data:image/svg+xml,' + quote(favicon),
            footer_text='Synthetic teaching scenarios; inspect assumptions and numerical checks.')
        pdoc.render.env.globals['course_modules'] = modules
        output.mkdir(parents=True, exist_ok=True)
        (output / 'assets').mkdir(exist_ok=True)
        for name, source in assets().items():
            shutil.copyfile(source, output / 'assets' / name)
        for name, document in documents.items():
            (output / (name + '.html')).write_bytes(pdoc.render.html_module(document, documents).encode('utf-8'))
        (output / 'search.js').write_bytes(pdoc.render.search_index(documents).encode('utf-8'))
        (output / 'index.html').write_bytes(b'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=course_guide.html"><title>Control of Dynamical Systems API</title></head><body><a href="course_guide.html">Open the illustrated Python reference</a></body></html>\n')
        (output / '.nojekyll').write_bytes(b'')
        checks = validate_site(output, modules)
        record = {'generator': 'pdoc', 'pdoc_version': pdoc.__version__,
                  'render_dependencies': {name: version(name) for name in ('Jinja2', 'MarkupSafe', 'markdown2', 'Pygments')},
                  'source_sha256_lf': source_hashes(modules), 'source_image_sha256': asset_hashes(),
                  'artifact_sha256': {p.relative_to(output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'build.json'},
                  'coverage': modules, 'validation': checks}
        (output / 'build.json').write_bytes((json.dumps(record, indent=2) + '\n').encode('utf-8'))
    print(json.dumps(checks, indent=2))
    print('Documentation: ' + str(output / 'index.html'))


if __name__ == '__main__':
    main()
