import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

## Set a random seed for reproducibility
np.random.seed(0)

## Load the metadata file
df = pd.read_csv('metadata.csv')

## Exclude rows where piano isn't the only instrument
instrument_filter = df['Instruments'].isin(['Piano', 'Piano (2)', 'Piano (3)'])
df = df[instrument_filter]

## Assign initial splits based on your criteria
df['Split'] = 'unassigned'
df.loc[df['Difficulty'] == 'Advanced', 'Split'] = 'test'
df.loc[(df['Monophonic'] == 'Yes') | (df['Difficulty'] == 'Beginner'), 'Split'] = 'train'

train_count = df[df['Split'] == 'train'].shape[0]
print("Number of rows assigned to train:", train_count)

## Separate the unassigned data
unassigned_df = df[df['Split'] == 'unassigned'].copy()

## Fill NaN values in stratify columns with a default value 'Unknown'
stratify_cols = ['Composer', 'Genre', 'Difficulty']  
for col in stratify_cols:
    unassigned_df[col] = unassigned_df[col].fillna('Unknown')

## Check if stratification is possible
min_members_in_classes = min(unassigned_df[col].value_counts().min() for col in stratify_cols)

if min_members_in_classes >= 2:
    ## Perform stratified sampling for the unassigned data
    train_val, test_temp = train_test_split(unassigned_df, test_size=0.2, stratify=unassigned_df[stratify_cols])
    train_temp, val_temp = train_test_split(train_val, test_size=0.125, stratify=train_val[stratify_cols])  # 0.125 x 0.8 = 0.1
else:
    ## Stratification is not possible, use simple random sampling
    train_val, test_temp = train_test_split(unassigned_df, test_size=0.2)
    train_temp, val_temp = train_test_split(train_val, test_size=0.125)  


## Assign splits
df.loc[train_temp.index, 'Split'] = 'train'
df.loc[val_temp.index, 'Split'] = 'validation'
df.loc[test_temp.index, 'Split'] = 'test'


def adjust_splits(df, target_counts, original_split_info):
    # Iterate through each split and adjust to meet the target counts
    for split, target_count in target_counts.items():
        current_count = df[df['Split'] == split].shape[0]
        difference = target_count - current_count

        if difference > 0:
            # Need to add more rows to this split
            # Select rows from the originally unassigned rows
            pool = original_split_info[(original_split_info['Split'] == 'unassigned') & (df['Split'] == 'unassigned')]
            if not pool.empty:
                additional = pool.sample(min(len(pool), difference), random_state=0)
                df.loc[additional.index, 'Split'] = split

        elif difference < 0:
            # Need to remove some rows from this split
            # Select rows that are currently in this split but were originally unassigned
            pool = original_split_info[original_split_info['Split'] == split]
            if not pool.empty:
                to_remove = pool.sample(min(len(pool), -difference), random_state=0)
                df.loc[to_remove.index, 'Split'] = 'unassigned'

    # Assign remaining unassigned rows to the splits that haven't reached their target counts
    remaining_unassigned = df[df['Split'] == 'unassigned']
    for split, target_count in target_counts.items():
        current_count = df[df['Split'] == split].shape[0]
        difference = target_count - current_count

        if not remaining_unassigned.empty and difference > 0:
            additional = remaining_unassigned.sample(min(len(remaining_unassigned), difference), random_state=0)
            df.loc[additional.index, 'Split'] = split
            remaining_unassigned = remaining_unassigned.drop(additional.index)

# Store the original split information for unassigned rows
original_split_info = df.copy()

# Define target ratios and calculate target counts
total_rows = len(df)
target_ratios = {'train': 0.8, 'validation': 0.1, 'test': 0.1}
target_counts = {split: int(total_rows * ratio) for split, ratio in target_ratios.items()}

# Apply the adjustment function
adjust_splits(df, target_counts, original_split_info)

# Save the updated dataframe
df.to_csv('updated_metadata_with_split.csv', index=False)
