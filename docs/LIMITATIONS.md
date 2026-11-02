# Model and evidence limitations

- Every numerical parameter is a chosen teaching value, and every generated dataset is synthetic. There are no bench measurements in this collection.
- Thermal and ventilation models assume spatial mixing and constant coefficients. The tracer example is not an exposure assessment.
- Mechanical and electrical models omit real friction, parasitics, travel limits and component loading unless explicitly introduced.
- Motor PI and state feedback assume nominal parameters and ideal sensing; the PID experiment introduces saturation deliberately.
- Delay plots use a stated Pade approximation, while the capstone uses a discrete delay buffer. They are different approximations with different purposes.
- Digital stability depends on the exact update order in the assignment.
- Identification uses independently generated excitation records but still the same declared synthetic plant class. It is not validation of real equipment.
- Numerical assertions check selected mathematical invariants and outcomes. They are not formal proofs of all derivations or guarantees of physical safety.
- MATLAB and Simulink execution require their proprietary runtimes; availability of their source files is not proof they were executed.
