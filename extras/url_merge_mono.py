import pandas as pd

## Load the CSV files
urls_df = pd.read_csv('urls.csv')
metadata_df = pd.read_csv('metadata.csv')

## Append the URL column from urls_df to metadata_df
merged_df = pd.concat([metadata_df, urls_df['URL']], axis=1)

## Monophonic file numbers path 
mono_folder_path = 'C:\\Users\\nikit\\escraping_hell\\super-cool-thesis\\data\\extra\\monophonic_midi_numbers.csv'

## Load the monophonic file numbers
monophonic_files_df = pd.read_csv(mono_folder_path)

## Convert the monophonic file numbers to a list
monophonic_files_list = monophonic_files_df['File_Number'].tolist()

## Add a 'Monophonic' column with default value 'No'
merged_df['Monophonic'] = 'No'

## Update the 'Monophonic' column based on whether the file number is in the monophonic list
## Assuming 'File_Number' is the column in metadata_df that matches 'File_Number' in monophonic_files_list
merged_df['Monophonic'] = merged_df['File_Number'].apply(lambda x: 'Yes' if x in monophonic_files_list else 'No')

## Save the updated dataframe to metadata.csv
merged_df.to_csv('metadata.csv', index=False)

## Display the first few rows of the merged dataframe
print(merged_df.head())
