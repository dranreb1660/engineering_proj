import wandb
import torch, sys, os
import pytorch_lightning as pl
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from pytorch_lightning.loggers import WandbLogger

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


from fpl_engineering.data.lit_data_module import FPLDataModule
from fpl_engineering.models.lit_models import FPLLSTMRegressor

from fpl_engineering.utils import get_project_root
project_root = str(get_project_root())
log_dir = project_root+'/logs'

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu'

sweep_config = {
  "method": "grid",   # grid search
  "metric": {           # We want to minimize val_loss
      "name": "val_loss",
      "goal": "minimize"
  },
  "parameters": {

        "batch_size": {
            # Choose from pre-defined values
            "values": [64, 128, 256]
        },
        
        "seq_len": {
            # Choose from pre-defined values
            "values": [5] 
        },
        "n_layers": {
            # Choose from pre-defined values
            "values": [2] 
        },

        "hidden_size": {
            # Choose from pre-defined values
            "values": [128, 256]
        },

        "lr": {
        # a flat distribution between 0 and 0.1
            'values': [0.00005, 0.001,0.005] # ,
        },

        "dropout": {
            # Choose from pre-defined values
            "values": [ 0.75, 0.85] #
        },
    },

}

static_config = {'n_features': 35, 'epochs':50, 'data_dir': 'data'}

def sweep_iteration():

    # set up W&B logger
    wandb.init(config=sweep_config)    # required to have access to `wandb.config`
    config = wandb.config

    # setup data
    data_module = FPLDataModule(batch_size=config.batch_size, seq_len=config.seq_len, download_data=False, data_dir=static_config['data_dir'])


    # setup model - note how we refer to sweep parameters with wandb.config
    model = FPLLSTMRegressor(n_features= static_config['n_features'], hidden_size=config.hidden_size, seq_len=config.seq_len, 
                            batch_size=config.batch_size, num_layers=config.n_layers, dropout=config.dropout,learning_rate=config.lr)


    # early_stopping_callback = EarlyStopping(monitor='val_loss', patience=4, verbose=True)
    progress_bar = TQDMProgressBar(refresh_rate=1)

    logger = WandbLogger(save_dir=log_dir, project='FPL')
    callbacks = [progress_bar]

    # setup Trainer
    trainer = pl.Trainer(accelerator = device,
                        max_epochs = static_config['epochs'],
                        logger= logger,
                        callbacks = callbacks,
                        log_every_n_steps=20,
                        precision=16)

    # train
    trainer.fit(model, datamodule=data_module)



if __name__ == '__main__':

    '''
    All parameters are aggregated in one place.
    This is useful for reporting experiment params to experiment tracking software
    '''

    sweep_id = wandb.sweep(sweep_config, project="FPL")
    wandb.agent(sweep_id, sweep_iteration,project='FPL' ,count=200)
    wandb.finish()
