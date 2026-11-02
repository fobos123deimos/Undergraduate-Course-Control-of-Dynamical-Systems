# Exercise collections

The course includes **65 integrated problems**: five cross-topic design studies and five problems for each of twelve laboratories. Every collection provides English statements and worked solutions. Numerical parameters are hypothetical and all datasets are synthetic.

## General collection

[Five integrated studies (PDF)](integrated-design/exercises.pdf) · [Worked solutions (PDF)](integrated-design/solutions.pdf) · [Question source](integrated-design/exercises.tex) · [Solution source](integrated-design/solutions.tex)

## Laboratory practice

Each laboratory problem has three linked parts; each general case has six. The solution documents repeat every part and show worked reasoning. The sheets combine original physical illustrations, control diagrams and problems without figures. Both PDFs are accompanied by standalone LaTeX sources.

| Module | Topic | Questions | Worked solutions | LaTeX |
|---|---|---|---|---|
| 01 | [Thermal enclosure and a slow sensor](../laboratories/01-thermal-enclosure/README.md) | [PDF](../laboratories/01-thermal-enclosure/exercises.pdf) | [PDF](../laboratories/01-thermal-enclosure/exercise-solutions.pdf) | [Questions](../laboratories/01-thermal-enclosure/exercises.tex) / [Solutions](../laboratories/01-thermal-enclosure/exercise-solutions.tex) |
| 02 | [Ventilation as a bilinear dynamical system](../laboratories/02-ventilation/README.md) | [PDF](../laboratories/02-ventilation/exercises.pdf) | [PDF](../laboratories/02-ventilation/exercise-solutions.pdf) | [Questions](../laboratories/02-ventilation/exercises.tex) / [Solutions](../laboratories/02-ventilation/exercise-solutions.tex) |
| 03 | [A precision platform under floor motion](../laboratories/03-vibration-isolation/README.md) | [PDF](../laboratories/03-vibration-isolation/exercises.pdf) | [PDF](../laboratories/03-vibration-isolation/exercise-solutions.pdf) | [Questions](../laboratories/03-vibration-isolation/exercises.tex) / [Solutions](../laboratories/03-vibration-isolation/exercise-solutions.tex) |
| 04 | [A passive notch filter and component tolerance](../laboratories/04-notch-filter/README.md) | [PDF](../laboratories/04-notch-filter/exercises.pdf) | [PDF](../laboratories/04-notch-filter/exercise-solutions.pdf) | [Questions](../laboratories/04-notch-filter/exercises.tex) / [Solutions](../laboratories/04-notch-filter/exercise-solutions.tex) |
| 05 | [Flywheel speed regulation under a load torque](../laboratories/05-motor-load-rejection/README.md) | [PDF](../laboratories/05-motor-load-rejection/exercises.pdf) | [PDF](../laboratories/05-motor-load-rejection/exercise-solutions.pdf) | [Questions](../laboratories/05-motor-load-rejection/exercises.tex) / [Solutions](../laboratories/05-motor-load-rejection/exercise-solutions.tex) |
| 06 | [Gain selection with a third-order actuator](../laboratories/06-root-locus/README.md) | [PDF](../laboratories/06-root-locus/exercises.pdf) | [PDF](../laboratories/06-root-locus/exercise-solutions.pdf) | [Questions](../laboratories/06-root-locus/exercises.tex) / [Solutions](../laboratories/06-root-locus/exercise-solutions.tex) |
| 07 | [A feedback loop with a communication delay](../laboratories/07-delay-budget/README.md) | [PDF](../laboratories/07-delay-budget/exercises.pdf) | [PDF](../laboratories/07-delay-budget/exercise-solutions.pdf) | [Questions](../laboratories/07-delay-budget/exercises.tex) / [Solutions](../laboratories/07-delay-budget/exercise-solutions.tex) |
| 08 | [Lead-lag design for a normalized camera axis](../laboratories/08-camera-compensation/README.md) | [PDF](../laboratories/08-camera-compensation/exercises.pdf) | [PDF](../laboratories/08-camera-compensation/exercise-solutions.pdf) | [Questions](../laboratories/08-camera-compensation/exercises.tex) / [Solutions](../laboratories/08-camera-compensation/exercise-solutions.tex) |
| 09 | [PID regulation when the actuator saturates](../laboratories/09-pid-saturation/README.md) | [PDF](../laboratories/09-pid-saturation/exercises.pdf) | [PDF](../laboratories/09-pid-saturation/exercise-solutions.pdf) | [Questions](../laboratories/09-pid-saturation/exercises.tex) / [Solutions](../laboratories/09-pid-saturation/exercise-solutions.tex) |
| 10 | [Two thermal zones with one temperature measurement](../laboratories/10-observer-control/README.md) | [PDF](../laboratories/10-observer-control/exercises.pdf) | [PDF](../laboratories/10-observer-control/exercise-solutions.pdf) | [Questions](../laboratories/10-observer-control/exercises.tex) / [Solutions](../laboratories/10-observer-control/exercise-solutions.tex) |
| 11 | [Sampling can destabilize a continuous-time design](../laboratories/11-digital-control/README.md) | [PDF](../laboratories/11-digital-control/exercises.pdf) | [PDF](../laboratories/11-digital-control/exercise-solutions.pdf) | [Questions](../laboratories/11-digital-control/exercises.tex) / [Solutions](../laboratories/11-digital-control/exercise-solutions.tex) |
| 12 | [A synthetic process from identification to validation](../laboratories/12-identification-capstone/README.md) | [PDF](../laboratories/12-identification-capstone/exercises.pdf) | [PDF](../laboratories/12-identification-capstone/exercise-solutions.pdf) | [Questions](../laboratories/12-identification-capstone/exercises.tex) / [Solutions](../laboratories/12-identification-capstone/exercise-solutions.tex) |

## Reproduce and verify

Compile each source from its own directory with Tectonic or pdfLaTeX. The documents use standard mathematics, TikZ, page-layout and hyperlink packages; their diagrams need no external image files.

Run `python tools/validate_exercises.py` from the repository root for selected numerical checks and statement/solution counts. See [exercise validation](../docs/EXERCISES.md) for the evidence boundary.
