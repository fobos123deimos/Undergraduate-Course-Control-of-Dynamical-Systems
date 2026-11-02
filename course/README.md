# Learning path and prerequisite map

[Course guide PDF](guide.pdf) · [Editable LaTeX](guide.tex) · [Exercise collections](../problem-sets/README.md)

The sequence progresses from physical modeling to feedback design, state estimation, sampled implementation and evidence assessment. Difficulty is cumulative rather than strictly increasing question by question: review items consolidate earlier ideas, and clearly identified return tasks preview later methods.

## Entry knowledge

Use elementary differential equations, complex arithmetic, derivatives, matrix multiplication/eigenvalues and basic Python. Learn Laplace transforms and transfer functions before the sensor calculation in 01. Basic variance and independent errors are needed for 01 Problem 4(b); least squares and the chi-square reference distribution are needed for 12 Problems 2--3. These statistical parts can be completed on a second pass.

## Module sequence

| Module | Entry knowledge / earlier modules | New demand | Readiness check |
|---|---|---|---|
| [01-thermal-enclosure](../laboratories/01-thermal-enclosure/README.md) | Elementary ODEs, units and Laplace transforms | Physical state versus sensor lag and stored energy | Noise propagation in Problem 4(b) also uses independent-error variance. |
| [02-ventilation](../laboratories/02-ventilation/README.md) | 01 and partial derivatives | Local approximation versus nonlinear operating points | First solve 1--3 and 5(b); return to 4 and 5(a,c) after 05, with actuator limits revisited after 09. |
| [03-vibration-isolation](../laboratories/03-vibration-isolation/README.md) | Second-order ODEs and complex frequency response | Base excitation, resonance, travel and energy | Connect each transfer function to the actual input location. |
| [04-notch-filter](../laboratories/04-notch-filter/README.md) | 03 and basic circuit laws | Measured voltage, zeros, tolerance and passivity | Problem 5 previews state models; the full feedback treatment is in 10. |
| [05-motor-load-rejection](../laboratories/05-motor-load-rejection/README.md) | 01--04 and P/PI feedback definitions | Tracking, load rejection and supply feasibility | Return to 4(a,c) after Routh analysis in 06, and 1(b) after controllability in 10. |
| [06-root-locus](../laboratories/06-root-locus/README.md) | 05 and characteristic polynomials | Algebraic stability and gain-selection limits | Do not replace a stability proof with a short time-response plot. |
| [07-delay-budget](../laboratories/07-delay-budget/README.md) | 03--04 frequency response and 06 stability | Phase margins, pure delays and sensor dynamics | Learn gain crossover and phase margin before estimating a delay budget. |
| [08-camera-compensation](../laboratories/08-camera-compensation/README.md) | 06--07 and steady tracking errors | Simultaneous tracking, phase and noise requirements | Recheck all requirements after adding the lag section. |
| [09-pid-saturation](../laboratories/09-pid-saturation/README.md) | 05--06 and numerical ODEs | Derivative filtering, saturation and anti-windup | Compare actual actuator effort as well as requested effort. |
| [10-observer-control](../laboratories/10-observer-control/README.md) | 04--05 state models, eigenvalues and 09 actuator limits | State feedback, estimation and implementation assumptions | Derive the full-state result before introducing the observer. |
| [11-digital-control](../laboratories/11-digital-control/README.md) | 05 PI control, 10 state models and difference equations | Sampling stability and software update order | Specify the held input and integrator update order first. |
| [12-identification-capstone](../laboratories/12-identification-capstone/README.md) | 02, 05, 07, 09, 11 and basic probability/least squares | Identification, independent validation and fractional delays | The chi-square interval in 3(c) needs a probability refresher. |

## First pass versus return tasks

- **02:** first complete Problems 1--3 and 5(b). Return to 4 and 5(a,c) after 05. Reconsider integral action under limits after 09.
- **05:** begin with Problems 1(a,c), 2, 3, 4(b) and 5. Use 06 before completing the Routh items 4(a,c); use 10 before completing the controllability preview 1(b).
- **01 Problem 4(b) and 12 Problem 3(c):** complete the elementary probability prerequisites before drawing conclusions from the noise calculations.
- **10:** first perform full-state calculations, then introduce estimated-state feedback. Keep saturation and bias separate from the nominal linear theorem.
- **11:** specify the controller update order before calculating poles; use all real second-order Jury conditions, not a few sampled periods.

## Five general cases: recommended order

Problem numbers identify stable references, not increasing difficulty. A more accessible first pass is **2 → 1 → 3 → 4 → 5**.

| Case | Start after | Main integration |
|---|---|---|
| 2: optical isolation | 03 (04 reinforces frequency interpretation) | Modeling, vibration/travel limits, sag and energy |
| 1: interacting tanks | 02, 05 and 06 | Nonlinear balances, local PI stability and pump limits |
| 3: motor servo | 05 and 06; use 09 for anti-windup discussion | Reduced/full models, power, load rejection and implementation |
| 4: camera tracking | 07--08 | Compensation, tracking, delay reserve and actuator noise |
| 5: thermal regulation | 09--11 | Physical state model, observer, saturation and exact sampled feedback |

After 12, revisit the validation-plan items in all five cases. A simulated result is never a physical measurement.

## How to decide whether to move on

Before opening the solution, identify the input, output, units, initial condition and model boundary. Derive at least one quantitative prediction. Then run the notebook and reconcile discrepancies. Move on when you can explain the model's limitation and the design decision without relying only on a plot or a passing assertion.

External method references and bilingual video links are in the [reference catalog](../docs/REFERENCES.md).
