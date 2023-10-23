import pytz
from datetime import datetime
import numpy as np
import scipy.stats as si
import math
from d2y.enums import *
from functools import cache


@cache
def calculate_option_price(S, K, T, r, sigma, option_type: OptionType):
    """
    Calculate the price of a European option using the Black-Scholes model.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.
    option_type (OptionType): The type of the option (either 'CALL' or 'PUT').

    Returns:
    float: The calculated price of the option.
    """

    T = (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )
    d1 = black_scholes_d1(S, K, T, r, sigma)
    d2 = black_scholes_d1(S, K, T, r, sigma) - sigma * math.sqrt(T)

    if option_type == OptionType.CALL:
        option_price = S * si.norm.cdf(d1) - K * math.exp(-r * T) * si.norm.cdf(d2)
    elif option_type == OptionType.PUT:
        option_price = K * math.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type")

    return option_price


@cache
def calculate_time_to_expiry(T):
    """
    Calculate the time to expiry of an option in years.

    Parameters:
    T (datetime): Expiry date of the option.

    Returns:
    float: The time to expiry of the option in years.
    """
    return (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )


@cache
def newton_raphson_volatility(
    S, K, T, r, C, option_type, sigma_est=0.6, tol=1e-3, max_iter=50
):
    """
    Estimate the volatility of the underlying asset using the Newton-Raphson method.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    C (float): Option's market price.
    option_type (OptionType): The type of the option (either 'CALL' or 'PUT').
    sigma_est (float): Initial estimate of the volatility.
    tol (float): Tolerance for the convergence of the method.
    max_iter (int): Maximum number of iterations.

    Returns:
    float: Estimated volatility of the underlying asset.
    """
    if not C:
        print("No call price given!")
        C = calculate_option_price(S, K, T, r, 1, option_type)

    for _ in range(max_iter):
        f_val = calculate_option_price(S, K, T, r, sigma_est, option_type) - C
        vega_val = black_scholes_vega(S, K, T, r, sigma_est)

        if abs(f_val) < tol:
            return sigma_est

        # return if vega is too small
        if vega_val < 1e-10:
            break

        sigma_est -= f_val / vega_val

    print(f"Failed to converge after {max_iter} iterations")
    return None


# Calculate d1 using the Black-Scholes formula
@cache
def black_scholes_d1(S, K, T, r, sigma):
    """
    Calculate the 'd1' term in the Black-Scholes model.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.

    Returns:
    float: 'd1' term in the Black-Scholes model.
    """
    return (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))


# Calculate d2 using the Black-Scholes formula
@cache
def black_scholes_d2(S, K, T, r, sigma):
    """
    Calculate the 'd2' term in the Black-Scholes model.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.

    Returns:
    float: 'd2' term in the Black-Scholes model.
    """
    return black_scholes_d1(S, K, T, r, sigma) - sigma * math.sqrt(T)


# Calculate delta using the Black-Scholes formula
@cache
def black_scholes_delta(S, K, T, r, sigma, option_type: OptionType):
    """
    Calculate the delta of the option using the Black-Scholes formula.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.
    option_type (OptionType): The type of the option (either 'CALL' or 'PUT').

    Returns:
    float: Delta of the option.
    """
    T = (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == OptionType.CALL:
        delta = si.norm.cdf(d1)
    elif option_type == OptionType.PUT:
        delta = si.norm.cdf(d1) - 1
    else:
        raise ValueError("option_type must be either 'call' or 'put'")

    return delta


# Calculate vega using the Black-Scholes formula
@cache
def black_scholes_vega(S, K, T, r, sigma):
    """
    Calculate the vega of the option using the Black-Scholes formula.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.

    Returns:
    float: Vega of the option.
    """
    T = (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )
    # if K == 2000 and T > 0.1:
    #     print(f"S: {S}, K: {K}, T: {T}, r: {r}, sigma: {sigma}")
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S * si.norm.pdf(d1) * np.sqrt(T)

    return vega


# Calculate gamma using the Black-Scholes formula
@cache
def black_scholes_gamma(S, K, T, r, sigma):
    """
    Calculate the gamma of the option using the Black-Scholes formula.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.

    Returns:
    float: Gamma of the option.
    """
    T = (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))

    return gamma


# Calculate rho using the Black-Scholes formula
@cache
def black_scholes_rho(S, K, T, r, sigma, option_type: OptionType):
    """
    Calculate the rho of the option using the Black-Scholes formula.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.
    option_type (OptionType): The type of the option (either 'CALL' or 'PUT').

    Returns:
    float: Rho of the option.
    """
    T = (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == OptionType.CALL:
        rho = K * T * np.exp(-r * T) * si.norm.cdf(d2)
    elif option_type == OptionType.PUT:
        rho = -K * T * np.exp(-r * T) * si.norm.cdf(-d2)
    else:
        raise ValueError("option_type must be either 'call' or 'put'")

    return rho


# Calculate theta using the Black-Scholes formula
@cache
def black_scholes_theta(S, K, T, r, sigma, option_type: OptionType):
    """
    Calculate the theta of the option using the Black-Scholes formula.

    Parameters:
    S (float): Underlying asset's current market price.
    K (float): Option's strike price.
    T (datetime): Expiry date of the option.
    r (float): Risk-free interest rate.
    sigma (float): Underlying asset's volatility.
    option_type (OptionType): The type of the option (either 'CALL' or 'PUT').

    Returns:
    float: Theta of the option.
    """
    T = (T - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() / (
        24 * 60 * 60 * 365
    )
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == OptionType.CALL:
        theta = (-S * si.norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - (
            r * K * np.exp(-r * T) * si.norm.cdf(d2)
        )
    elif option_type == OptionType.PUT:
        theta = (-S * si.norm.pdf(d1) * sigma / (2 * np.sqrt(T))) + (
            r * K * np.exp(-r * T) * si.norm.cdf(-d2)
        )
    else:
        raise ValueError("option_type must be either 'call' or 'put'")

    return theta
