import pandas as pd

df1 = pd.read_csv("df_Orders.csv")
df2 = pd.read_csv("df_OrderItems.csv")

# Merge the two DataFrames on the 'OrderID' column
merged_df = pd.merge(df1, df2, on='order_id')
merged_df.to_csv("order.csv", index=False)