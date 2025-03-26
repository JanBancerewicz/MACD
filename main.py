import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# wybór danych - APPLE rosnie w okresie czasu, NESN w miare stabilnie w okresie czasu, ALEP - podupada w okresie czasu
datachoice=2 # 0 - AAPL, 1 - NESN, 2 - ALEP

datanames = ["AAPL", "NESN", "ALEP"]
datacurrency = ["USD", "CHF", "PLN"]
inputpaths = ["./data/AAPL.csv", "./data/NESN.csv", "./data/ALEP.csv"]
path = inputpaths[datachoice]
storage_path = "./diagrams/"

data = pd.read_csv(path)

#conversion to datetime.date
data["Data"] = pd.to_datetime(data["Data"], errors='coerce', dayfirst=True)
data["Data"] = data["Data"].dt.date

for item in ["Zamkniecie","Otwarcie","Max.","Min."]: # nazwy kolumn
    data[item] = data[item].str.replace(',', '.')
    data[item] = pd.to_numeric(data[item])

data = data.head(1000) #testujemy na 1000 pierwszych danych

prices = data["Zamkniecie"].values
timestamps = data["Data"].values
# print(timestamps)

short_period = 12
long_period = 26
signal_period = 9

def EMA(prices, N): # implementacja EMA
    alpha = 2 / (N + 1)
    ema_result = [prices[0]]
    for i in range(1, len(prices)):
        ema_i = alpha * prices[i] + (1 - alpha) * ema_result[-1]
        ema_result.append(ema_i)
    return ema_result

ema_short = EMA(prices, short_period)
ema_long = EMA(prices, long_period)

macd = np.array(ema_short) - np.array(ema_long) # implementacja macd
signal = EMA(macd, signal_period) # implementacja signal

# from_pandas = data["Zamkniecie"].ewm(span=26).mean()
# # for i in range(len(from_pandas)):
# #     print(from_pandas[i] - ema_long[i])
# # # porownanie z gotowa funkcja pandas <-> wyniki sa takie same

def calculate_points(macd_v, signal_v, start=0, end=1000):
    if end > len(macd_v):
        end = len(macd_v)

    macd = macd_v[start:end]
    signal = signal_v[start:end]

    buy_points = []  # przeciecie od dolu
    sell_points = []  # przeciecie od dolu

    for i in range(1, len(macd)):
        if macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:  # przeciecie od dolu
            buy_points.append(i)
        elif macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:  # przeciecie od gory
            sell_points.append(i)
    # przeciecia beda w nastepnym dniu
    return buy_points, sell_points

#INFO: symulacje mozna zrobic dla poszczegolnych przedzialow czasowych,
# ale sygnaly kupna i sprzedazy sa obliczane dla calosci danych, tylko w nich bedzemy kupowac / sprzedawac akcje w całości
def simulation(prices_v, macd_v, signal_v, start=0, end=1000):
    if end > len(macd_v):
        end = len(macd_v)

    buy_points, sell_points = calculate_points(macd_v, signal_v, start, end)
    prices = prices_v[start:end]

    money = 1000  # poczatkowy kapital, zakładajac walutę w której są ceny akcji
    stocks = 0

    # tabele będą miały tyle elementów jaki jest przedział
    wallet = []
    actions = []
    transactions = []

    for i in range(len(prices)-1):
        if i in buy_points:
            if money > 0:
                stocks_buying_val = money / prices[i]
                stocks += stocks_buying_val
                # money -= stocks * prices[i]
                transactions.append((money, 'buy'))
                money = 0
        elif i in sell_points:
            if stocks > 0:
                money_selling_val = round(stocks * prices[i], 2)
                money += money_selling_val
                stocks = 0
                transactions.append((money, 'sell'))
        actions.append(stocks) # w pierwszym dniu nie ma akcji, ostatni pomijamy i robimy ręcznie
        wallet.append(money + round(stocks * prices[i])) # w pierwszym dniu jest 1k w portfelu, ostatni pomijamy i robimy ręcznie
    money += round(stocks * prices[-1],2)
    if(stocks != 0):
        transactions.append((round(stocks * prices[-1],2), 'sell'))
    stocks = 0
    actions.append(stocks)
    wallet.append(money)
    print(money)
    return wallet, actions, transactions


###
### Wykresy
###

def plotMACD(macd_v, signal_v, timestamps_v, filename, wide=False, start=0, end=1000, folder=""):
    if end > len(macd_v):
        end = len(macd_v)

    buy_points, sell_points = calculate_points(macd_v, signal_v, start, end) # obliczenie punktow kupna i sprzedazy
    macd = macd_v[start:end]
    signal = signal_v[start:end]
    timestamps = timestamps_v[start:end]


    if wide:
        plt.figure(figsize=(12, 5))
    else:
        plt.figure(figsize=(8, 5))
    # Wykresy MACD i SIGNAL
    plt.plot(timestamps, macd, marker='', linestyle='-', color='b', label="MACD")
    plt.plot(timestamps, signal, marker='', linestyle='-', color='r', label="Signal")

    # Kupna i sprzedaż
    if buy_points:
        plt.scatter(timestamps[buy_points], macd[buy_points], color='g', marker='^', label="Kupno", zorder=3)

    if sell_points:
        plt.scatter(timestamps[sell_points], macd[sell_points], color='black', marker='v', label="Sprzedaż", zorder=3)

    plt.xlabel("Data")
    plt.ylabel("MACD i SIGNAL")
    plt.title("MACD i SIGNAL dla " + datanames[datachoice])
    plt.legend()
    plt.grid()

    if filename != "":
        plt.savefig(storage_path + folder + "MACD_" + datanames[datachoice] + filename, dpi=300, bbox_inches="tight")

    # plt.show() # jest usuniete, aby moc wywolac wszystko na raz


def plotStockPrices(prices_v, macd_v, signal_v, timestamps_v, filename, wide=False, start=0, end=1000, folder=""):
    if end > len(prices_v):
        end = len(prices_v)

    buy_points, sell_points = calculate_points(macd_v, signal_v, start, end)  # obliczenie punktow kupna i sprzedazy

    prices = prices_v[start:end]
    timestamps = timestamps_v[start:end]

    if wide:
        plt.figure(figsize=(12, 5))
    else:
        plt.figure(figsize=(8, 5))

    plt.plot(timestamps, prices, marker='', linestyle='-', color='gray', label=f"Wartość akcji w {datacurrency[datachoice]}")

    # Kupna i sprzedaż
    if buy_points:
        plt.scatter(timestamps[buy_points], prices[buy_points], color='g', marker='^', label="Punkty kupna", zorder=3)

    if sell_points:
        plt.scatter(timestamps[sell_points], prices[sell_points], color='r', marker='v', label="Punkty sprzedaży", zorder=3)

    plt.xlabel("Data")
    plt.ylabel("Cena zamknięcia")

    plt.title("Notowania spółki " + datanames[datachoice])
    plt.legend()
    plt.grid()

    if filename != "":
        plt.savefig(storage_path + folder + "Stock_prices_" + datanames[datachoice] + filename, dpi=300, bbox_inches="tight")

    # plt.show() # jest usuniete, aby moc wywolac wszystko na raz


def plotHoldings(actions_v, timestamps_v, filename, wide=False, start=0, end=1000):
    #run a simulation before plotting
    if end > len(actions_v):
        end = len(actions_v)

    actions = actions_v[start:end]
    timestamps = timestamps_v[start:end]

    if wide:
        plt.figure(figsize=(12, 5))
    else:
        plt.figure(figsize=(8, 5))

    plt.plot(timestamps, actions, color='purple', label=f"Liczba akcji {datanames[datachoice]}")

    plt.xlabel("Data")
    plt.ylabel("Liczba akcji")
    plt.title("Posiadane akcje spółki " + datanames[datachoice])
    plt.legend()
    plt.grid()

    if filename != "":
        plt.savefig(storage_path +  "Holdings_" + datanames[datachoice] + filename, dpi=300, bbox_inches="tight")

    # plt.show() # jest usuniete, aby moc wywolac wszystko na raz


def plotWallet(wallet_v, timestamps_v, filename, wide=False, start=0, end=1000):
    # run a simulation before plotting
    if end > len(wallet_v):
        end = len(wallet_v)

    wallet = wallet_v[start:end]
    timestamps = timestamps_v[start:end]


    if wide:
        plt.figure(figsize=(12, 5))
    else:
        plt.figure(figsize=(8, 5))

    plt.plot(timestamps, wallet, color='green', label=f"Wartość portfela w {datacurrency[datachoice]}")

    plt.xlabel("Data")
    plt.ylabel("Wartość portfela")
    plt.title("Wartość portfela inwestycyjnego dla " + datanames[datachoice])
    plt.legend()
    plt.grid()

    if filename != "":
        plt.savefig(storage_path +  "Wallet_" + datanames[datachoice] + filename, dpi=300, bbox_inches="tight")

    # plt.show() # jest usuniete, aby moc wywolac wszystko na raz


def plotTransactions(transactions, filename, wide=False):
    # run a simulation before plotting
    print(f"Ilość transakcji: {len(transactions)}")
    # print(transactions)

    sum_trans = []
    for i in range(len(transactions) // 2):
        sum_trans.append(transactions[i * 2 + 1][0] - transactions[i * 2][0])

    if wide:
        plt.figure(figsize=(12, 5))
    else:
        plt.figure(figsize=(8, 5))

    indices = np.arange(len(sum_trans))

    colors = ['green' if value > 0 else 'red' for value in sum_trans]

    plt.bar(indices, sum_trans, color=colors, label=f"kolejna transakcja kupna+sprzedaży w {datacurrency[datachoice]}")

    # Opis osi
    plt.xlabel("Transakcja nr")
    plt.ylabel("Zysk / Strata")
    plt.title("Wykres zysków i strat z transakcji dla " + datanames[datachoice])

    # Siatka pomocnicza
    plt.grid()
    plt.legend()

    if filename != "":
        plt.savefig(storage_path +  "Transactions_" + datanames[datachoice] + filename, dpi=300, bbox_inches="tight")

    # plt.show() # jest usuniete, aby moc wywolac wszystko na raz





# interesujace fragmenty dla poszczegolnych akcji
start_end = [0, 500, 500, 1000]
if(datachoice == 0): # dla AAPL
    start_end = [0, 500, 850, 1000]
elif(datachoice == 1): # dla NESN
    start_end = [435, 575, 500, 1000]
elif (datachoice == 2): # dla ALEP
    start_end = [85, 200, 500, 1000]


wallet, actions, transactions = simulation(prices, macd, signal)

# print(transactions)



plotMACD(macd, signal, timestamps,"_full", True)
plotMACD(macd, signal, timestamps,"_zoom1", False, start_end[0], start_end[1], "zoom/")
plotMACD(macd, signal, timestamps,"_zoom2", False, start_end[2], start_end[3], "zoom/")

plotStockPrices(prices,macd,signal, timestamps, "_full", True)
plotStockPrices(prices,macd,signal, timestamps, "_zoom1", False, start_end[0], start_end[1], "zoom/")
plotStockPrices(prices,macd,signal, timestamps, "_zoom2", False, start_end[2], start_end[3], "zoom/")

plotHoldings(actions, timestamps, "_full", True)
plotWallet(wallet, timestamps, "_full", True)

# # plotWallet(wallet, timestamps, "_zoom1", False, start_end[0], start_end[1]) # nie robimy tego
# # plotWallet(wallet, timestamps, "_zoom2", False, start_end[2], start_end[3]) # nie robimy tego
# # plotHoldings(actions, timestamps, "_zoom1", False, start_end[0], start_end[1]) # nie robimy tego
# # plotHoldings(actions, timestamps, "_zoom2", False, start_end[2], start_end[3]) # nie robimy tego

plotTransactions(transactions, "_full", True)

plt.show()



# print(wallet)
# print(stock_actions)


# 1800.08, 76
# 1068.07, 74
# 776.18, 74



#TODO stock prices (9)
# Stock_prices_AAPL, Stock_prices_MACD_NESN, Stock_prices_MACD_ALEP * {zoom1}, * {zoom2}
#TODO macd (9)
# MACD_AAPL, MACD_NESN, MACD_ALEP * {zoom1}, * {zoom2}
#TODO holdings (3)
# HOLDINGS_AAPL,  HOLDINGS_NESN,  HOLDINGS_ALEP overall
#TODO portfel (3)
# WALLET_AAPL, VOLUME_NESN, VOLUME_ALEP overall
#TODO transactions (3)
# TRANS_AAPL, TRANS_NESN, TRANS_ALEP overall



