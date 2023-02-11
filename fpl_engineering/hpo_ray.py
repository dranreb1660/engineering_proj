import wandb
import torch
import os, sys
import pytorch_lightning as pl
from pytorch_lightning.callbacks.progress import TQDMProgressBar
# from pytorch_lightning.loggers import WandbLogger
import ray
from ray import tune, air
# from ray.air.integrations.wandb import setup_wandb
from ray.tune.integration.wandb import wandb_mixin
from ray.tune.integration.pytorch_lightning import TuneReportCallback
from ray.tune.schedulers import ASHAScheduler, PopulationBasedTraining
from ray.tune import CLIReporter

import getpass

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from fpl_engineering.data.lit_data_module import FPLDataModule
from fpl_engineering.models.lit_models import FPLLSTMRegressor

from fpl_engineering.utils import get_project_root
project_root = str(get_project_root())
log_dir = project_root+'/logs'


static_config = {'n_features': 35, 'epochs':40, 'device': 'cuda' if torch.cuda.is_available() else 'cpu'}


@wandb_mixin
def sweep_iteration(config, static_config = static_config):

    project_root = str(get_project_root())
    log_dir = project_root+'/logs'


    # set up W&B logger
    wandb.init(config=config)    # required to have access to `wandb.config`
    config = wandb.config

    # setup data
    data_module = FPLDataModule(batch_size=config.batch_size, seq_len=config.seq_len, download_data=False, data_dir='data')


    # setup model - note how we refer to sweep parameters with wandb.config
    model = FPLLSTMRegressor(n_features= static_config['n_features'], hidden_size=config.hidden_size, seq_len=config.seq_len, 
                            batch_size=config.batch_size, num_layers=config.n_layers, dropout=config.dropout,learning_rate=config.lr)


    # early_stopping_callback = EarlyStopping(monitor='val_loss', patience=4, verbose=True)
    progress_bar = TQDMProgressBar(refresh_rate=1)

    # logger = [WandbLoggerCallback]

    metrics = {"loss": "val_loss"}
    callbacks = [TuneReportCallback(metrics, on="validation_end"), progress_bar]
    # setup Trainer
    trainer = pl.Trainer(accelerator =static_config['device'],
                        max_epochs = static_config['epochs'],
                        callbacks = callbacks,
                        precision=16)

    # train
    trainer.fit(model, datamodule=data_module)


def tune_asha(static_config=static_config):

  tr_config = {  

      "dropout":tune.grid_search([0.3, 0.4, 0.5, 0.75, 0.85]),
      "hidden_size":tune.grid_search([64, 128, 256, 512]),
      "batch_size":tune.grid_search([64, 128, 256, 512]),
      "lr":tune.grid_search([0.0001,0.0005, 0.001,0.005, 0.01, 0.1]),
      "seq_len":tune.grid_search([4,5]),
      "n_layers":tune.grid_search([1,2]),
      "wandb": {
          "project": "FPL",
          "api_key":api_key,
      }
      }

  scheduler = ASHAScheduler(
      max_t=static_config['epochs'],
      grace_period=1,
      reduction_factor=2)

  reporter = CLIReporter(
      parameter_columns=["dropout", "hidden_size", "lr", "batch_size", 'n_layers','seq_len' ],
      metric_columns=["loss","training_iteration"])

  train_fn_with_parameters = tune.with_parameters(sweep_iteration,
                                                    static_config=static_config)
  
  resources_per_trial = {"cpu": 1, "gpu": 0}

  tuner = tune.Tuner(
      tune.with_resources(
          train_fn_with_parameters,
          resources=resources_per_trial
      ),
      tune_config=tune.TuneConfig(
          metric="loss",
          mode="min",
          scheduler=scheduler,
          num_samples=10,
      ),
      run_config=air.RunConfig(
          name="tune_fpl_asha",
          progress_reporter=reporter,
      ),
      param_space=tr_config,
  )

  results = tuner.fit()

  # analysis = tune.run(
  #         sweep_iteration,
  #         config = tr_config,
  #     )
  print("Best hyperparameters found were: ", results.get_best_result().config)



if __name__ == '__main__':
    api_key = '0e7613d70774bd853ddb2dc316968c77437977be'
    ray.init()
    tune_asha(static_config=static_config)