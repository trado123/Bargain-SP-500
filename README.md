# Bargain-SP-500

## Description
This project finds the "bargains" in the S&P 500 and statistically demonstrates the profitability of the strategy.  

## Installation
This project requires Python 3.10+, as well as the `yfinance`, `numpy`, and `pandas` libraries.  

## Usage
The Python file [trailing_bargain_sp500.py](./trailing_bargain_sp500.py) prints to the terminal a list of tickers that satisfy the strategy conditions.  
The other Python file [proof_bargain_sp500.py](./proof_bargain_sp500.py) demonstrates the effectiveness of the strategy using simple statistical tools. It also generates a `.txt` file containing the results of the bootstrap analysis.  

## Limitations
The limited historical data available through the `yfinance` library (only the past 4 years) is a significant constraint for the statistical analysis. This prevents the user from being fully certain about the validity of the strategy.  

## License
This project is licensed under the Apache License. See the [LICENSE.txt](./LICENSE.txt) file for details.
