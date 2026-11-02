# Integrated problems and worked reasoning

The collection contains **65 problems with 210 linked parts**. Each of the twelve laboratories has five problems with parts (a)–(c). The general collection has five larger cases with parts (a)–(f). Separate English exercise and solution PDFs have editable LaTeX sources.

The general cases cover interacting water tanks, vibration isolation, a voltage-limited motor, camera lead-lag compensation and sampled thermal regulation. They replace the earlier collection of 31 short questions; this is a redesigned set of cases, not a one-to-one renumbering.

## How the laboratory problems changed

The ten earlier original questions in each laboratory now contribute analytical parts to five coherent scenarios. A new synthesis part connects them through feasibility, uncertainty, implementation or evidence. The [mapping record](exercise-map.json) identifies the previous question and its new location. This mapping concerns this repository's previous original edition, not third-party handouts.

Equipment illustrations appear in Problem 1 and a control structure in Problem 3. Other problems develop the scenario without a supplied figure. A solution must show intermediate reasoning and end with a justified decision. The solution PDF repeats each question and develops its answer directly underneath it.

## Verification

- The structural checks confirm five problems and fifteen worked parts in every laboratory, plus five general problems and thirty worked parts.
- The 88 retained numerical checks and 67 additional integrated checks pass. They cover independently integrated balances, finite-difference linearization, energy conservation, physical feasibility, margins, eigenvalues and fractional-delay integration.
- All revised PDFs are compiled and rendered. See [document counts and hashes](document-validation.json), [notation checks](notation-validation.json), [retained calculations](exercise-validation.json) and [new integrated calculations](integrated-validation.json).

The checks support selected claims; they are not a formal proof of every argument. Every parameter and dataset is hypothetical or synthetic. No physical measurements are asserted.

## Reproduction

Run the four validation programs listed in the root README after installing the Python requirements. Compile each TeX source from its own directory. Keep the repository directory structure: shared illustrations are included by relative paths. No third-party images are required.

The repository workflow runs these checks alongside the existing Python notebook and GNU Octave checks. MATLAB/Simulink runtime limitations remain documented in [validation](VALIDATION.md).
