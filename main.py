import json
import callAPI
import testUI
import finGet
from crypto_data_updater import CryptoDataUpdater


def main():
    # Create an instance of CryptoDataUpdater with the appropriate parameters
    crypto_data_updater = CryptoDataUpdater(
        'wss://ws.coincap.io/prices?assets=ALL',
        'priceData.json',
        'output_file.json'
    )

    # Start the WebSocket connection and data update loop
    crypto_data_updater.main()

if __name__ == "__main__":
    main()


# test inputs - will be part of menus
chain = str("ethereum")
address = str("0x938A75511F44325b9a5EB75eBe445BBaeb29F305")
what = str("bal") # tx = transactions, bal = balances
name = str("SITG")
chains = "bitcoin","ethereum"


def openFile(filename,directory):
    with open(filename) as data:
        data = json.load(data)
        filename.close()
    return data


#callAPI.cAPIBal(chain,address,what,name)
portfolio = finGet.getAssets(chain,address,what,name)
print(portfolio)
portValue = finGet.balValue(portfolio, name)
print(portValue)
# testUI.update_values(portfolio,portValue,name,chain)


if __name__ == '__main__':
    portfolio = portfolio  # Replace with your portfolio data
    portValue = [sum(portfolio[1])]
    name = name
    chain = chain

    ui = testUI.TestUI(portfolio, portValue, name, chain)
    ui.run()

