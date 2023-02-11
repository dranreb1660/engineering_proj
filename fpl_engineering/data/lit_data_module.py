import os
import numpy as np
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from fpl_engineering.data.base_dataset import FPLDataset, make_sequences
from fpl_engineering.data.fpl import FPL

# wraping our data into a pl datamodule
class FPLDataModule(pl.LightningDataModule):
    """
    
    """
    def __init__(self,batch_size: int, data_dir:str , seq_len: int, n_features: int, download_data:bool):
        super().__init__()
        self.batch_size = batch_size
        self.data_dir = data_dir
        self.seq_len = seq_len
        self.n_features = n_features
        self.download_data = download_data

        self.scaler = StandardScaler()
        

    def prepare_data(self):

        # download
        data = FPL(self.data_dir, download=self.download_data)
        self.df = data.get_cleaned_df()
        self.tr_sequences,self.tr_targets, self.val_sequences, self.val_targets = make_sequences(self.df, s_len=self.seq_len)
        self.scaler.fit(np.stack(self.tr_sequences).reshape(-1,self.seq_len * self.n_features ))

        self.tr_sequences = self.scaler.transform( np.stack(self.tr_sequences).reshape(-1,self.seq_len * self.n_features)).reshape(-1,self.seq_len ,self.n_features)
        self.val_sequences = self.scaler.transform( np.stack(self.val_sequences).reshape(-1,self.seq_len * self.n_features)).reshape(-1,self.seq_len, self.n_features)


    def setup(self, stage:str):

        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            self.train_dataset = FPLDataset(self.tr_sequences, self.tr_targets)
            self.val_dataset = FPLDataset(self.val_sequences, self.val_targets)
    
        # Assign test dataset for use in dataloader(s)
        if stage == "test":
            self.val_dataset = FPLDataset(self.val_sequences, self.val_targets)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset, batch_size=self.batch_size,
            shuffle=False, num_workers=os.cpu_count()
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset, batch_size=1,
            num_workers=os.cpu_count()
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset, batch_size=1,
            num_workers=os.cpu_count()
        )

