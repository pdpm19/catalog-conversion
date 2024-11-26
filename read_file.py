import pandas as pd
import matplotlib.pyplot as plt
import os
from obspy.core import read, UTCDateTime
from obspy.core.inventory import read_inventory

# static variables
current_directory = os.getcwd()
input_file = 'input.mseed'
output_file = 'generated.xlsx'


# read file using pandas
df = pd.read_csv(os.path.join(current_directory, input_file))

print(df.head(20))


# 



inventory = read_inventory(os.path.join(current_directory, input_file))

print(inventory)

# Saves the file into Excel format
# df.to_excel(output_file)

# Reads an Excel file
# df2 = pd.read_excel(output_file)

df.plot()
plt.show()

full_df = df.to_string()

print(full_df)

splitted = full_df.split()

print(splitted)

