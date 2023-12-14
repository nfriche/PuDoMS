import pandas as pd

# Load the CSV files
metadata_df = pd.read_csv('metadata.csv')
new_df = pd.read_csv('NEW.csv')

# Merge the dataframes
merged_df = pd.merge(metadata_df, new_df[['File_Number', 'Instruments']], on='File_Number', how='left')

# Overwrite the original metadata.csv with the merged dataframe
merged_df.to_csv('metadata.csv', index=False)