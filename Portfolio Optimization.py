from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage


from pypfopt.risk_models import sample_cov
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


def pfopt(df, amount):
    mu = mean_historical_return(df)
    S = CovarianceShrinkage(df).ledoit_wolf()
    
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    
    projection = ef.portfolio_performance(verbose=True)
    
    latest_prices = get_latest_prices(df)
    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=amount)
    allocation, leftover = da.greedy_portfolio()
    
    return allocation
    print(allocation, projection)

