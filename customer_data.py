import pandas as pd
import numpy as np
import random

# Set seed for Python's random module
random.seed(42)

# Set seed for NumPy (affects pandas operations that rely on NumPy)
np.random.seed(42)


# Set the number of customers
num_customers = 1000

# Define segment proportions
segment_proportions = [0.3, 0.5, 0.2]  # First, Second, Third

# Calculate the number of customers in each segment
num_first = int(num_customers * segment_proportions[0])
num_second = int(num_customers * segment_proportions[1])
num_third = num_customers - num_first - num_second

# Function to generate data for each segment with distributions around the given averages
def generate_data(num_customers, age_range, loyalty_range, purchase_amount_range, purchase_freq_range, income_range, avg_units, avg_price):
    ages = np.random.randint(*age_range, size=num_customers)
    loyalties = np.random.uniform(*loyalty_range, size=num_customers)
    purchase_amounts = np.random.normal(loc=(purchase_amount_range[0] + purchase_amount_range[1]) / 2, 
                                        scale=(purchase_amount_range[1] - purchase_amount_range[0]) / 6, 
                                        size=num_customers)
    purchase_frequencies = np.random.normal(loc=(purchase_freq_range[0] + purchase_freq_range[1]) / 2, 
                                            scale=(purchase_freq_range[1] - purchase_freq_range[0]) / 6, 
                                            size=num_customers)
    annual_incomes = np.random.normal(loc=(income_range[0] + income_range[1]) / 2, 
                                      scale=(income_range[1] - income_range[0]) / 6, 
                                      size=num_customers)
    average_units = np.random.normal(loc=avg_units, scale=avg_units / 6, size=num_customers)
    average_price = np.random.normal(loc=avg_price, scale=avg_price / 6, size=num_customers)
    
    # Ensure no negative values
    purchase_amounts = np.clip(purchase_amounts, purchase_amount_range[0], purchase_amount_range[1])
    purchase_frequencies = np.clip(purchase_frequencies, purchase_freq_range[0], purchase_freq_range[1])
    annual_incomes = np.clip(annual_incomes, income_range[0], income_range[1])
    average_units = np.clip(average_units, 1, avg_units * 2)  # reasonable upper limit
    average_price = np.clip(average_price, 0.01, avg_price * 2)  # reasonable upper limit

    return ages, loyalties, purchase_amounts, purchase_frequencies, annual_incomes, average_units, average_price

# Generate data for each segment
age_first, loyalty_first, purchase_amount_first, purchase_frequency_first, annual_income_first, average_units_first, average_price_first = generate_data(
    num_first, (50, 70), (70, 100), (300, 500), (10, 50), (70000, 150000), 9, 4.77)

age_second, loyalty_second, purchase_amount_second, purchase_frequency_second, annual_income_second, average_units_second, average_price_second = generate_data(
    num_second, (30, 50), (40, 70), (150, 300), (5, 30), (40000, 90000), 10.5, 1.98)

age_third, loyalty_third, purchase_amount_third, purchase_frequency_third, annual_income_third, average_units_third, average_price_third = generate_data(
    num_third, (18, 30), (1, 40), (50, 150), (1, 10), (20000, 50000), 20, 0.94)

# Combine data
ages = np.concatenate([age_first, age_second, age_third])
loyalties = np.concatenate([loyalty_first, loyalty_second, loyalty_third])
purchase_amounts = np.concatenate([purchase_amount_first, purchase_amount_second, purchase_amount_third])
purchase_frequencies = np.concatenate([purchase_frequency_first, purchase_frequency_second, purchase_frequency_third])
annual_incomes = np.concatenate([annual_income_first, annual_income_second, annual_income_third])
average_units = np.concatenate([average_units_first, average_units_second, average_units_third])
average_prices = np.concatenate([average_price_first, average_price_second, average_price_third])
genders = np.random.choice(['Male', 'Female'], size=num_customers)

# Create a DataFrame
data = {
    'CustomerID': range(1, num_customers + 1),
    'Age': ages,
    'Gender': genders,
    'AnnualIncome': annual_incomes,
    'PurchaseAmount': purchase_amounts,
    'PurchaseFrequency': purchase_frequencies,
    'LoyaltyScore': loyalties,
    'AverageUnits': average_units,
    'AveragePrice': average_prices
}

customer_df = pd.DataFrame(data)

# Convert the average price to German decimal format
#customer_df['AveragePrice'] = customer_df['AveragePrice'].map(lambda x: f"{x:.2f}".replace('.', ','))

# Rounding all values to the second decimal
customer_df['PurchaseAmount'] = customer_df['PurchaseAmount'].round(0)
customer_df['AnnualIncome'] = customer_df['AnnualIncome'].round(0)
customer_df['Age'] = customer_df['Age'].round(0)
customer_df['PurchaseFrequency'] = customer_df['PurchaseFrequency'].round(0)
customer_df['LoyaltyScore'] = customer_df['LoyaltyScore'].round(0)
customer_df['AverageUnits'] = customer_df['AverageUnits'].round(0)
customer_df['AveragePrice'] = customer_df['AveragePrice'].round(2)

# Save the dataframe to an Excel file with German decimal format
output_path = "customer_data.xlsx"
customer_df.to_excel(output_path, index=False)