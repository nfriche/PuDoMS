import pandas as pd

## Load the metadata and silent DataFrames
metadata_df = pd.read_csv('metadata.csv')
silent_df = pd.read_csv('silent.csv', header=None)  # Use header=None if the file doesn't have a header row

## Ensure the silent_df values are of the same type as File_Number in metadata_df (convert to same data type)
silent_set = set(silent_df[0].astype(metadata_df['File_Number'].dtype))

## Define a function to check if a file number is silent
def is_silent(file_number):
    return 'Yes' if file_number in silent_set else 'No'

## Apply the function to each row in the metadata DataFrame
metadata_df['Silent'] = metadata_df['File_Number'].apply(is_silent)

## Save the modified DataFrame back to a csv
metadata_df.to_csv('metadata.csv', index=False)
