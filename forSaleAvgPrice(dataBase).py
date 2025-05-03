import pandas as pd

# Read the CSV file
df = pd.read_csv(r"C:\Users\User\Desktop\realtor-data.zip.csv")

# Filter the DataFrame
df_filtered = df[df['status'] == 'for_sale'].copy()

# Convert the 'price' column to numeric
df_filtered['price'] = pd.to_numeric(df_filtered['price'])

# Calculate the average price
average_price = round(df_filtered['price'].mean(), 2)

print(average_price)