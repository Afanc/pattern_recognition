"""
CNN with 3 conv layers and a fully connected classification layer
PATTERN RECOGNITION EXERCISE:
Fix the three lines below marked with PR_FILL_HERE
"""

import torch
import torch.nn as nn
import utils
import matplotlib.pyplot as plt
import numpy as np

class Flatten(nn.Module):
    """
    Flatten a convolution block into a simple vector.

    Replaces the flattening line (view) often found into forward() methods of networks. This makes it
    easier to navigate the network with introspection
    """
    def forward(self, x):
        x = x.view(x.size()[0], -1)
        return x


class PR_CNN(nn.Module):
    """
    Simple feed forward convolutional neural network

    Attributes
    ----------
    expected_input_size : tuple(int,int)
        Expected input size (width, height)
    conv1 : torch.nn.Sequential
    conv2 : torch.nn.Sequential
    conv3 : torch.nn.Sequential
        Convolutional layers of the network
    fc : torch.nn.Linear
        Final classification fully connected layer

    """

    def __init__(self, **kwargs):
        """
        Creates an CNN_basic model from the scratch.

        Parameters
        ----------
        output_channels : int
            Number of neurons in the last layer
        input_channels : int
            Dimensionality of the input, typically 3 for RGB
        """
        super(PR_CNN, self).__init__()
        # PR_FILL_HERE: Here you have to put the expected input size in terms of width and height of your input image
        self.expected_input_size = (28, 28)

        # First layer
        self.conv1 = nn.Sequential(
            # PR_FILL_HERE: Here you have to put the input channels, output channels ands the kernel size
            # o = [(i + 2p -k)/s + 1]
            nn.Conv2d(in_channels=1, out_channels=24, kernel_size=7 , stride=3),
            nn.LeakyReLU(0.2)
        )

        # Classification layer
        self.fc = nn.Sequential(
            Flatten(),
            # PR_FILL_HERE: Here you have to put the output size of the linear layer. DO NOT change 1536!

            nn.Linear(1536, 10)     #~channel2*kernel_size**2 after maxpool
        )

    def forward(self, x):
        """
        Computes forward pass on the network

        Parameters
        ----------
        x : Variable
            Sample to run forward pass on. (input to the model)

        Returns
        -------
        Variable
            Activations of the fully connected layer
        """
        x = self.conv1(x)
        x = self.fc(x)
        return x

def trainAndTest(batch_size=32, learning_rate=0.003, g=0.5, n_epochs=10, plot=False) :
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    #batch_size = 32
    utils.loadDatasets(batch_size)

    model = PR_CNN()
    model.to(device)

    #learning_rate = learning_rate
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer=optimizer, step_size=5, gamma=g)


    training_losses = []
    training_accuracies = []
    testing_losses = []
    testing_accuracies = []

    #n_epochs = 10

    for epoch in range(n_epochs):
            print("Epoch ", epoch)
            training_results = utils.train(model, utils.train_loader, optimizer, loss_function, batch_size)
            training_losses.append(training_results[0])
            training_accuracies.append(training_results[1])

            testing_results= utils.test(model, utils.train_loader, optimizer, loss_function, batch_size)
            testing_losses.append(testing_results[0])
            testing_accuracies.append(testing_results[1])

            if scheduler :
                scheduler.step()

    #return(testing_accuracies[-1])
    if plot :
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.plot(np.arange(n_epochs), training_losses, color="blue", label="train loss")
        plt.plot(np.arange(n_epochs), testing_losses, color="red", label="val loss")
        plt.legend(loc='upper right')
        plt.subplot(1,2,2)
        plt.plot(np.arange(n_epochs), training_accuracies, color="blue", label="train accuracy")
        plt.plot(np.arange(n_epochs), testing_accuracies, color="red", label="val accuracy")
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

    return(testing_accuracies[-1])

if __name__=='__main__' :
    #
    trainAndTest(n_epochs=10, plot=True, batch_size=16, learning_rate=0.003, g=0.1)
