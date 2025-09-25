# Bargain-S&amp;P-500
# Description
This project consist in two different programs:
- the first one [trailing_bargain_sp500.py](./trailing_bargain_sp500.py) spots the companies that satisfy the criteria of being "bargain" in a trimestral timespan.
- the other part is to prove, via [proof_bargain_sp500.py](./proof_bargain_sp500.py), that those companies are actually more profitable than the others.
# Trailing Bargain S&P 500
This python file examines all the S&amp;P 500 tickers' trimester balance sheet and trimester income statement.    
It gives back a list containing the companies which pass the test and it is shown to the terminal.
## Requirements
- Python 3.9+  
- Libraries:  
```bash
pip install yfinance pandas requests
```
## Usage  
Clone the repository and run:
```bash
python trailing_bargain_sp500.py
```
You will see in the terminal the tickers' list
# Proof Bargain S&P500

This part of the project implements a statistical test to verify the **Deep Value Investing** hypothesis applied to the S&P 500 index.  
Specifically, it evaluates whether companies classified as "bargain" (i.e. with **market value < equity** and **EPS > 0**) have achieved significantly different returns compared to non-"bargain" companies in recent years.

## Main Features
- **Extract S&P 500 tickers** from Wikipedia  
- **Fetch market and financial statement data** via `yfinance`  
- **Build a table for each ticker** with:  
  - annual financial statement dates  
  - percentage change in price compared to the following year  
  - result of the "deep value" test (True/False)  
- **Statistical analysis**:  
  - mean returns for bargain vs non-bargain groups  
  - bootstrap with 10,000 samples to estimate confidence interval  
  - probability that the observed difference is > 0  
- **Outputs results** in a `proof.txt` file  
## Requirements
- Python 3.9+  
- Libraries:  
```bash
pip install yfinance numpy pandas requests
```
## Usage
Clone the repository and run:
```bash
python proof_bargain_sp500
```
It generates a file contining the statistical results called `proof.txt`. The process will take at least 4 minutes, so the repository already contains that file.
## Limitations
The limited historical data available through the `yfinance` library (only the past 4 years) is a significant constraint for the statistical analysis.  
This prevents the user from being fully certain about the validity of the strategy.  
## Result's Discussion
The user familiar whith statistics can run more tests with the lists collected in the function get proof. You will find out that the study loses statistical power due to the high value of I^2 found during a random-effects (DerSimonian–Laird) analysis over the tree different years.  
In different terms, the eterogenety of the tree years inficiates a lot a comparative analysis.
## License
This project is licensed under the Apache License. See the [LICENSE.txt](./LICENSE.txt) file for details.
