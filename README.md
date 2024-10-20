# MH4518: Simulation Techniques for Barrier Reverse Convertibles

Welcome to our repository dedicated to the simulation and pricing of Barrier Reverse Convertible (BRC) derivatives. Here, we explore various models and methods to price these complex structured products effectively.

## Overview of Barrier Reverse Convertibles

Barrier Reverse Convertibles (BRCs) are structured products that offer a fixed coupon payment and conditional capital protection. Our simulations focus on:

1. **Single Asset BRCs**: Linked to one underlying asset.
2. **Multi-Asset BRCs**: Linked to a basket of underlying assets.

## Key Features Modeled

Our simulations capture the essential features of BRCs:

* Fixed coupon payments
* Continuous or end-of-term barrier observation
* Potential for capital loss based on worst-performing asset

## Modeling and Simulation of Underlying Assets

We incorporate various asset models to ensure robust BRC pricing:

* **Geometric Brownian Motion (GBM)**: The foundational model for asset price simulation.
* **Heston Stochastic Volatility Model**: Captures dynamic volatility of underlying assets.
* **Jump-Diffusion Models**: Incorporates sudden price movements.

Each model is simulated under various scenarios, considering effects of dividends and correlation between multiple assets.

## Pricing Methods

We utilize several numerical techniques for BRC valuation:

* **Monte Carlo Simulation**: For path-dependent barrier features.
* **Finite Difference Method (FDM)**: To solve partial differential equations for option components.
* **Analytical Approximations**: For quick pricing under simplified assumptions.

## Sensitivity Analysis and Greeks

We compute key sensitivities to understand BRC price dynamics:

* **Delta (δ)**: Rate of change in BRC price relative to underlying asset price.
* **Gamma (Γ)**: Second-order price sensitivity to underlying asset movements.
* **Vega (ν)**: Sensitivity to volatility changes.
* **Theta (θ)**: Time decay of the BRC value.

## Risk Assessment

Our models provide comprehensive risk metrics:

* **Value at Risk (VaR)**: Estimating potential losses.
* **Expected Shortfall**: Assessing tail risk.
* **Scenario Analysis**: Testing BRC performance under various market conditions.

## Data Analysis and Backtesting

We focus on empirical testing and validation:

* **Historical Simulation**: Backtesting BRC performance using historical data.
* **Stress Testing**: Evaluating BRC behavior under extreme market scenarios.

## Contributing

We welcome contributions that enhance our BRC simulations or introduce new relevant models. Please refer to our contribution guidelines for more information.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
