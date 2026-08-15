# Rocket Launch Simulator & Optimizer

A Python physics simulator that models the flight of an air-powered rocket, predicting trajectory, stability, and range — paired with a Monte Carlo optimizer that searches thousands of design configurations to find the best rocket setup for a given goal (e.g., max range, lowest cost, highest speed).

Built as a follow-up to a physical air-powered rocket launcher project, to predict and optimize performance computationally rather than through trial and error alone.

## Features

- **Trajectory simulation** using Euler's method, including angle-of-attack effects
- **Stability analysis** via the Barrowman equations, calculating center of pressure vs. center of gravity, with fin-body interference correction
- **Component-based drag modeling** — nose cone, body, and fins modeled separately using empirical aerodynamic coefficients, skin friction (Schlichting's formula), and Sutherland's law for air viscosity
- **Barrel launch physics** — models pressure, friction (Darcy-Weisbach equation), and seal losses during the launch phase
- **Monte Carlo optimizer** — tests 1,000+ configurations against range, height, speed, and cost constraints under realistic parameter bounds
- **Trajectory and angle-of-attack plotting** for visualizing flight results

## How to run

Requires: `numpy`, `matplotlib` *(update this list to match what you actually import)*

## Model validation

Model accuracy was iteratively tuned by comparing predicted range against real launch data (~30m actual range). Early versions predicted 47.7m; after refining barrel friction, seal losses, boat tail geometry, and drag modeling, predictions converged to 37.35m — with the stability margin (3.29) correctly matching the stable flight observed in real testing.

## Known limitations

- 2D trajectory only (no lateral wind effects)
- Assumes manufacturing perfection (no shot-to-shot variability)
- Empirical drag/friction coefficients used in place of full CFD or experimental measurement
