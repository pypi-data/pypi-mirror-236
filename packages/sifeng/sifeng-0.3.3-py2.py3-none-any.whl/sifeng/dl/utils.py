import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from math import floor, ceil
from colorama import Fore, Back, Style

import logging
from typing import Optional, Literal, Callable, Union

g_device = "cuda:0" if torch.cuda.is_available() else "cpu"

__all__ = [
    "VerboseBase",
    "stat",
    "dl_trainer",
    "dl_evaluator",
]

class VerboseBase:
    """The base for all Verbosers

    Functions
    ---------
    epoch_end: [int, str] -> Optional[float]:
        Will be called when an epoch ends, now you can summarize your results and output/log your
    evaluation, additionally, you may also return your metric to override early stopping (Note that
    the metric also assumes less being better, so metrics like accuracy should be negatived before
    returning)
    eval_iter: [torch.Tensor, torch.Tensor] -> None:
        Will be called each epoch, and you may calculate whatever metric you want

    """
    def __init__(self):
        pass

    def epoch_end(self,
                  epoch: int,
                  mode: str,
                  ) -> Optional[float]:
        raise NotImplementedError

    def eval_iter(self,
                  yhat: torch.Tensor,
                  y: torch.Tensor
                  ) -> None:
        raise NotImplementedError

def stat(model: torch.nn.Module,
         sort: Literal[":idx", "idx:", ":name", "name:", ":train", "train:", ":params", "params:", ":memory", "memory:"] = "train:",
         howio: Union[Callable, Literal["str"]] = print,
         format: str = "{}",
         ) -> str:
    """Prints analysis for a specific model

    Parameters
    ----------
    model: torch.nn.Module
        the model to be interepted
    sort: Literal[":idx", "idx:", ":name", "name:", ":train", "train:", ":params", "params:", ":memory", "memory:"], deafult `"train:"`
        how to sort the output, a leading comma means ascending and a trailing comma means descending
    howio: Union[Callable, Literal["str"]], default `print`
        how to print out the stats of a model, default to std print
    format: str, default `"{}"`
        The format string for custom formatting output
    """
    def fmt(info, length, place):
        info = str(info)
        if place == "center":
            return " " * floor((length - len(info)) / 2) + info + " " * ceil((length - len(info)) / 2)
        elif place == "left":
            return " " + info + " " * floor(length - len(info) - 1)
        elif place == "right":
            return " " * floor(length - len(info) - 1) + info + " "
    def elafmt(sz, carry, seq, dig):
        idx = 0
        while sz >= carry and idx < len(seq) - 1:
            sz = sz / carry
            idx = idx + 1
        if idx == 0 and seq[idx] == "":
            return "{:d}".format(int(sz))
        elif idx == 0 or int(sz) == sz:
            return "{:d} {}".format(int(sz), seq[idx])
        elif dig == 2:
            return "{:.2f} {}".format(sz, seq[idx])
        elif dig == 4:
            return "{:.4f} {}".format(sz, seq[idx])
    mem_lookup = {
        torch.uint8: 1,
        torch.ByteTensor: 1,
        torch.int8: 1,
        torch.CharTensor: 1,
        torch.int16: 2,
        torch.short: 2,
        torch.ShortTensor: 2,
        torch.float16: 2,
        torch.half: 2,
        torch.HalfTensor: 2,
        torch.int32: 4,
        torch.int: 4,
        torch.IntTensor: 4,
        torch.float: 4,
        torch.float32: 4,
        torch.FloatTensor: 4,
        torch.float64: 8,
        torch.double: 8,
        torch.DoubleTensor: 8,
        torch.int64: 8,
        torch.long: 8,
        torch.LongTensor: 8
    }

    assert isinstance(model, torch.nn.Module), "model is not a torch module."

    info = ""
    model_info, model_params, model_memsz = [], 0, 0
    row_width = (
        6 if sort in [":idx", "idx:"] else 5,
        7 if sort in [":name", "name:"] else 6,
        7,
        8 if sort in [":train", "train:"] else 7,
        9 if sort in [":params", "params:"] else 8,
        9 if sort in [":memory", "memory:"] else 8,
    )
    for idx, (name, w_variable) in enumerate(model.named_parameters()):
        shape = str(w_variable.shape)
        params = 1
        for dim_size in w_variable.shape:
            params = params * dim_size
        model_params = model_params + params
        model_memsz = model_memsz + mem_lookup[w_variable.dtype] * params
        train = "True" if w_variable.requires_grad else "False"
        row_width = (max(row_width[0], len(str(idx)) + 2),
                     max(row_width[1], len(str(name)) + 2),
                     max(row_width[2], len(str(shape)) + 2),
                     max(row_width[3], len(train) + 2),
                     max(row_width[4], len(elafmt(params, 1000, ["", "K", "M", "B", "T"], 2)) + 2),
                     max(row_width[5], len(elafmt(mem_lookup[w_variable.dtype] * params, 1024, ["Bytes", "KiB", "MiB", "GiB", "TiB"], 2)) + 2),
                     )
        model_info.append((idx, name, shape, train, params, mem_lookup[w_variable.dtype] * params))

    assert sort in [":idx", "idx:", ":name", "name:", ":train", "train:", ":params", "params:", ":memory", "memory:"], \
        "Unsupported sorting direction."
    if sort == ":idx":
        model_info.sort(key=lambda x: (x[0]), reverse=False)
    elif sort == "idx:":
        model_info.sort(key=lambda x: (x[0]), reverse=True)
    elif sort == ":name":
        model_info.sort(key=lambda x: (x[1], x[0]), reverse=False)
    elif sort == "name:":
        model_info.sort(key=lambda x: (x[1], x[0]), reverse=True)
    elif sort == ":train":
        model_info.sort(key=lambda x: (x[3], x[0]), reverse=False)
    elif sort == "train:":
        model_info.sort(key=lambda x: (x[3], x[0]), reverse=True)
    elif sort == ":params":
        model_info.sort(key=lambda x: (x[4], x[0]), reverse=False)
    elif sort == "params:":
        model_info.sort(key=lambda x: (x[4], x[0]), reverse=True)
    elif sort == ":memory":
        model_info.sort(key=lambda x: (x[5], x[0]), reverse=False)
    elif sort == "memory:":
        model_info.sort(key=lambda x: (x[5], x[0]), reverse=True)

    info = info + "┌" + "─" * row_width[0] + \
                  "┬" + "─" * row_width[1] + \
                  "┬" + "─" * row_width[2] + \
                  "┬" + "─" * row_width[3] + \
                  "┬" + "─" * row_width[4] + \
                  "┬" + "─" * row_width[5] + "┐\n"
    info = info + "│{}│{}│{}│{}│{}│{}│\n".format(
        fmt(sort if sort in [":idx", "idx:"] else "idx", row_width[0], "center"),
        fmt(sort if sort in [":name", "name:"] else "name", row_width[1], "center"),
        fmt("shape", row_width[2], "center"),
        fmt(sort if sort in [":train", "train:"] else "trainable", row_width[3], "center"),
        fmt(sort if sort in [":params", "params:"] else "params", row_width[4], "center"),
        fmt(sort if sort in [":memory", "memory:"] else "memory", row_width[5], "center"),
    )
    info = info + "├" + "-" * row_width[0] + \
                  "┼" + "-" * row_width[1] + \
                  "┼" + "-" * row_width[2] + \
                  "┼" + "-" * row_width[3] + \
                  "┼" + "-" * row_width[4] + \
                  "┼" + "-" * row_width[5] + "┤\n"
    if len(model_info) != 0:
        for item in model_info:
            if item[3] == "True":
                info = info + "│{}{}│{}│{}│{}│{}│{}{}│\n".format(
                    Style.NORMAL,
                    Fore.GREEN + fmt(item[0], row_width[0], "right") + Fore.RESET,
                    Fore.GREEN + fmt(item[1], row_width[1], "left") + Fore.RESET,
                    Fore.GREEN + fmt(item[2], row_width[2], "left") + Fore.RESET,
                    Fore.GREEN + fmt(item[3], row_width[3], "left") + Fore.RESET,
                    Fore.GREEN + fmt(elafmt(item[4], 1000, ["", "K", "M", "B", "T"], 2), row_width[4], "left") + Fore.RESET,
                    Fore.GREEN + fmt(elafmt(item[5], 1024, ["Bytes", "KiB", "MiB", "GiB", "TiB"], 2), row_width[5], "left") + Fore.RESET,
                    Fore.RESET + Back.RESET + Style.RESET_ALL,
                )
            elif item[3] == "False":
                info = info + "│{}{}│{}│{}│{}│{}│{}{}│\n".format(
                    Style.DIM,
                    Fore.RED + fmt(item[0], row_width[0], "right") + Fore.RESET,
                    Fore.RED + fmt(item[1], row_width[1], "left") + Fore.RESET,
                    Fore.RED + fmt(item[2], row_width[2], "left") + Fore.RESET,
                    Fore.RED + fmt(item[3], row_width[3], "left") + Fore.RESET,
                    Fore.RED + fmt(elafmt(item[4], 1000, ["", "K", "M", "B", "T"], 2), row_width[4], "left") + Fore.RESET,
                    Fore.RED + fmt(elafmt(item[5], 1024, ["Bytes", "KiB", "MiB", "GiB", "TiB"], 2), row_width[5], "left"),
                    Fore.RESET + Back.RESET + Style.RESET_ALL,
                )
    else:
        info = info + "│{}│\n".format(fmt("No Parameters", row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5, "center"))
    info = info + "├" + "-" * row_width[0] + \
                  "┴" + "-" * row_width[1] + \
                  "┴" + "-" * row_width[2] + \
                  "┴" + "-" * row_width[3] + \
                  "┴" + "-" * row_width[4] + \
                  "┴" + "-" * row_width[5] + "┤\n"
    info = info + "│{}│\n".format(fmt("Model params: {}".format(elafmt(model_params, 1000, ["", "K", "M", "B", "T"], 4)), row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5, "left"))
    info = info + "│{}│\n".format(fmt("Model memory: {}".format(elafmt(model_memsz, 1024, ["Bytes", "KiB", "MiB", "GiB", "TiB"], 4)), row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5, "left"))
    info = info + "└" + "-" * (row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5) + "┘"

    if howio == "str":
        return format.format(info)
    elif callable(howio):
        howio(format.format(info))

class dl_trainer:
    """The torch model trainer

    Parameters
    ----------
    model: torch.nn.Module
        The model to be trained
    loss: Callable[[torch.nn.tensor, torch.nn.tensor], torch.tensor]
        The loss function
    optimizer: torch.optim.Optimizer
        The BP optimizer
    epoch: int
        Number of epochs to train
    lr: float,
        The learning rate
    lr_scheduler: Optional[Callable[[int], float]], default `None`
        A function that computes a multiplicative factor given an integer parameter epoch, `None`
    to disable
    batch_size: Union[int, Callable[[int], int]], default `64`
        A function that computes batch size given an integer parameter epoch, or a constant batch
    size, only enable when passing a
    `torch.utils.data.Dataset` to the trainer
    mini_batch: Union[int, Callable[[int], int]], default `1`
        A function that computes mini batch size given an integer parameter epoch, or a constant
    mini batch size, useful when you have a small GPU
    memory size but want much larger batch sizes
    patience: int, default `-1`:
        The patience parameter for early stopping, set to `-1` to disable
    delta: float, default `0`:
        The minimal loss improvement required for the model to be considered improving
    logger: Optional[logging.Logger], default `None`
        A logger for debug-level information
    verbose: Optional[VerboseBase], default `None`
        The verbose evaluator for epoch level data
    eval_train: bool, default `False`
        Whether to eval the train set every epoch
    device: torch.device, default `"cuda:0" if torch.cuda.is_available() else "cpu"`
        On which device to train the model
    *args, **kwargs:
        Additional args for optimizer
    """
    def __init__(self,
                 model: nn.Module,
                 loss: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
                 optimizer: torch.optim.Optimizer,
                 epoch: int,
                 lr: float,
                 lr_scheduler: Optional[Callable[[int], float]] = None,
                 batch_size: Union[int, Callable[[int], int]] = 64,
                 mini_batch: Union[int, Callable[[int], int]] = 1,
                 patience: int = -1,
                 delta: float = 0,
                 logger: Optional[logging.Logger] = None,
                 verbose: Optional[VerboseBase] = None,
                 eval_train: bool = False,
                 device: torch.device = "cuda:0" if torch.cuda.is_available() else "cpu",
                 *args, **kwargs,
                 ) -> None:
        self.model = model
        self.loss = loss
        self.lr = lr
        self.optimizer = optimizer(filter(lambda layer: layer.requires_grad, self.model.parameters()), lr=lr, *args, **kwargs)
        self.epoch = epoch
        self.lr_lambda = lr_scheduler
        self.lr_scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda=lr_scheduler) if lr_scheduler is not None else None
        self.batch_size = batch_size
        self.mini_batch = mini_batch
        self.patience = patience
        self.delta = delta
        self.logger = logger
        self.verbose = verbose
        self.eval_train = eval_train
        self.device = device

    def train(self,
              train_data: Union[Dataset, DataLoader],
              valid_data: Union[Dataset, DataLoader],
              *args, **kwargs) -> None:
        """Train the model

        Parameters
        ----------
        train_data: Union[Dataset, DataLoader]
            The training data
        valid_date: Union[Dataset, DataLoader]
            The validation data
        *args, **kwargs:
            Additional parameters for `torch.utils.data.DataLoader` if passing a `torch.utils.data.Dataset`
        """
        self.logger.info("Begin training model. Training params: loss = {}; optimizer = {}.".format(self.loss, self.optimizer)) if self.logger else None # INFO-LOG
        stat(self.model, howio=self.logger.debug, format="Model params:\n{}") if self.logger else None # DEBUG-LOG
        torch.cuda.empty_cache()
        self.model.to(self.device)
        best_loss, best_metric, patience = np.inf, np.inf, self.patience
        self.model.to(self.device)
        for EPOCH in tqdm(range(self.epoch), desc="training", unit="epoch"):
            self.logger.info("Start training@EPOCH {}. Current params: lr = {}{}{}; patience = {}/{}".format(EPOCH, self.lr, " * {}".format(self.lr_lambda(EPOCH)) if self.lr_lambda else "", "; batch size = {} * {}".format(self.batch_size(EPOCH) if callable(self.batch_size) else self.batch_size, self.mini_batch(EPOCH) if callable(self.mini_batch) else self.mini_batch) if isinstance(train_data, Dataset) else "", patience, self.patience)) if self.logger else None # INFO-LOG
            if patience > 0:
                patience = patience - 1
            self.train_epoch(EPOCH, train_data, *args, **kwargs)
            if self.eval_train:
                loss = self.eval_epoch(EPOCH, train_data, *args, **kwargs)
                self.logger.info(f"Finished train-eval@EPOCH {EPOCH}, current loss = {loss:.8f}") if self.logger else None # INFO-LOG
                if self.verbose is not None:
                    metric = self.verbose.epoch_end(EPOCH, "train")
            loss = self.eval_epoch(EPOCH, valid_data, *args, **kwargs)
            if loss < best_loss - self.delta:
                self.logger.info(f"Finished validing@EPOCH {EPOCH}, current loss = {loss:.8f}, loss update {best_loss:.8f} -> {loss:.8f}") if self.logger else None # INFO-LOG
                best_loss = loss
                patience = self.patience
            else:
                self.logger.info(f"Finished validing@EPOCH {EPOCH}, current loss = {loss:.8f}") if self.logger else None # INFO-LOG
            if self.verbose is not None:
                metric = self.verbose.epoch_end(EPOCH, "valid")
                if metric is not None and metric < best_metric:
                    self.logger.info(f"Verbose metric: {metric:.8f}, metric update {best_metric:.8f} -> {metric:.8f}.") if self.logger else None # INFO LOG
                    best_metric = metric
                    patience = self.patience
                else:
                    self.logger.info(f"Verbose metric: {metric:.8f}.") if self.logger else None # INFO LOG
            if patience == 0:
                break

            if self.lr_scheduler is not None:
                self.lr_scheduler.step()

    def train_epoch(self,
                    epoch: int,
                    train_data: Union[Dataset, DataLoader],
                    *args, **kwargs
                    ) -> None:
        if isinstance(train_data, DataLoader):
            train_loader = train_data
        elif isinstance(self.batch_size, int):
            train_loader = DataLoader(train_data, batch_size=self.batch_size, *args, **kwargs)
        elif callable(self.batch_size):
            train_loader = DataLoader(train_data, batch_size=self.batch_size(epoch), *args, **kwargs)
        else:
            raise ValueError
        mini_batch, countr = self.mini_batch if isinstance(self.mini_batch, int) else self.mini_batch(epoch), 0
        self.model.train()
        for idx, packet in enumerate(train_loader):
            x, y = packet[0].to(self.device), packet[1].to(self.device)
            yhat = self.model(x)
            loss = self.loss(yhat, y) / mini_batch
            if countr == 0:
                self.optimizer.zero_grad()
            loss.backward()
            countr = countr + 1
            if countr == mini_batch:
                self.optimizer.step()
                self.logger.debug("Training iter {}, loss = {:.8f}, optimizer stepped.".format(idx, loss.data * mini_batch)) if self.logger else None # DEBUG-LOG
                countr = 0
            else:
                self.logger.debug("Training iter {}, loss = {:.8f}.".format(idx, loss.data * mini_batch)) if self.logger else None # DEBUG-LOG

    def eval_epoch(self,
                   epoch: int,
                   valid_data: Union[Dataset, DataLoader],
                   *args, **kwargs
                   ) -> float:
        if isinstance(valid_data, DataLoader):
            valid_loader = valid_data
        elif isinstance(self.batch_size, int):
            valid_loader = DataLoader(valid_data, batch_size=self.batch_size, *args, **kwargs)
        elif callable(self.batch_size):
            valid_loader = DataLoader(valid_data, batch_size=self.batch_size(epoch), *args, **kwargs)
        else:
            raise ValueError
        accum_loss, accum_batch = 0, 0
        self.model.eval()
        with torch.no_grad():
            for x, y in valid_loader:
                x, y = x.to(self.device), y.to(self.device)
                yhat = self.model(x)
                loss = self.loss(yhat, y)
                accum_loss = accum_loss + loss.data * y.shape[0]
                accum_batch = accum_batch + y.shape[0]
                if self.verbose is not None:
                    self.verbose.eval_iter(yhat=yhat, y=y)
        return accum_loss / accum_batch

class dl_evaluator:
    """The torch model evaluator

    Parameters
    ----------
    model: torch.nn.Module
        The trained model.
    verbose: Optional[VerboseBase], default `None`
        The verbose evaluator for infomation output
    """
    def __init__(self,
                 model: nn.Module,
                 verbose: Optional[VerboseBase] = None,
                 ) -> None:
        self.model = model
        self.verbose = verbose

    def eval(self,
             valid_data: Union[Dataset, DataLoader],
             *args, **kwargs,
             ) -> float:
        if isinstance(valid_data, DataLoader):
            valid_loader = valid_data
        else:
            valid_loader = DataLoader(valid_data, *args, **kwargs)
        accum_loss, accum_batch = 0, 0
        self.model.eval()
        with torch.no_grad():
            for x, y in valid_loader:
                x, y = x.to(self.device), y.to(self.device)
                yhat = self.model(x)
                loss = self.loss(yhat, y)
                accum_loss = accum_loss + loss.data * y.shape[0]
                accum_batch = accum_batch + y.shape[0]
                if self.verbose is not None:
                    self.verbose.eval_iter(yhat=yhat, y=y)
        self.verbose.epoch_end(0, "eval")
        return accum_loss / accum_batch
