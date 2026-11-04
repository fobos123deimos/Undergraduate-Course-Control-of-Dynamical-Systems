r"""# Control of Dynamical Systems

An illustrated Python reference for twelve reproducible laboratories.
Each module page combines the physical equipment, signal diagram, governing
equation, computed response and the actual executable source.

![Interacting tanks](assets/interacting-tanks.png)

The common workflow is **physical balance → model → analytical prediction →
numerical experiment → evidence and limitations**. Every scenario is synthetic.
The tank illustration belongs to the separate integrated design exercises.

## Laboratory API map

| Unit | Illustrated laboratory | Entry point |
|---|---|---|
| 01 | [Thermal enclosure and sensor lag](lab01_thermal_enclosure.html) | [run](lab01_thermal_enclosure.html#run) |
| 02 | [Ventilation and local linearization](lab02_ventilation.html) | [run](lab02_ventilation.html#run) |
| 03 | [Base-excited vibration isolation](lab03_vibration_isolation.html) | [run](lab03_vibration_isolation.html#run) |
| 04 | [Passive notch filter and component tolerance](lab04_notch_filter.html) | [run](lab04_notch_filter.html#run) |
| 05 | [Motor speed and load rejection](lab05_motor_load_rejection.html) | [run](lab05_motor_load_rejection.html#run) |
| 06 | [Gain selection and the stability boundary](lab06_root_locus.html) | [run](lab06_root_locus.html#run) |
| 07 | [Feedback delay and phase reserve](lab07_delay_budget.html) | [run](lab07_delay_budget.html#run) |
| 08 | [Lead-lag compensation for a camera axis](lab08_camera_compensation.html) | [run](lab08_camera_compensation.html#run) |
| 09 | [PID saturation and back-calculation](lab09_pid_saturation.html) | [run](lab09_pid_saturation.html#run) |
| 10 | [State feedback with one thermal measurement](lab10_observer_control.html) | [run](lab10_observer_control.html#run) |
| 11 | [Sampling and closed-loop stability](lab11_digital_control.html) | [run](lab11_digital_control.html#run) |
| 12 | [Identification, held-out prediction and control](lab12_identification_capstone.html) | [run](lab12_identification_capstone.html#run) |

## First execution

```bash
python -m pip install -r requirements.txt
cd laboratories/01-thermal-enclosure
python analysis.py
```

The original scripts are preserved at their laboratory paths. Each now has
an explicit `run()` entry point and a main guard, so documentation generation
does not execute simulations, change Matplotlib settings or write results.
The same calculation still executes when the script is launched directly.
The unique `lab01_...` names identify documentation pages, not separately
installable modules. Source links point to the actual `analysis.py` files.

## Companion material

- [Course, notebooks and all twelve laboratories](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems)
- [Worked exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/problem-sets)
- [Equipment and control-diagram atlas](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/docs/DIAGRAMS.md)
- [MATLAB and Octave](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/matlab)
- [Simulink builders and their scope](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/simulink)
- [Validation evidence](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/docs/VALIDATION.md)
- [Documentation maintenance](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/docs/API_DOCUMENTATION.md)

## Reading the figures

Equipment views establish the physical meaning of variables; block diagrams
show the mathematical signal paths. Response plots are numerical evidence
under the stated assumptions. Stability checks, approximation errors and
intentional unstable cases are explained beside each plot. None of the
figures proves experimental calibration or hardware safety.

This pdoc site documents Python. MATLAB/Octave implementations, Simulink
builders and PDF derivations remain linked companion resources.
"""
