import json
import coinmarketcapapi

# Initialize CoinMarketCap API
cmc = coinmarketcapapi.CoinMarketCapAPI('301f73fd-54ba-4fac-91bd-b599b50d3de5')

# List of assets (symbols) for which you want to retrieve prices

# Call the function to retrieve prices
def priceCall(symbols):
    symbols = "".join(symbols)
    price_data_response = cmc.cryptocurrency_quotes_latest(symbol=symbols, convert='USD')
    filtered_data = {}
    # Check if the response contains data
    if price_data_response.data:
        # Extract the JSON content from the response
        price_data = price_data_response.data
        symbols = symbols.split(',')
        for symbol in symbols:  # Only process the symbols specified in the list
            if symbol in price_data:
                symbol_data = price_data[symbol]

                if symbol_data:  # Check if symbol_data is not empty
                    asset_data = {
                        "asset": symbol,
                        "max_supply": symbol_data[0].get("max_supply", 0),
                        "circulating_supply": symbol_data[0].get("circulating_supply", 0),
                        "total_supply": symbol_data[0].get("total_supply", 0),
                        "cmc_rank": symbol_data[0].get("cmc_rank", 0),
                        "price": symbol_data[0]["quote"]["USD"].get("price", 0)
                    }
                    filtered_data[symbol] = asset_data
                else:
                    # Handle the case where symbol_data is empty
                    filtered_data[symbol] = {
                        "asset": symbol,
                        "max_supply": 0,
                        "circulating_supply": 0,
                        "total_supply": 0,
                        "cmc_rank": 0,
                        "price": 0
                    }

        print(filtered_data)
        return filtered_data







#symbols = ['BTC,ETH,LTC'] 
