import json
import random


def randomiseKellyStats(portfolio):

    # Check and generate random statistics for other assets if missing
    for asset, details in portfolio.items():
        if asset != "Cash" and ("successProbability" not in details or "expectedReturn" not in details):
            # Generate random success probability (between 0.0 and 1.0)
            success_probability = round(random.uniform(0.1, 0.6), 2)
            # Generate random expected return (between -1.0 and 1.0)
            expected_return = round(random.uniform(2, 20), 2)

            # Update the portfolio data with random statistics
            details["successProbability"] = success_probability
            details["expectedReturn"] = expected_return

    # Save the updated portfolio data to a JSON file
    output_file = 'test.json'
    with open(output_file, 'w') as json_output:
        json.dump(portfolio, json_output, indent=4)

    print(f"Updated portfolio data saved to {output_file}")
