# Illustration review — 19 November 2026

The photorealistic tank scene and its technical counterpart now use the same process topology: an external supply feeds the pump, the pump enters tank 1 from above, the submerged connection permits flow between tanks, and only tank 2 drains externally. Heights refer to the ideal common hydraulic outlet datum. The README and the site opening share the photorealistic view; the internal gallery and laboratory pages retain technical illustrations.

Labels were grouped into aligned bands or clear margins, with short leaders to the intended component. Tank labels no longer cover the water levels; circuit labels leave terminals and signal paths visible. The detailed equations remain editable TikZ.

| View | Physical and visual review |
|---|---|
| Thermal enclosure | Separated heater, sensor and heat-loss labels; retained the distinct thermal-storage and sensor-lag states. |
| Ventilation | Replaced misleading heater/flame imagery with a tracer emitter. Room and liquid analogue remain separate, with their own volume units. |
| Vibration isolation | Removed the prism/iris obstruction and oriented the receiver toward the optical source. Two springs and one damper remain in parallel between payload and foundation. |
| RLC filter | Used an enclosed nonpolar capacitor and an unbanded resistor. The positive probe lead is at the R/L junction and the negative lead at the capacitor return: the output spans L + C. |
| Motor and flywheel | Clarified combined rotating inertia and the actual bearing location; retained the shaft-centered rotation indication and opposing load brake. |
| Positioning actuator | Attached the encoder readhead to the moving carriage and retained the fixed scale; distinguished the lead screw from the carriage/nut. |
| Communication delay | Separated measurement and command paths; the return command terminates at the stage motor. |
| Camera axis | Removed the extra rigid support that obstructed the indicated rotational freedom. Raised the target to the camera direction. The angle marks mechanical orientation, not a ray through the pivot. |
| Saturating actuator | Moved mass, spring and damping labels off the components; retained the applied-force and displacement directions. |
| Two thermal zones | Grouped capacities, losses and coupling labels above the equipment; kept heating in zone 1 and measurement in zone 2. |
| Sampled RC process | Used an enclosed nonpolar capacitor and an unbanded resistor; completed the ADC common-reference terminal and connection. The dashed loop represents sampled data and commands, with an explicit digital controller. |
| Identification experiment | Moved the fluid-state label off the stirrer; showed equal inlet/outlet flow q and the remote measurement after transport. |
| Interacting tanks | Removed the false pipe from the motor rear, added the pump suction hose in both styles, and kept levels, valves and intertank connection unobstructed. |

These are conceptual illustrations of the stated models. Geometric dimensions, component construction and decorative instrument displays do not identify additional model parameters. Numerical simulation sources and mathematical control diagrams were not changed by this review.
