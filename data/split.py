import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('metadata.csv')

# Add a new column for the split and initially set all to 'excluded'
df['Split'] = 'excluded'

# Filter based on the 'Instruments' and 'Download_Status' columns
df_filtered = df[(df['Instruments'].isin(['Piano', 'Piano (2)', 'Piano (3)'])) & (df['Download_Status'] != 'FAILED')]

# Calculate the exact number of files for each split
total_files = len(df_filtered)
train_count = 5663
val_count = 708
test_count = 708

# Perform the split for the filtered dataset
train_val, test_set = train_test_split(df_filtered, test_size=test_count, random_state=42)
train_set, val_set = train_test_split(train_val, test_size=val_count, random_state=42)

# Update the 'Split' column in the original dataframe
df.loc[train_set.index, 'Split'] = 'train'
df.loc[val_set.index, 'Split'] = 'validation'
df.loc[test_set.index, 'Split'] = 'test'

# Save the updated dataframe to a new CSV file
df.to_csv('updated_metadata_with_split.csv', index=False)
