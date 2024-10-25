1. Input product price: Each 1 month:
 - 25/07 - 25/08
 - 25/08 - 25/09 
 - 25/09 - 25/10 DONE

2. Modelling assets:
- Define payoff function of the product = **QUAN**
- Model of underlying assets: Local or stochastic factors (volatility or interest rate) models 
- AND use exogeneous (option or bond) data to calibrate model parameters.

3. Simulation techniques: Generate data for 25/07 to 25/10
- Complicated models with efficient simulation (non-discretized, from research paper) 
    - Start simple: Multivariate GBM
    - Complicated: 1 each 
        - **BACH**
        - **LINH**
        - **QUAN**
- Variance reduction + comparing with and without variance reduction techniques


------ **AFTER ALL THE ABOVE ARE DONE**
4. Quantitative Analysis of the product:
- Derive prices and Greek values (???) of the product
- Accurately and efficiently, backtest at least 3 months. Consistent with the true prices = RMSE
- Analytical solution to the price of the product with at least one exotic option feature (quan giai)
 - Example: Option price 

5. Presentation:
- Explains the product well, insightful interpretation of the results.
- Insights into trading and hedging strategies with this product.
