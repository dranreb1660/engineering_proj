import argparse
import wandb
import torch
import pickle
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from pytorch_lightning.loggers import WandbLogger

from fpl_engineering.data.lit_data_module import FPLDataModule
from fpl_engineering.models.lit_models import FPLLSTMRegressor

from fpl_engineering.utils import get_project_root

project_root = str(get_project_root())
log_dir = project_root+'/logs'

# device = 'cpu'
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def train(config, run_name):

    with wandb.init(project='FPL', job_type='train', config=config) as run:
        config = wandb.config

        data_module = FPLDataModule(batch_size=config.batch_size, seq_len= config.seq_len, download_data=False, data_dir=config.data_dir, n_features=config.n_features)

        model = FPLLSTMRegressor(n_features= config.n_features, hidden_size=config.hidden_size, seq_len=config.seq_len, 
        batch_size=config.batch_size, num_layers=config.n_layers, dropout=config.dropout,learning_rate=config.lr)

        # set up W&B logger
        checkpoint_callback = ModelCheckpoint(
        dirpath=log_dir+'/checkpoints',
        filename='best_checkpoint',
        save_top_k=1,
        verbose=True,
        monitor='val_loss',
        mode='min'
        )
        progress_bar = TQDMProgressBar()
        logger = WandbLogger(name=run_name, save_dir=log_dir, project='FPL')

        callbacks = [checkpoint_callback, progress_bar]

        # setup Trainer
        trainer = pl.Trainer(accelerator = device,
                            max_epochs = config.epochs,
                            logger= logger,
                            callbacks = callbacks,
                            log_every_n_steps=20,
                            precision=16)

        # train
        trainer.fit(model, datamodule=data_module)
        print(trainer.checkpoint_callback.best_model_path)

        model_artifact = wandb.Artifact(name='trained-model', type='model', 
                                        description='trained-lstm model',
                                        metadata=dict(config))

        best_model = FPLLSTMRegressor.load_from_checkpoint(trainer.checkpoint_callback.best_model_path)
        torch.save(best_model,project_root+'/models/lstm_model.pth')
        model_artifact.add_file(project_root+'/models/lstm_model.pth')


        input_sample = torch.randn(1, config.seq_len, config.n_features)
        best_model.to_onnx(project_root+'/models/lstm_model.onnx',input_sample=input_sample ,export_params=True,
                input_names = ['input'],  
                output_names = ['output'], 
                dynamic_axes={'input' : {0 : 'batch_size'},'output' : {0 : 'batch_size'}})
                
        model_artifact.add_file(project_root+'/models/lstm_model.onnx')

        run.log_artifact(model_artifact)
        # wandb.save('trained_model.pth')
        
        wandb.finish()
        with open(project_root+'/models/scaler.pkl', 'wb') as handle:
            pickle.dump(data_module.scaler, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return trainer, data_module


if __name__ == '__main__':

    '''
    All parameters are aggregated in one place.
    This is useful for reporting experiment params to experiment tracking software
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--seq_len', type=int, default=5)
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--batch_size', type=int, default=256)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--n_features', type=int, default=35)
    parser.add_argument('--hidden_size', type=int, default=128)
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--dropout', type=float, default=0.3)
    parser.add_argument('--lr', type=float, default=1e-4)

    args = parser.parse_args()
    config = vars(args)


    train(config=config, run_name='run_001')
