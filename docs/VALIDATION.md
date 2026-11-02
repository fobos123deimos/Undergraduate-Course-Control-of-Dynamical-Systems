# Validation status

Validation date: 2 November 2026. These results apply to the new original scenarios; predecessor-edition test results are not reused.

## Python programs and notebooks

All twelve original Python programs passed in clean processes. All twelve notebooks were validated as notebook documents, executed with fresh kernels and saved with their computed outputs and figures. Optional package-install cells are retained for Colab users but skipped during automated execution. All twelve saved notebook figures were visually inspected.

The local environment used Python 3.13.12, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2 and python-control 0.10.2. The dependency ranges are recorded separately; this does not certify every permitted version combination. See the per-module [execution record](validation.json).

GitHub Actions runs all twelve programs and all twelve notebooks on Ubuntu with Python 3.12. Consult the [validation workflow](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/actions/workflows/validate.yml) for the result associated with the current commit.

| Independent model check | Reproduced value |
|---|---|
| Thermal sensor under-reading after 60 s | 0.240761 K |
| Isolation threshold | 28.284271 rad/s |
| Motor PI final speed under the stated load | 5.000000 rad/s |
| Third-order gain stability | strict interval 0 < K < 96 |
| Lead-only phase margin | 55 degrees |
| PID recovery integral absolute error | 9.756216 without back-calculation; 1.841207 with it |
| Thermal state-feedback gain | [3, 5.5] |
| First digital stability boundary | Ts = 0.75 s, endpoint excluded |
| Fitted synthetic process [gain, time constant, delay] | [1.80002469, 3.99349123, 0.60428920] |
| Held-out synthetic-input prediction RMSE | 0.014502 |

Checks include agreement between analytic and integrated responses, physical equilibrium, notch cancellation, root locations, stability boundaries, controller margins, observer eigenvalues and convergence, and independent-input synthetic validation. They check selected invariants and outcomes; they are not formal proofs of every derivation in the exercise collection.

## Documents and navigation

All 40 LaTeX documents compiled with Tectonic 0.17.0, totaling 182 pages. Every final page was rendered and visually inspected, including focused re-renders after layout corrections. No missing-character, undefined-command, LaTeX-error or overfull-box warnings remain. The [document record](document-validation.json) lists page counts and SHA-256 hashes.

Local navigation and all 24 Colab links in the Markdown pages were checked against actual notebook paths. Teaching files were also checked for accidental source-handout filenames or institutional/professor references; none were found.

## Diagram and notation revision

Thirteen new physical illustrations and twelve control diagrams give 25 editable TikZ figures with PNG previews. The [atlas and gallery](DIAGRAMS.md) show both equipment and mathematical structures. All twelve notebooks display the relevant physical and control illustrations. The [notation review](NOTATION.md) records 284 distinct Markdown/notebook mathematical expressions compiled without syntax or missing-glyph errors. Executable notebook code is unchanged.

## Integrated exercise revision

The twelve laboratory sets now contain five problems each, with three linked parts per problem. The general collection has five cases with six parts each: 65 problems and 210 parts in total. All 88 retained numerical checks and 67 additional integrated checks passed locally. The new checks include nonlinear tank integration, numerical linearization, energy balances, actuator feasibility, sensor-lag margins, sampled thermal feedback and fractional-delay integration. See [the exercise guide](EXERCISES.md).

The [GitHub validation workflow](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/actions/workflows/validate.yml) runs programs, notebooks, both exercise suites, notation checks and GNU Octave after publication.

## MATLAB, GNU Octave and Simulink

All twelve scenarios in the portable implementation passed their computations and assertions in GNU Octave 11.1.0, using the control package and a noninteractive graphics backend. Current executions are available in the Octave job of the [validation workflow](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/actions/workflows/validate.yml), which runs lessons 01 through 12. The saturated-PID recovery errors were approximately 9.7562 and 1.8412; the synthetic capstone fitted approximately [1.8003, 4.0005, 0.5981] with held-out prediction RMSE 0.014542. The latter differs slightly from Python because the seeded samples and fitting implementations differ. No local MATLAB or Octave executable was available.

The Simulink script generates six nominal models when executed in MATLAB with Simulink. Proprietary MATLAB/Simulink execution and generated `.slx` files are not claimed. The capstone uses different positive-parameter fitting implementations and random-number generators in Python and MATLAB/Octave, as documented in [the port notes](../matlab/README.md).

## Evidence boundary

All data are synthetic. There are no measured experiments, hardware calibration results or assertions of experimental agreement. See [model limitations](LIMITATIONS.md).
