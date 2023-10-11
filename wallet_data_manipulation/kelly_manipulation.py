import json

# Load the portfolio data from the JSON file
with open('test2.json', 'r') as json_data:
    portfolio = json.load(json_data)

# Check if "Cash" exists in the portfolio
if "Cash" not in portfolio:
    # If "Cash" is not in the portfolio, add a default cash amount (you can adjust as needed)
    cash_amount = 30000.0  # Default cash amount
    portfolio["Cash"] = {
        "name": "Cash",
        "value": cash_amount,
        "successProbability": 1.0,  # You can set success probability to 1 for cash
        "expectedReturn": 0.0  # You can set expected return to 0 for cash
    }

# Calculate the portfolio value as the sum of asset values, including cash
portfolio_value = sum(params["value"] for params in portfolio.values())

# Calculate half Kelly allocations without any limiting factors
kelly_allocations = {}
for asset, params in portfolio.items():
    if asset != "Cash":
        expected_return = params["expectedReturn"]
        success_probability = params["successProbability"]
        
        # Calculate the Kelly fraction for each asset (half Kelly)
        b = expected_return
        p = success_probability
        q = 1 - p
        f = 0.5 * (p-((1-q) / b))  # Half Kelly
        
        
        kelly_allocations[asset] = f

# Calculate the total half Kelly allocation
total_half_kelly_allocation = sum(kelly_allocations.values())

# Calculate the adjusted allocations without any limiting factors
adjusted_allocations = {asset: (allocation / total_half_kelly_allocation) * portfolio_value for asset, allocation in kelly_allocations.items()}

# Create a list of tuples (asset, allocation) for sorting
allocation_tuples = [(asset, allocation) for asset, allocation in adjusted_allocations.items()]

# Sort the list of tuples by allocation in descending order
allocation_tuples.sort(key=lambda x: x[1], reverse=True)

# Print the adjusted allocations, success probability, and expected gain in order of allocation size
for asset, allocation in allocation_tuples:
    success_probability = portfolio[asset]["successProbability"]
    expected_gain = portfolio[asset]["expectedReturn"]
    
    print(f"{asset}: Adjusted Allocation = ${allocation:.2f}, Success Probability = {success_probability:.2f}, Expected Gain = {expected_gain:.2f}")

# Define the expected returns and adjusted allocations
expected_returns = {asset: params["expectedReturn"] for asset, params in portfolio.items() if asset != "Cash"}

# Calculate expected returns for each asset based on adjusted allocations
expected_returns_dict = {asset: expected_returns[asset] * adjusted_allocations[asset] for asset in adjusted_allocations}

# Calculate the overall portfolio return
overall_portfolio_return = sum(expected_returns_dict.values())

# Create a dictionary to store the results
results = {
    "Total Portfolio Value": portfolio_value,
    "Adjusted Allocations": adjusted_allocations,
    "Expected Returns for Each Asset": expected_returns_dict,
    "Overall Portfolio Return": overall_portfolio_return
}

# Save the results to a new JSON file
output_file = 'portfolio_results.json'
with open(output_file, 'w') as json_output:
    json.dump(results, json_output, indent=4)

print(f"Results saved to {output_file}")
