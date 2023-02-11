import torch
from torch.utils.data import Dataset
from tqdm import tqdm
import numpy as np


# Creat sequences, take n sequences and predict the n+1st term
def make_sequences(df, s_len, labels=True):
    """
    makes sequences from a given dataframe. The number of sequences are defined by the s_len parameter. 
    We take the log of the target values. Note:since some players could score as much as -3 or -4 points, 
    5 is added to each target value to prevent 'inf' values since log(0) is undefined

    returns:
        tr_sequences,tr_targets,val_sequences,  val_targets, in that order
    """ 
    print(f'<---------------------------------------------------------------->')   
    print(f'making sequences from raw data\n')   
    tr_sequences, tr_targets = [],[]
    val_sequences, val_targets = [],[]

    # if data has no labels
    if not labels:
        for series_id, group in tqdm(df.groupby('element'), colour='blue'):
            group.sort_values(by='round')
            d_size = len(group)
            # if player has played at least s_len games
            if d_size == s_len:
                for i in range(d_size-(s_len-1)):
                    sequence = group[i:i+s_len]
                    tr_sequences.append(sequence.values)

        print(f'Total sequences made: {len(tr_sequences)} \nSequence length: {s_len}')
        return tr_sequences

    for series_id, group in tqdm(df.groupby('element'), colour='blue'):
        group.sort_values(by='round')
        d_size = len(group)
        # if player has played at least s_len games
        if d_size > s_len:
            for i in range(d_size-(s_len-1)):
                sequence = group[i:i+s_len]
                label = group.iloc[i+s_len]['total_points']
                tr_sequences.append(sequence.values)
                tr_targets.append(round(np.log(label+5),6))
            
            val_sequences.append(tr_sequences.pop())
            val_targets.append(tr_targets.pop())
    print(f'Total train sequences made: {len(tr_sequences)} \nTotal train Validation sequences made: {len(val_sequences)} \nSequence length: {s_len}')
    return tr_sequences,tr_targets,val_sequences,  val_targets
    

class FPLDataset(Dataset):
    def __init__(self, sequences, labels) -> None:
        super().__init__()
        self.sequences = sequences
        self.labels = labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, index):
        sequence = self.sequences[index]
        label = self.labels[index]
        return dict(
            sequence=torch.tensor(sequence, dtype=torch.float),
            label=torch.tensor(label).float()
        )


if __name__ == '__main__':
    print('file run complete')