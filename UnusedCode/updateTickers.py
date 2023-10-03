
import requests
import json

# Define the API URL
api_url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
class priceManipulation(object):
        def __init__():
            return
        
# call this function to update ticker list (maybe once a week)
def getData():
    try:
        # Make a GET request to fetch coin data
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            coin_data = response.json()

            # Define the name of the JSON file to store the data
            json_file = 'coin_data.json'

            # Write the data to the JSON file
            with open(json_file, 'w') as file:
                json.dump(coin_data, file, indent=4)

            print(f'Data has been successfully stored in {json_file}')
        else:
            print(f'Failed to retrieve data. Status code: {response.status_code}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


# cross-reference CoinGecko data with API data (get tickers from name)
# e.g. input = 'bitcoin', output = 'btc'
def replaceTickers():

    # Load the data from file A (token file) and file B (ticker file)
    file_a_path = 'priceData.json'  # Replace with the path to your file A
    file_b_path = 'coin_data.json'  # Replace with the path to your file B

    with open(file_a_path, 'r') as file_a:
        data_a = json.load(file_a)

    with open(file_b_path, 'r') as file_b:
        data_b = json.load(file_b)

    # Create a new dictionary to store the updated data from file A
    updated_data_a = {}

    # Iterate through tokens in file A and try to match them with tickers in file B
    for token_name, token_value in data_a.items():
        matched_ticker = None
        
        # Search for a matching ticker in file B
        for entry_b in data_b:
            if entry_b['id'] == token_name:
                matched_ticker = entry_b['symbol']
                break  # Exit the loop when a match is found
        
        # If a match is found, create the desired structure
        if matched_ticker:
            print(matched_ticker,token_name)
            updated_data_a[token_name] = {
                'ticker': matched_ticker,
                'value': token_value
            }
        else:
            # If no match is found, use the first three letters of the token name as the ticker
            updated_data_a[token_name] = {
                'ticker': token_name[:6],
                'value': token_value
            }

    # Create the final output dictionary in the desired structure
    final_output = {'database': []}

    for token_name, token_data in updated_data_a.items():
        ticker = token_data['ticker']
        value = token_data['value']
        final_output['database'].append({
            'tokenname': token_name,
            'ticker': ticker,
            'value': value
        })
        
    # Print the final output
    print(json.dumps(final_output, indent=4))

    # Optionally, you can save the final output to a new file
    output_file_path = 'output_file.json'  # Replace with the desired output file path
    with open(output_file_path, 'w') as output_file:
        json.dump(final_output, output_file, indent=4)

    print(f'Final output has been saved to {output_file_path}')

# Update ticker list on launch
#replaceTickers()

# Function for matching a user token with its respective price

def getTickerPrice(user_tickers):
    # Specify the file path for the ticker data
    ticker_file = 'output_file.json'

    # Load ticker data from the JSON file
    with open(ticker_file, 'r') as tick:
        tickers = json.load(tick)

    # Convert user_tickers to lowercase for case-insensitive matching
    user_tickers = [ticker.lower() for ticker in user_tickers]

    # Initialize a dictionary to store matched ticker and price pairs
    matched_prices = {}

    # Iterate through user_tickers and find matching prices
    for i in range(len(tickers['database'])):
        ticker = tickers['database'][i]['ticker']
        if ticker in user_tickers:
            ticker = tickers['database'][i]['tokenname']
            matched_prices[ticker] = get_price_from_json(ticker)

    return matched_prices

# Function to get price data from the priceData.json file
# this means that price data can be continously streamed
# a cache file is created which is used to cross-reference
# user makes an internal request for price 

# inputs can be a long string of x many assets, return price for all in a list

def get_price_from_json(ticker):
    # Specify the file path for the price data
    price_file = 'priceData.json'
    price = []
    try:
        # Open the price data file and read it
        with open(price_file, 'r') as price_data:
            data = json.load(price_data)

        # Look up the ticker in the live price data
        price.append(float(data.get(ticker, 0)))
    except FileNotFoundError:
        price = 0
    print(price)
    return price

# custom price search for users
def customPriceSearch():
    if __name__ == "__main__":
        user_input = input("Enter tickers (comma-separated): ")
        user_tickers = user_input.split(",")

        ticker_prices = getTickerPrice(user_tickers)

        for ticker, price in ticker_prices.items():
            print(f"{ticker}: {price}")







