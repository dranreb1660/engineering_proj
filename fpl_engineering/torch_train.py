import argparse
import torch, os
import torch.nn as nn
import tqdm
from torch.utils.data import DataLoader

from fpl_engineering.data.base_dataset import FPLDataset, make_sequences
from fpl_engineering.data.fpl import FPL

from torch.autograd import Variable


class LSTMModel(nn.Module):
    def __init__(self, n_features, hidden_size, n_layers):
        super(LSTMModel, self).__init__()

        # Hidden dimensions
        self.hidden_size = hidden_size

        # Number of hidden layers
        self.n_layers = n_layers

        # Building your LSTM
        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(n_features, hidden_size, n_layers, batch_first=True).to(device)

        # Readout layer
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.n_layers, x.size(0), self.hidden_size).requires_grad_().to(device)

        # Initialize cell state
        c0 = torch.zeros(self.n_layers, x.size(0), self.hidden_size).requires_grad_().to(device)

        # One time step
        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 28, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states! 
        out = self.fc(out[:, -1, :]) 
        # out.size() --> 100, 10
        return out




batch_size = 128
device = torch.device(0)
print(device)

def train(config):

    network = LSTMModel(config.n_features, config.hidden_size, config.n_layers)

    print(network)
    print(len(list(network.parameters())))
    for i in range(len(list(network.parameters()))):
        print(list(network.parameters())[i].size())

    optimizer = torch.optim.Adam(network.parameters(), config.lr)
    loss_func = torch.nn.MSELoss()

    data = FPL(config.data_dir, download=False)
    df = data.get_cleaned_df()
    train_sequences, val_sequences = make_sequences(df, s_len=config.seq_len)

    train_dataset = FPLDataset(train_sequences)
    val_dataset = FPLDataset(val_sequences)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False, num_workers=os.cpu_count())
    val_dataloader = DataLoader(val_dataset, batch_size=1, shuffle=False, num_workers=os.cpu_count())

    network.to(device)
    for epoch_idx in range(10):
        train_losses = []

        network.train()
        for data in tqdm.tqdm(train_dataloader):
            # assert (
            #     torch.sum(y >= 10) == 0
            # ), f"y has more than 10 unique values but got {y}"
            x = data['sequence']
            x = x.to(device)
            y = data['label']
            y = y.to(device)
            logits = network(x)
            # y_pred = torch.argmax(logits, dim=1)
            loss = loss_func(logits, y.unsqueeze(1))
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            train_losses.append(loss.detach())

        print(
            f"Epoch {epoch_idx} train loss: {torch.mean(torch.stack(train_losses))} "
        )

        val_losses = []
        network.eval()
        for data in tqdm.tqdm(val_dataloader):
            x = data['sequence']
            x = x.to(device)
            y = data['label']
            y = y.to(device)
            logits = network(x)
            loss = loss_func(logits, y)

            val_losses.append(loss.detach())

        print(
            f"Epoch {epoch_idx} val loss: {torch.mean(torch.stack(val_losses))}"
        )


if __name__ == '__main__':



    '''
    All parameters are aggregated in one place.
    This is useful for reporting experiment params to experiment tracking software
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--seq_len', type=int, default=4)
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--n_features', type=int, default=35)
    parser.add_argument('--hidden_size', type=int, default=128)
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--dropout', type=int, default=0.2)
    parser.add_argument('--lr', type=float, default=1e-3)

    config = parser.parse_args()
    # config = vars(args)


    train(config=config)