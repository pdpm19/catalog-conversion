import pandas as pd

# Sample data in a multiline string format
data = """
   1   2012 11 01 00:42:40.507     2560.507   0.8409       6.8978       0.0634      15.0000     -inf     -nan    3    1    4   306.92
   GH     SHAI     P    2563.9900       3.4833   0.0000e+00       0.0098       0.2705       0.0441
   GH     KLEF     P    2565.4300       4.9233   0.0000e+00       1.3600       0.5900     306.9688
   GH     KLEF     S    2566.4700       5.9633   0.0000e+00      -0.0098       0.1800     306.9688
   GH     AKOS     P    2569.2700       8.7633   0.0000e+00      -0.5213       0.1393     359.5549
"""

# Create a list of column names for both row types
columns_type1 = ["Index", "Year", "Month", "Day", "Time", "Value1", "Value2", "Value3", "Value4", "Value5", "Value6", "Value7", "Value8", "Value9", "Value10"]
columns_type2 = ["Code1", "Code2", "Type", "Value1", "Value2", "Value3", "Value4", "Value5", "Value6"]

# Load the data line-by-line and distinguish between row types
rows_type1 = []
rows_type2 = []

for line in data.strip().splitlines():
    parts = line.split()
    if len(parts) == 15:
        rows_type1.append(parts)  # First row type with 15 columns
    elif len(parts) == 9:
        rows_type2.append(parts)  # Second row type with 9 columns

# Create DataFrames for each row type
df_type1 = pd.DataFrame(rows_type1, columns=columns_type1)
df_type2 = pd.DataFrame(rows_type2, columns=columns_type2)

# Convert numerical columns to proper data types
for df in [df_type1, df_type2]:
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

print("DataFrame for Type 1 rows:")
print(df_type1)

print("\nDataFrame for Type 2 rows:")
print(df_type2)