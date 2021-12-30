import torch.nn as nn


class Discriminator(nn.Module):
    '''
    Discriminator Class

    Parameters
    ----------
    img_chan : int
        the number of channels in the images ex : 3 for RGB (MNIST is black-and-white, so default is 1 channel)
    hidden_dim : int
        the inner dimension

    Attributes
    ----------
    model : nn.Sequential
        the DCGAN discriminator model
    '''

    def __init__(self, img_chan=1, hidden_dim=16):
        super().__init__()

        self.model = nn.Sequential(
            self.make_disc_block(input_channels=img_chan, output_channels=hidden_dim, kernel_size=4, stride=2),
            self.make_disc_block(input_channels=hidden_dim, output_channels=hidden_dim * 2, kernel_size=4, stride=2),
            nn.Conv2d(hidden_dim * 2, 1, kernel_size=4, stride=2)
        )

    def make_disc_block(self, input_channels, output_channels, kernel_size=4, stride=2):
        '''
        Build the sequence of operations corresponding to a discriminator block of DCGAN :
        - convolution
        - batchnorm
        - LeakyReLU activation

        Parameters
        ----------
        input_channels : int
            the number of channels of the input feature representation
        output_channels : int
            the number of channels of the output feature representation
        kernel_size : int
            the size of each convolutional filter (kernel_size, kernel_size)
        stride : int
            the stride of the convolution

        Returns
        -------
            nn.Sequential DCGAN generator block
        '''
        return nn.Sequential(
            nn.Conv2d(input_channels, output_channels, kernel_size, stride=stride),
            nn.BatchNorm2d(num_features=output_channels),
            nn.LeakyReLU(negative_slope=0.2, inplace=True)
        )

    def forward(self, x):
        '''
        Function that applies the forward pass of the discriminator model on a given
        image tensor and which returns a 1-dimensional tensor representing fake/real.

        Parameters
        ----------
        x : Tensor
            a flattened image tensor with dimension (img_dim)

        Returns
        -------
            1-dimensional tensor representing fake/real
        '''
        predictions = self.model(x)
        output = predictions.view(len(predictions), -1)
        return output