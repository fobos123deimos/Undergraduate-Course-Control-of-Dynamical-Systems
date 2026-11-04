# Illustrated Python documentation

The [pdoc reference](https://fobos123deimos.github.io/Undergraduate-Course-Control-of-Dynamical-Systems/) contains an introduction and twelve laboratory pages. Each laboratory includes its physical-system illustration, signal diagram, committed response plot, governing equation and actual executable source. Search, expandable source and mathematical rendering follow the Fast Wave documentation style.

The repository contains standalone scripts, not an installable Python package. Each real `laboratories/*/analysis.py` now exposes `run()` and a standard main guard. The script's original computation body is preserved inside that function. Direct command-line execution is unchanged; importing no longer executes experiments or writes plots. Internal callbacks remain local implementation details, visible in the source. Unique `lab01_...` documentation names resolve the repeated `analysis.py` basename without duplicating or reimplementing numerical code.

## Regenerate and inspect

```bash
python -m pip install -r requirements-docs.txt
python tools/build_api_docs.py
python tools/build_api_docs.py --check
python -m http.server 8000 --bind 127.0.0.1 --directory docs/api
```

Open `http://127.0.0.1:8000/`. Search works over HTTP, and MathJax requires an internet connection. Figures are local files bundled with the site. `--output build/api` creates an independent build. Only `docs/api` and directories under `build/` are accepted as output destinations.

The build imports the guarded scripts without calling `run()`. Checks cover the exact twelve-script inventory, documented entry points, every local link and anchor, three figures per laboratory and the 37-image inventory. The [manifest](api/build.json) records source hashes normalized to LF, original image hashes, generated-file hashes, dependency versions and coverage. `--check` rejects stale sources, changed figures and altered or unexpected artifacts.

Edit module/function docstrings and rebuild the site; do not hand-edit generated HTML. Refresh a laboratory's response plot only by executing its program and inspecting the numerical checks. These images are synthetic evidence and must retain their assumptions and captions.

## Publication

[The API workflow](../.github/workflows/api-docs.yml) checks the committed documentation, independently rebuilds it, and deploys successful main-branch builds to GitHub Pages. Configure Pages to use **GitHub Actions** as its source. Publication uses the workflow's temporary token. This guide does not itself establish that a deployment completed: inspect the actual workflow result and site.

pdoc documents Python only. MATLAB/Octave implementations, Simulink builders, reports and notebooks remain linked companion material with their existing validation boundaries.

Publication was verified on 4 November 2026 for source `8abb8d1bfa7d87c3736efbc404c166845c49daed`: [API build and deployment](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/actions/runs/41917142630) and [Python/Octave course validation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/actions/runs/41917142734) passed. The live site displayed the thermal equation, signal diagram and response figure; searching for `observer` returned two results. The [publication record](api-validation.json) identifies jobs, coverage and execution boundaries.

References: [pdoc rendering API](https://pdoc.dev/docs/pdoc/render.html), [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
