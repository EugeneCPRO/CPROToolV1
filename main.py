import asyncio
import json
import get_financial_data
from crypto_data_updater import CryptoDataUpdater
from crypto_apis_call import WalletDataProcessor


# test inputs - will be part of menus
address = str("0x938A75511F44325b9a5EB75eBe445BBaeb29F305")
what = str("bal") # tx = transactions, bal = balances
name = str("SITG")
chains = "bitcoin","ethereum"




# launch app
if __name__ == '__main__':
    # format and store wallet data
    processor = WalletDataProcessor(address,what,name)
    processor.fetch_and_store_data()

    # run price updates
    updater = CryptoDataUpdater(
        'wss://ws.coincap.io/prices?assets=ALL',
        'priceData.json',
        'coin_data.json',
        'thirdFile.json'
    )
    asyncio.run(updater.main())


#callAPI.cAPIBal(chain,address,what,name)
# portfolio = finGet.getAssets(chain,address,what,name)
# print(portfolio)
# portValue = finGet.balValue(portfolio, name)
# print(portValue)
# testUI.update_values(portfolio,portValue,name,chain)


