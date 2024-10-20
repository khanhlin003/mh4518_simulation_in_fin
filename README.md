# MH4518: Simulation Techniques in Finance - Barrier Reverse Convertible Analysis

Welcome to our repository dedicated to the simulation and pricing of Barrier Reverse Convertible (BRC) products. Here, we focus on analyzing and modeling the 7% p.a. CHF Barrier Reverse Convertible linked to Roche, Richemont, and Zurich stocks.

## Featured Product Analysis

Our primary focus is on a specific structured product:

1. **7% p.a. CHF Barrier Reverse Convertible on Roche, Richemont, Zurich**
   - Coupon: 7% p.a., paid quarterly
   - Barrier: 60% of initial fixing, continuously observed
   - Term: 15 months
   - Currency: CHF
   - Issuer: Credit Suisse AG, London Branch

For detailed product specifications, please refer to the product factsheet in the `docs` directory.

## Modeling and Simulation of Underlying Assets

We implement various models to simulate the behavior of the underlying stocks:

* **Geometric Brownian Motion (GBM)**: Basic model for stock price movements
* **Heston Stochastic Volatility Model**: Captures dynamic volatility of the stocks
* **Correlation Matrix Estimation**: Models the interdependence between Roche, Richemont, and Zurich stocks

## Pricing Methodology

Our repository includes implementations of various pricing methods:

* **Monte Carlo Simulation**: For path-dependent barrier feature
* **Finite Difference Method (FDM)**: Solves the multi-dimensional PDE for the BRC
* **Analytical Approximations**: Quick estimations using closed-form solutions where applicable

## Risk Metrics and Sensitivity Analysis

We compute and analyze key risk metrics:

* **Greeks**: Delta, Gamma, Vega, Theta for each underlying stock
* **Barrier Probabilities**: Estimation of barrier hit probabilities
* **Scenario Analysis**: Product behavior under various market conditions

## Data Analysis and Backtesting

Our analysis includes:

* **Historical Data Analysis**: Performance of Roche, Richemont, and Zurich stocks
* **Backtesting**: Simulating historical performance of similar BRC products
* **Dividend Modeling**: Incorporating historical and projected dividends

## Visualization Tools

We provide tools for visualizing:

* **Payoff Diagrams**: Interactive plots showing product payoff at maturity
* **Stock Price Simulations**: Visual representation of Monte Carlo paths
* **Sensitivity Surfaces**: 3D plots of product value against various parameters

## Contributing

We welcome contributions that enhance our BRC analysis or introduce new relevant models. Please refer to our contribution guidelines for more information.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
