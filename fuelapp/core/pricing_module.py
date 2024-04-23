def calculate_price(gallons_requested, location, has_history):
    current_price_per_gallon = 1.50
    location_factor = 0.02 if location == 'TX' else 0.04
    rate_history_factor = 0.01 if has_history else 0
    gallons_requested_factor = 0.02 if gallons_requested > 1000 else 0.03
    company_profit_factor = 0.10
    
    margin = current_price_per_gallon * (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor)
    suggested_price = current_price_per_gallon + margin
    return suggested_price, gallons_requested * suggested_price


