# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__()
        # certain definitions
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 6, kernel_size=5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer3 = nn.Flatten()
        self.layer4 = nn.Sequential(
            nn.Linear(400, 256),
            nn.ReLU())
        self.layer5 = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU())
        self.layer6 = nn.Linear(128, 100)


    def forward(self, x):
        shape_dict = {}
        # certain operations
        out = self.layer1(x)
        shape_dict[1] = list(out.size())
        out = self.layer2(out)
        shape_dict[2] = list(out.size())
        out = self.layer3(out)
        shape_dict[3] = list(out.size())
        out = self.layer4(out)
        shape_dict[4] = list(out.size())
        out = self.layer5(out)
        shape_dict[5] = list(out.size())
        out = self.layer6(out)
        shape_dict[6] = list(out.size())
        
        return out, shape_dict


def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    model = LeNet()

    out, shape = model.forward(torch.randn(1, 3, 32, 32))
    model_params = 0

    #trainable parameters in convolutional layers
    lastChannelNum = 3
    currChannelNum = shape[1][1]
    kernelSize = 5

    # + 1 for bias terms
    model_params += (lastChannelNum*kernelSize*kernelSize + 1) * currChannelNum

    lastChannelNum = currChannelNum
    currChannelNum = shape[2][1]
    
    model_params += (lastChannelNum*kernelSize*kernelSize + 1) * currChannelNum

    #linear layer params
    for i in range(3, 6):
        lastLayer = shape[i][1]
        currLayer = shape[i+1][1]
        # + 1 for bias
        model_params += (lastLayer + 1) * currLayer

    return model_params / 1000000


def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        ###################################
        # fill in the standard training loop of forward pass,
        # backward pass, loss computation and optimizer step
        ###################################

        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        # Uncomment the below line after you fill block 1 and 2
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc
