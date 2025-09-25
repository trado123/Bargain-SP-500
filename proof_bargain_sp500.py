# Costruisce una tabella per ogni ISIN con una riga per le date, una con il delta di prezzo rispetto all'anno successivo
# E una con la condizione di quell'anno di bargain (True or False)
import yfinance
import numpy as np
import pandas as pd
import requests
from io import StringIO


def get_list_sp500(): # estrae da wikipedia la lista di tutti gli ISIN che figurano nell'SP500
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    tables = pd.read_html(StringIO(response.text))
    sp500_table = tables[0]
    tickers = sp500_table["Symbol"].tolist()
    return tickers


def date_retriver(mkt, date):  # trova la data più vicina, dove ci sono prezzi di mercato, alla pubblicazione dell'esercizio
    i = 30
    while i > 0:
        try:
            i = i - 1
            p = mkt.loc[date]
            return date
        except KeyError:
            date_list = list(date)
            days = str(int(date[8:10]) - 1)
            days_list = list(days)
            date_list = date_list[0:8] + days_list
            date = "".join(date_list)
    return "NaN"


def deep_value_test_fun(ISIN, y):  # effettua il test deep_value e restituisce dtype=bool
    try:
        data = yfinance.Ticker(ISIN)
        bal_she = data.balancesheet[y]
        inc_stmt = data.incomestmt[y]
        total_equity = bal_she["Stockholders Equity"]
        total_shares = data.info["sharesOutstanding"]
        y = date_retriver(date=y, mkt=data.history(period="6y"))
        price = data.history(period="6y").loc[y]["Close"]
        market_value = price * total_shares
        eps = inc_stmt["Diluted EPS"]
        return bool(eps > 0 and market_value < total_equity)
    except KeyError:
        print("Error")
        return False


def get_deltas(ISIN):  # resitisce i delta% dell'anno 2024-2023 2023-2022 2022-2021
    dat = yfinance.Ticker(ISIN)
    h = dat.history(period="6y")["Close"]
    dates_list = dat.balance_sheet.columns
    mkt_prices = []
    for i in range(len(dates_list)):
        date = date_retriver(mkt=h, date=str(dates_list[i])[0:10])
        p = h.loc[date]
        mkt_prices.append(p)  # il primo prezzo è del 2024, l'ultimo è del 2020

    dates_list = np.array(dates_list)
    mkt_prices = np.array(mkt_prices)
    deltas = ["NaN"]
    for i in range(len(mkt_prices) - 1):
        diff = mkt_prices[i] - mkt_prices[i + 1]
        diff = diff / mkt_prices[i + 1]
        deltas.append(diff)
    deltas = np.array(deltas)  # abbiamo 2024-2023 2023-2022 2022-2021 2021-2020
    return deltas[1:4]


def get_dates(ISIN):  # restituisce la lista con le date di pubblicazione del bilancio annuale
    dat = yfinance.Ticker(ISIN)
    dates_list = dat.balance_sheet.columns
    dates = []
    for d in dates_list:
        dates.append(str(d)[0:10])
    return dates[1:4]


def deep_value_list_fun(ISIN):  # resistuisce una lista con il deep_value_test_fun applicato su 2023,2022,2021
    dates = get_dates(ISIN)
    bool_list = []
    for d in dates:
        bool_list.append(deep_value_test_fun(ISIN, d))
    return np.array(bool_list)


def get_table(ISIN):  # resituisce la tabella con le seguenti entrate: anno,delta(rispetto all'anno successivo),bool di deep_value
    dates = get_dates(ISIN)
    deltas = get_deltas(ISIN)
    bools = deep_value_list_fun(ISIN)
    table = np.stack([dates, deltas, bools])
    return table


def get_proof(): # genera il file 'proof.txt' in cui  vi sono informazioni statistiche sulla validità del test
    """
    Calcola in media quanto guadgna l'azione con una condizione di TRUE e quanto con una di FALSE
    per vedere se ci sono differenze tra i due valori.
    """
    list_24_23_T = []
    list_23_22_T = []
    list_22_21_T = []
    list_24_23_F = []
    list_23_22_F = []
    list_22_21_F = []
    list = get_list_sp500()
    e = 0
    p = 0
    for isin in list:
        p += 1
        print("Stock analyzed:", p)
        try:
            t = get_table(isin)
            if (t[0][0])[0:4] == "2023" and t[2][0] == "False":
                list_24_23_F.append(float(t[1][0]))
            elif (t[0][0])[0:4] == "2023" and t[2][0] == "True":
                list_24_23_T.append(float(t[1][0]))
            if (t[0][1])[0:4] == "2022" and t[2][1] == "False":
                list_23_22_F.append(float(t[1][1]))
            elif (t[0][1])[0:4] == "2022" and t[2][1] == "True":
                list_23_22_T.append(float(t[1][1]))
            if (t[0][2])[0:4] == "2021" and t[2][2] == "False":
                list_22_21_F.append(float(t[1][2]))
            elif (t[0][2])[0:4] == "2021" and t[2][2] == "True":
                list_22_21_T.append(float(t[1][2]))
        except (KeyError, IndexError, ValueError):
            e += 1
    sum = 0
    mean = 0
    for x in list_24_23_F:
        sum += float(x)
        mean = sum / len(list_24_23_F)
    mean2423F = mean
    sum = 0
    mean = 0
    for x in list_24_23_T:
        sum += float(x)
        mean = sum / len(list_24_23_T)
    mean2423T = mean
    sum = 0
    mean = 0
    for x in list_23_22_F:
        sum += float(x)
        mean = sum / len(list_23_22_F)
    mean2322F = mean
    sum = 0
    mean = 0
    for x in list_23_22_T:
        sum += float(x)
        mean = sum / len(list_23_22_T)
    mean2322T = mean
    sum = 0
    mean = 0
    for x in list_22_21_F:
        sum += float(x)
        mean = sum / len(list_22_21_F)
    mean2221F = mean
    sum = 0
    mean = 0
    for x in list_22_21_T:
        sum += float(x)
        mean = sum / len(list_22_21_T)
    mean2221T = mean

    # eseguo il bootstrap
    strategy = np.array(list_22_21_T + list_23_22_T + list_24_23_T)
    control = np.array(list_22_21_F + list_23_22_F + list_24_23_F)
    obs_diff = np.mean(strategy) - np.mean(control)
    n_boot = 10000
    boot_diffs = []
    rng = np.random.default_rng(seed=0)
    for _ in range(n_boot):
        boot_strat = rng.choice(strategy, size=len(strategy), replace=True)
        boot_ctrl = rng.choice(control, size=len(control), replace=True)
        boot_diffs.append(np.mean(boot_strat) - np.mean(boot_ctrl))
    boot_diffs = np.array(boot_diffs)
    p_positive = np.mean(boot_diffs > 0)
    ci_lower, ci_upper = np.percentile(boot_diffs, [2.5, 97.5])
    u = 3

    #scrivo su file
    f = open(file="proof.txt", mode="w")
    f.write(f"Strategy mean during 2023 (number of observations = {len(list_24_23_T)}):" + " " + str(round(mean2423T*100, u))+"%")
    f.write("\n")
    f.write(f"Control mean during 2023 (number of observations = {len(list_24_23_F)}):" + " " + str(round(mean2423F*100, u))+"%")
    f.write("\n")
    f.write("\n")
    f.write(f"Strategy mean during 2022(number of observations = {len(list_23_22_T)}):" + " " + str(round(mean2322T*100, u))+"%")
    f.write("\n")
    f.write(f"Control mean during 2022(number of observations = {len(list_23_22_F)}):" + " " + str(round(mean2322F*100, u))+"%")
    f.write("\n")
    f.write("\n")
    f.write(f"Strategy mean during 2021(number of observations = {len(list_22_21_T)}):" + " " + str(round(mean2221T*100, u))+"%")
    f.write("\n")
    f.write(f"Control mean during 2021(number of observations = {len(list_22_21_F)}):" + " " + str(round(mean2221F*100, u))+"%")
    f.write("\n")
    f.write("\n")
    f.write(f"Observed mean difference: {obs_diff*100:.3f}"+"%")
    f.write("\n")
    f.write(f"Difference probability > 0: {p_positive*100:.3f}"+"%")
    f.write("\n")
    f.write(f"95% confidence interval bootstrap: [{ci_lower*100:.4f}%, {ci_upper*100:.4f}%]")
    f.close()


if __name__ == "__main__":
    get_proof()
