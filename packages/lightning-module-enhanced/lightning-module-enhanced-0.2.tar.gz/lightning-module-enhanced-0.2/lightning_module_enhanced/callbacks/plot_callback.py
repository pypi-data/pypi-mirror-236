"""Module to create a plot callback for train and/or validation for a Lightning Module"""
from typing import Callable
from pathlib import Path
from overrides import overrides
from pytorch_lightning import Trainer, LightningModule
from pytorch_lightning.callbacks import Callback
import torch as tr

from ..logger import logger

class PlotCallbackGeneric(Callback):
    """Plot callback impementation. For each train/validation epoch, create a dir under logger_dir/pngs/epoch_X"""
    def __init__(self, plot_callback: Callable):
        self.plot_callback = plot_callback

    @staticmethod
    def _get_out_dir(trainer: Trainer, dir_name: str) -> Path:
        """Gets the output directory as '/path/to/log_dir/pngs/train_or_val/epoch_N/' """
        if len(trainer.loggers) == 0:
            return None
        out_dir = Path(f"{trainer.loggers[0].log_dir}/pngs/{dir_name}/{trainer.current_epoch + 1}")
        out_dir.mkdir(exist_ok=True, parents=True)
        return out_dir

    def _do_call(self, trainer: Trainer, pl_module: LightningModule, batch, batch_idx, key):
        if batch_idx != 0:
            return
        if len(trainer.loggers) == 0:
            logger.warning("No lightning logger found. Not calling PlotCallbacks()")
            return
        out_dir = PlotCallbackGeneric._get_out_dir(trainer, key)
        with tr.no_grad():
            y = pl_module.forward(batch)
        self.plot_callback(model=pl_module, batch=batch, y=y, out_dir=out_dir)

    @overrides
    # pylint: disable=unused-argument
    def on_validation_batch_end(self, trainer: Trainer, pl_module: LightningModule,
                                outputs, batch, batch_idx: int, dataloader_idx: int = 0) -> None:
        self._do_call(trainer, pl_module, batch, batch_idx, "validation")

    @overrides
    # pylint: disable=unused-argument
    def on_train_batch_end(self, trainer: Trainer, pl_module: LightningModule,
                           outputs, batch, batch_idx: int, unused: int = 0):
        self._do_call(trainer, pl_module, batch, batch_idx, "train")

    @overrides
    def on_test_batch_end(self, trainer: Trainer, pl_module: LightningModule,
                          outputs, batch, batch_idx: int, dataloader_idx: int = 0) -> None:
        self._do_call(trainer, pl_module, batch, batch_idx, "test")

class PlotCallback(PlotCallbackGeneric):
    """Above implementation + assumption about data/labels keys"""
    @overrides
    def _do_call(self, trainer, pl_module, batch, batch_idx, key):
        if batch_idx != 0:
            return
        if len(trainer.loggers) == 0:
            logger.warning("No lightning logger found. Not calling PlotCallbacks()")
            return

        out_dir = PlotCallbackGeneric._get_out_dir(trainer, key)
        x, gt = batch["data"], batch["labels"]
        with tr.no_grad():
            y = pl_module.forward(x)

        self.plot_callback(x=x, y=y, gt=gt, out_dir=out_dir, model=pl_module)
