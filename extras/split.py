import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

## Set a random seed for reproducibility
np.random.seed(0)

## Load the metadata file
df = pd.read_csv('path_to_your_metadata_file.csv')

## Exclude rows where Piano_Only is No
df = df[df['Piano_Only'] == 'Yes']

## Assign initial splits based on your criteria
df['Split'] = 'unassigned'
df.loc[df['Difficulty'] == 'Advanced', 'Split'] = 'test'
df.loc[(df['Monophonic'] == 'Yes') | (df['Difficulty'] == 'Beginner'), 'Split'] = 'train'

## Separate the unassigned data
unassigned_df = df[df['Split'] == 'unassigned']

## Perform stratified sampling for the unassigned data
stratify_cols = ['Composer', 'Genre', 'Difficulty']  ## Modify as needed
train_val, test_temp = train_test_split(unassigned_df, test_size=0.2, stratify=unassigned_df[stratify_cols])
train_temp, val_temp = train_test_split(train_val, test_size=0.125, stratify=train_val[stratify_cols])  ## 0.125 x 0.8 = 0.1

## Assign splits to the stratified samples
df.loc[train_temp.index, 'Split'] = 'train'
df.loc[val_temp.index, 'Split'] = 'validation'
df.loc[test_temp.index, 'Split'] = 'test'

## Function to adjust the splits to 80/10/10
def adjust_splits(df, target_ratios):
    counts = df['Split'].value_counts(normalize=True)
    total = len(df)
    target_counts = {split: int(total * ratio) for split, ratio in target_ratios.items()}

    for split, target_count in target_counts.items():
        current_count = counts.get(split, 0)
        difference = target_count - current_count

        if difference > 0:
            ## Need to add more to this split
            pool = df[df['Split'] == 'unassigned']
            if not pool.empty:
                additional = pool.sample(min(len(pool), difference), random_state=0)
                df.loc[additional.index, 'Split'] = split
        elif difference < 0:
            ## Need to remove some from this split
            pool = df[df['Split'] == split]
            if not pool.empty:
                to_remove = pool.sample(min(len(pool), -difference), random_state=0)
                df.loc[to_remove.index, 'Split'] = 'unassigned'

## Define target ratios for the splits
target_ratios = {'train': 0.8, 'validation': 0.1, 'test': 0.1}

## Apply the adjustment function to the dataframe
adjust_splits(df, target_ratios)

## Handle any remaining unassigned (due to rounding issues or constraints)
## Assign them to the smallest split to balance it out
remaining = df[df['Split'] == 'unassigned']
if not remaining.empty:
    smallest_split = df['Split'].value_counts().idxmin()
    df.loc[remaining.index, 'Split'] = smallest_split

## Save the updated dataframe
df.to_csv('updated_metadata_with_split.csv', index=False)
