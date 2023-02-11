import torch
import torch.nn as nn
import pytorch_lightning as pl

class FPLLSTMRegressor(pl.LightningModule):
    '''
    Standard PyTorch Lightning module:
    https://pytorch-lightning.readthedocs.io/en/latest/lightning_module.html
    '''
    def __init__(self, 
                 n_features, 
                 hidden_size, 
                 seq_len, 
                 batch_size,
                 num_layers, 
                 dropout, 
                 learning_rate):
        super(FPLLSTMRegressor, self).__init__()
        self.n_features = n_features
        self.hidden_size = hidden_size
        self.seq_len = seq_len
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.learning_rate = learning_rate

        self.criterion = nn.MSELoss()
        self.lstm = nn.LSTM(input_size=self.n_features, 
                                hidden_size=self.hidden_size,
                                num_layers=self.num_layers, 
                                dropout=self.dropout, 
                                batch_first=True)
        self.linear = nn.Linear(self.hidden_size, 1)

        self.save_hyperparameters()

        
    def forward(self, x):
        # lstm_out = (batch_size, seq_len, hidden_size)
        self.lstm.flatten_parameters()
        _, (hidden, _) = self.lstm(x)
        out = hidden[-1]
        y_pred = self.linear(out)
        return y_pred

    def common_step(self, batch):
        x = batch['sequence']
        y = batch['label']
        y_hat = self(x)
        loss = self.criterion(y_hat, y.unsqueeze(1))
        return loss, y_hat

    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    def training_step(self, batch, batch_idx):
        loss, _ = self.common_step(batch)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, _ = self.common_step(batch)
        self.log('val_loss', loss)
        return loss

    
    def test_step(self, batch, batch_idx):
        loss, _ = self.common_step(batch)
        self.log('test_loss', loss)