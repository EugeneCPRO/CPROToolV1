
import callAPI
import updateTickers

# financials

class finGet():
    def __init__():
        return

    mUrl = str("https://rest.cryptoapis.io/market-data/exchange-rates/by-symbols/")

    def getAssets(chain,address,what,name):
        directory = f'./{name}/'
        filename = f'{name}_{chain}_{what}.json'
        tickers = []
        balances = []
        data = callAPI.openFile(directory+filename)
        lenData = len(data["data"]["items"])

        for i in range(lenData):
            ticker = data["data"]["items"][i]["symbol"]
            tickers.append(ticker)

        for i in range(lenData):
            balance = data["data"]["items"][i]["confirmedBalance"]
            balances.append(float(balance))
        return tickers, balances

    def priceStream(tickers):
        ticker_prices = updateTickers.getTickerPrice(tickers)
        print(ticker_prices)
        return ticker_prices

    def balValue(portfolio,name):

        base = "usd"
        value = []
        tickers = portfolio[1]

        for i in range(len(portfolio[0])):
            # i believe this could be optimised by getting all assets with single call
            val = portfolio[1][i] * callAPI.cAPIPrice(portfolio[0][i],base,name)
            str(val)
            value.append(val)

        total = sum(value)

        return value, total

