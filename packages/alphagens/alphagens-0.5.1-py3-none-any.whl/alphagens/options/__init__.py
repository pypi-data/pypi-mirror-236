import numpy as np
from scipy.stats import norm

def black_scholes(S0, K, T, r, q, sigma, option_type="call"):
    d1 = (np.log(S0 / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        C = S0 * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return C
    elif option_type == "put":
        P = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * np.exp(-q * T) * norm.cdf(-d1)
        return P
    else:
        raise ValueError("Option type must be either 'call' or 'put'")
