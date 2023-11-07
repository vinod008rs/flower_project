from itertools import product

def calculate_order_summary(order_data):
    prices = {
        'R12': [(5, 6.99), (10, 12.99)],
        'L09': [(3, 9.95), (6, 16.95), (9, 24.95)],
        'T58': [(3, 5.95), (5, 9.95), (9, 16.99)]
    }

    def find_best_combination(code, quantity):
        # Generate all combinations of bundle quantities for the product code.
        bundle_combinations = []
        for bundle in prices[code]:
            bundle_qty = bundle[0]
            bundle_combinations.append(range((quantity // bundle_qty) + 1))

        # Calculate the total price for each combination and find the best fit.
        best_combination = None
        best_price = float('inf')
        best_total_bundles = 0  # Keep track of the closest match to the quantity
        for combination in product(*bundle_combinations):
            total_bundles = sum(qty * prices[code][idx][0] for idx, qty in enumerate(combination))
            if total_bundles >= quantity and (total_bundles < best_total_bundles or best_total_bundles < quantity):
                total_price = sum(qty * prices[code][idx][1] for idx, qty in enumerate(combination))
                if total_bundles == quantity and total_price < best_price:
                    best_price = total_price
                    best_combination = combination
                    best_total_bundles = total_bundles
                elif total_bundles > quantity and (best_combination is None or total_bundles < best_total_bundles):
                    best_price = total_price
                    best_combination = combination
                    best_total_bundles = total_bundles

        exact_match = (best_total_bundles == quantity)
        return best_combination, best_price, exact_match

    # Parse the order data and calculate summary.
    lines = order_data.strip().split("\n")
    summary = []

    for line in lines:
        quantity, code = line.split()
        quantity = int(quantity)

        best_combination, total_price, exact_match = find_best_combination(code, quantity)

        if best_combination is not None:
            # Create the item details.
            item_details = [
                {
                    'num_bundles': qty,
                    'bundle_quantity': prices[code][idx][0],
                    'bundle_price': prices[code][idx][1],
                }
                for idx, qty in enumerate(best_combination) if qty > 0
            ]
        else:
            # If no combination found, use the closest match.
            item_details = []

        summary.append({
            'code': code,
            'quantity': quantity,
            'total_price': total_price,
            'bundles': item_details,
            'exact_match': exact_match
        })

    return summary
