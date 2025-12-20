import torch 
import torch.nn as nn 
import torch.optim as optim
from torchvision import datasets, transforms 
from torch.utils.data import DataLoader 

transform = transforms.Compose([
transforms.ToTensor(),
transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.247, 0.243, 0.261])])

train_dataset = datasets.CIFAR10(root='./data', train=True,download=True, transform=transform)
test_dataset = datasets.CIFAR10(root='./data', train=False, download=True,transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)