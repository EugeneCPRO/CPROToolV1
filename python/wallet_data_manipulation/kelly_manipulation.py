import json

# Load the portfolio data
with open('updated_portfolio.json', 'r') as json_data:
    portfolio = json.load(json_data)

# Initialize cash balance
cash_balance = 0.0

# List of Ethereum stablecoin contracts (can add all stablecoins here from any chain)
stablecoin_contracts = [
    "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
    "0x4fabb145d64652a948d72533023f6e7a623c7c53",  # BUSD
    "0x056fd409e1d7a124bd7017459dfea2f387b6d5cd",  # CEL
    "0x0000000000085d4780b73119b644ae5ecd22b376",  # Tether USD (USDT on Ethereum)
    "0x8e870d67f660d95d5be530380d0ec0bd388289e1",  # PAX
    "0xdf574c24545e5ffecb9a659c229253d4111d87e1",  # TrueUSD (TUSD)
    "0x57ab1ec28d129707052df4df418d58a2d46d5f51",  # sUSD
]


# Identify stablecoins and treat them as cash
stablecoin_symbols = []  # Create a list to store stablecoin symbols

for asset, details in portfolio.items():
    if details["contractAddress"] in stablecoin_contracts:
        print(f'{details["symbol"]} with balance {details["value"]} identified.')
        cash_balance += details["value"]
        # Set the value of stablecoins to 0, so they are considered cash for further calculations
        details["value"] = 0.0  # Set the value of stablecoins to 0
        stablecoin_symbols.append(details["symbol"])  # Add the symbol to the stablecoin_symbols list

# Calculate the total portfolio value using the "value" field 
portfolio_value = sum(details["value"] for details in portfolio.values()) + cash_balance

# Calculate the half-Kelly allocations without any limiting factors
kelly_allocations = {}
for asset, details in portfolio.items():
    if details["contractAddress"] in stablecoin_contracts:
        # Skip stablecoins, treat them as cash
        continue

    expected_return = details["expectedReturn"]
    success_probability = details["successProbability"]
    
    if success_probability < 0:
        f = 0
    else:
        b = expected_return
        p = success_probability
        q = 1 - p
        f = 0.5 * (p - (q / b))  # Half Kelly

    kelly_allocations[asset] = f

# Calculate the dollar amount for each new allocation
dollar_allocations = {asset: f * portfolio_value for asset, f in kelly_allocations.items()}

# Calculate the sum of the new allocations
sum_new_allocations = sum(dollar_allocations.values())

# Check if there are negative allocations
negative_assets = [asset for asset, allocation in dollar_allocations.items() if allocation < 0]

# If there are negative allocations, distribute proportionally among other assets
if negative_assets:
    total_negative_allocation = sum(dollar_allocations[asset] for asset in negative_assets)
    
    # Check if there's enough cash to cover negative allocations
    if cash_balance >= abs(total_negative_allocation):
        for asset in negative_assets:
            cash_balance -= dollar_allocations[asset]
            dollar_allocations[asset] = 0
    else:
        for asset in dollar_allocations:
            dollar_allocations[asset] += (dollar_allocations[asset] / (portfolio_value - abs(total_negative_allocation))) * total_negative_allocation
            if dollar_allocations[asset] < 0:
                dollar_allocations[asset] = 0

# Adjust cash balance if the sum of new allocations exceeds the old portfolio value
if sum_new_allocations > portfolio_value:
    cash_balance -= (sum_new_allocations - portfolio_value)

# Scale down allocations if the sum of new allocations is still higher than the old portfolio value
while sum_new_allocations > portfolio_value:
    scaling_factor = portfolio_value / sum_new_allocations
    dollar_allocations = {asset: allocation * scaling_factor for asset, allocation in dollar_allocations.items()}
    sum_new_allocations = sum(dollar_allocations.values())

# Calculate expected overall gains, excluding stablecoins
expected_overall_gain = sum(
    details["expectedReturn"] * details["successProbability"] * details["value"] / portfolio_value
    for details in portfolio.values()
    if details["symbol"] not in stablecoin_symbols  # Exclude stablecoins
)


# Calculate the expected overall gain with Kelly optimization, excluding stablecoins
expected_overall_gain_kelly = sum(
    details["expectedReturn"] * details["successProbability"] * dollar_allocations[asset] / portfolio_value
    for asset, details in portfolio.items() if asset not in stablecoin_symbols
)


# Calculate the expected profit for each strategy
expected_profit = expected_overall_gain * portfolio_value - cash_balance
expected_profit_kelly = expected_overall_gain_kelly * portfolio_value

# Compare gains
if expected_profit_kelly > expected_profit:
    gain_difference = expected_profit_kelly - expected_profit
    print(f"You have increased your expected gains by ${round(gain_difference,2)}")
elif expected_profit_kelly < expected_profit:
    print("You are better than Kelly!")
else:
    print("No change in expected gains.")

# Create the results dictionary
results = {
    "Total Portfolio Value": portfolio_value,
    "Cash Balance": cash_balance,
    "Kelly Ratio Allocations": kelly_allocations,
    "Dollar Allocations": dollar_allocations,
    "Expected Overall Gain": expected_overall_gain,
    "Expected Overall Gain (Kelly)": expected_overall_gain_kelly,
    "Expected Profit": expected_profit,
    "Expected Profit (Kelly)": expected_profit_kelly
}

# Save the results to a JSON file
output_file = 'kelly_optimised_portfolio.json'
with open(output_file, 'w') as json_output:
    json.dump(results, json_output, indent=4)

print(f"Results saved to {output_file}")
