import asyncio
import json
import websockets

class CryptoDataUpdater:
    def __init__(self, websocket_url, json_file, main_file):
        self.websocket_url = websocket_url
        self.json_file = json_file
        self.main_file = main_file
        self.crypto_prices = {}
        self.crypto_data = {}

    async def on_message(self, websocket, path):
        async for message in websocket:
            try:
                data = json.loads(message)

                for asset, price in data.items():
                    print(asset, price)

                    # Check if the price has changed
                    if self.crypto_prices.get(asset) != price:
                        self.crypto_prices[asset] = float(price)
                        print(f"Updated {asset} price: {price}")

                        # Split asset name into token name and ticker (assuming format is "token_name-ticker")
                        token_name, ticker = asset.split("-")

                        # Create the data structure
                        if token_name not in self.crypto_data:
                            self.crypto_data[token_name] = {}
                        if ticker not in self.crypto_data[token_name]:
                            self.crypto_data[token_name][ticker] = {}

                        # Update the price in the data structure
                        self.crypto_data[token_name][ticker]['price'] = price

                # Save updated data to the JSON file
                with open(self.json_file, 'w') as file:
                    json.dump(self.crypto_data, file, indent=4)

            except Exception as e:
                print(f"Error: {str(e)}")

    async def run_websocket(self):
        async with websockets.connect(self.websocket_url) as websocket:
            await websocket.send('{"method":"subscribe","topic":"market-all","market":"ALL"}')
            await self.on_message(websocket, None)

    async def main(self):
        # Start the WebSocket connection in the background
        asyncio.create_task(self.run_websocket())

        # Your program can continue executing other tasks here
        while True:
            await asyncio.sleep(1)  # Perform other tasks and sleep to avoid busy-waiting
