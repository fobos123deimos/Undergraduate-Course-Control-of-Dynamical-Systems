# Programmatically generated Simulink models

Run `addpath('simulink'); build_models` in MATLAB with Simulink. The script generates and simulates six nominal `.slx` models using standard blocks, then saves them under `generated/`.

The default call refuses to overwrite an existing output. To deliberately replace saved generated files, call `build_models(true)`. An already loaded model always stops generation: save and close it yourself first. All six names are checked before the first model is created. The GitHub Octave job checks that the function parses and exposes one optional argument; this does not run or validate Simulink.

| Model | Input | Output | Interpretation |
|---|---|---|---|
| Thermal sensor | Incremental heat, W | Indicated temperature rise, K | Includes the 12 s sensor lag; use step amplitude 40 for the laboratory. |
| Ventilation local | Incremental airflow, m³/min | Incremental excess concentration, ppm | Local small-signal model; add 120 ppm for absolute excess concentration. |
| Platform floor | Floor displacement, m | Absolute platform displacement, m | Base-excitation transfer with damping ratio 0.08. |
| Passive notch | Source voltage, V | Voltage across L + C, V | Ideal unloaded RLC model. |
| Motor voltage | Armature voltage, V | Angular speed, rad/s | Open-loop motor without the load input. |
| Root locus K12 | Normalized reference | Normalized output | Already closed-loop with K=12; do not close it a second time. |

Default inputs are unit steps. Scale them to the stated laboratory experiment and respect local-linearization limits. These are nominal input-output realizations, not complete hardware rigs or Simscape networks. Nonlinear saturation, observers, identification and sampled control are implemented in the Python and MATLAB/Octave material.

No generated `.slx` file is claimed unless the generator actually runs in a licensed installation. GNU Octave cannot execute Simulink. See [validation](../docs/VALIDATION.md).
