import torch
import torchvision
import torchvision.transforms as transforms
import os
import torch.optim as optim
import numpy as np
import random

import copy
import torch.optim as optim
# import timm


import copy
import math
import random
import time
from collections import OrderedDict, defaultdict
from typing import Union, List

import numpy as np
import torch
from matplotlib import pyplot as plt
from torch import nn
from torch.optim import *
from torch.optim.lr_scheduler import *
from torch.utils.data import DataLoader
# from torchprofile import profile_macs
from torchvision.datasets import *
from torchvision.transforms import *
from tqdm.auto import tqdm

# from torchprofile import profile_macs

# assert torch.cuda.is_available(), \
# "The current runtime does not have CUDA support." \
# "Please go to menu bar (Runtime - Change runtime type) and select GPU"


# import timm

import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
# !pip uninstall sconce
# !pip install git+https://github.com/satabios/sconce --upgrade


class VGG(nn.Module):
  ARCH = [64, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M']

  def __init__(self) -> None:
    super().__init__()

    layers = []
    counts = defaultdict(int)

    def add(name: str, layer: nn.Module) -> None:
      layers.append((f"{name}{counts[name]}", layer))
      counts[name] += 1

    in_channels = 3
    for x in self.ARCH:
      if x != 'M':
        # conv-bn-relu
        add("conv", nn.Conv2d(in_channels, x, 3, padding=1, bias=False))
        add("bn", nn.BatchNorm2d(x))
        add("relu", nn.ReLU(True))
        in_channels = x
      else:
        # maxpool
        add("pool", nn.MaxPool2d(2))
    add("avgpool", nn.AvgPool2d(2))
    self.backbone = nn.Sequential(OrderedDict(layers))
    self.classifier = nn.Linear(512, 10)

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    # backbone: [N, 3, 32, 32] => [N, 512, 2, 2]
    x = self.backbone(x)

    # avgpool: [N, 512, 2, 2] => [N, 512]
    # x = x.mean([2, 3])
    x = x.view(x.shape[0], -1)

    # classifier: [N, 512] => [N, 10]
    x = self.classifier(x)
    return x

# # checkpoint_url = "./vgg.cifar.pretrained.pth"
checkpoint = torch.load("./vgg.cifar.pretrained.pth", map_location="cpu")
model = VGG().cuda()
# # print(f"=> loading checkpoint '{checkpoint_url}'")
model.load_state_dict(checkpoint['state_dict'])
# recover_model = lambda : model.load_state_dict(checkpoint['state_dict'])

class Net(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Conv2d(3, 4, 3)
    self.bn1 = nn.BatchNorm2d(4)
    self.pool = nn.MaxPool2d(2, 2)
    self.conv2 = nn.Conv2d(4, 6, 3)
    self.bn2 = nn.BatchNorm2d(6)
    self.fc1 = nn.Linear(6 * 6 * 6, 32)
    self.fc2 = nn.Linear(32, 10)

  def forward(self, x):
    x = self.pool(self.bn1(F.relu(self.conv1(x))))
    x = self.pool(self.bn2(F.relu(self.conv2(x))))
    x = torch.flatten(x, 1)
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return x


# from torchvision.transforms import Compose
image_size = 32
transforms = {
    "train": transforms.Compose([
        RandomCrop(image_size, padding=4),
        RandomHorizontalFlip(),
        ToTensor(),
    ]),
    "test": ToTensor(),
}
dataset = {}
for split in ["train", "test"]:
  dataset[split] = CIFAR10(
    root="data/cifar10",
    train=(split == "train"),
    download=True,
    transform=transforms[split],
  )
dataloader = {}
for split in ['train', 'test']:
  dataloader[split] = DataLoader(
    dataset[split],
    batch_size=512,
    shuffle=(split == 'train'),
    num_workers=0,
    pin_memory=True,
  )



from sconce import sconce


sconces = sconce()
sconces.device = "cuda"
sconces.epochs =1
sconces.model= model
sconces.criterion = nn.CrossEntropyLoss()
sconces.optimizer= optim.Adam(sconces.model.parameters(), lr=1e-4)
sconces.scheduler= optim.lr_scheduler.CosineAnnealingLR(sconces.optimizer, T_max=200)
sconces.dataloader = dataloader
sconces.prune_mode = "CWP"
sconces.channel_pruning_ratio = 0.80
sconces.bitwidth = 4
sconces.compress()


# dummy_input = torch.randn(1, 3, 32, 32).cuda()
# original_mac = sconces.get_model_macs(model, dummy_input)
# pruned_model = sconces.channel_prune(model, prune_ratio=0.90)
# pruned_macs = sconces.get_model_macs(pruned_model, dummy_input)
# print(original_mac,pruned_macs)
