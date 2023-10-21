import torch
from torch import nn
from math import floor, ceil
from colorama import Fore, Back, Style

from typing import Literal

__all__ = [
    "stat",
]

def stat(model: torch.nn.Module,
         sort: Literal[":idx", "idx:", ":name", "name:", ":train", "train:", ":params", "params:", ":memory", "memory:"] = "train:",
         ) -> str:
    """Prints analysis for a specific model

    Parameters
    ----------
    model: torch.nn.Module
        the model to be interepted
    sort: Literal[":idx", "idx:", ":name", "name:", ":train", "train:", ":params", "params:", ":memory", "memory:"], deafult `"train:"`
        how to sort the output, a leading comma means ascending and a trailing comma means descending
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
        model_info.sort(key=lambda x: (x[1], -x[0]), reverse=True)
    elif sort == ":train":
        model_info.sort(key=lambda x: (x[3], x[0]), reverse=False)
    elif sort == "train:":
        model_info.sort(key=lambda x: (x[3], -x[0]), reverse=True)
    elif sort == ":params":
        model_info.sort(key=lambda x: (x[4], x[0]), reverse=False)
    elif sort == "params:":
        model_info.sort(key=lambda x: (x[4], -x[0]), reverse=True)
    elif sort == ":memory":
        model_info.sort(key=lambda x: (x[5], x[0]), reverse=False)
    elif sort == "memory:":
        model_info.sort(key=lambda x: (x[5], -x[0]), reverse=True)

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
    info = info + "├" + "─" * row_width[0] + \
                  "┼" + "─" * row_width[1] + \
                  "┼" + "─" * row_width[2] + \
                  "┼" + "─" * row_width[3] + \
                  "┼" + "─" * row_width[4] + \
                  "┼" + "─" * row_width[5] + "┤\n"
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
    info = info + "├" + "─" * row_width[0] + \
                  "┴" + "─" * row_width[1] + \
                  "┴" + "─" * row_width[2] + \
                  "┴" + "─" * row_width[3] + \
                  "┴" + "─" * row_width[4] + \
                  "┴" + "─" * row_width[5] + "┤\n"
    info = info + "│{}│\n".format(fmt("Model params: {}".format(elafmt(model_params, 1000, ["", "K", "M", "B", "T"], 4)), row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5, "left"))
    info = info + "│{}│\n".format(fmt("Model memory: {}".format(elafmt(model_memsz, 1024, ["Bytes", "KiB", "MiB", "GiB", "TiB"], 4)), row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5, "left"))
    info = info + "└" + "─" * (row_width[0] + row_width[1] + row_width[2] + row_width[3] + row_width[4] + row_width[5] + 5) + "┘"

    return info
