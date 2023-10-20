from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import torch


class VariationalEncoder(nn.Module):
    """
    This class implements a variational encoder that maps input data to a latent space (representation of compressed data) using a neural network. 
    The encoder uses a normal distribution to sample from the latent space and calculates the KL divergence loss between the sampled distribution and the prior distribution.
    
    ## Class Example
    from vz_recommender.models.encoders import VariationalEncoder

    # create random input data
    input_data = torch.randn(32, 64)

    # create an instance of the VariationalEncoder class
    encoder = VariationalEncoder(latent_dims=32, input_dim=64)

    # pass the input data through the encoder
    latent_space = encoder(input_data)

    # print the output and shape of the latent space
    print(latent_space)
    print(latent_space.shape)

    For a full working example, please check for AutoEncoderPL implementation
    in this file personalization-ai/search_reco/ai_search/models.py
    """

    def __init__(self, latent_dims, input_dim):
        """
        ## Method Comment - This method initializes the VariationalEncoder class with the specified latent dimension (lower dimension) and input dimension. It also initializes the neural network layers and the normal distribution used for sampling.
        ## Method Arguments - 
        - latent_dims: int - the number of dimensions in the latent space
        - input_dim: int - the number of dimensions in the input data
        ## Method Return - None
        ## Method Shape - N/A    
        """
        super().__init__()
        self.linear1 = nn.Linear(input_dim, input_dim // 2)
        self.linear2 = nn.Linear(input_dim // 2, latent_dims)
        self.linear3 = nn.Linear(input_dim // 2, latent_dims)
        self.input_dim = input_dim

        self.N = torch.distributions.Normal(0, 1)
        self.kl = 0

    def forward(self, x):
        """
        ## Method Comment - This method takes in input data and maps it to the latent space (representation of compressed data) 
        using a neural network. 
        It also calculates the KL divergence loss between the sampled distribution and the prior distribution.
        ## Method Arguments - 
        - x: torch.Tensor - the input data to be mapped to the latent space
        ## Method Return - 
        - z: torch.Tensor - the output tensor representing the mapped input data in the latent space
        ## Method Shape - 
        - Input: (batch_size, input_dim)
        - Output: (batch_size, latent_dims)
        """
        x = F.relu(self.linear1(x))
        mu = self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        z = mu + sigma * self.N.sample(mu.shape).to(x.device)
        self.kl = (sigma ** 2 + mu ** 2 - torch.log(sigma) - 1 / 2).sum()
        return z  # , self.kl


class Decoder(nn.Module):
    """
    This class defines a decoder module for a deep learning model. 
    It takes in a latent dimension (usually lower dimension) and an input dimension and returns a decoded output.
    
    ## Class Example
    from vz_recommender.models.encoders import Decoder

    # create random input tensor
    input_tensor = torch.randn(1, 10)

    # create Decoder instance
    decoder = Decoder(latent_dims=5, input_dim=10)

    # pass input tensor through decoder
    output_tensor = decoder(input_tensor)

    # print output and shape of output
    print(output_tensor)
    print(output_tensor.shape)

    For a full working example, please check for AutoEncoderPL implementation
    in this file personalization-ai/search_reco/ai_search/models.py
    
    """

    def __init__(self, latent_dims, input_dim):
        """
        ## Method Comment - This method initializes the Decoder class with a linear layer for encoding the latent dimension to half the input dimension and another linear layer for decoding the encoded tensor to the input dimension. It also sets the latent dimension as an instance variable.
        ## Method Arguments - 
        - latent_dims (int): The dimension of the latent space.
        - input_dim (int): The dimension of the input space.
        ## Method Return - None
        ## Method Shape - N/A    
        """
        super().__init__()
        self.linear1 = nn.Linear(latent_dims, input_dim // 2)
        self.linear2 = nn.Linear(input_dim // 2, input_dim)
        self.latent_dims = latent_dims

    def forward(self, z):
        """
        ## Method - forward
        ## Method Comment - This method takes in a tensor and passes it through the decoder layers to return a decoded tensor.
        ## Method Arguments - 
        - z (torch.Tensor): The input tensor to be decoded.
        ## Method Return - The decoded tensor.
        ## Method Shape - Same as input tensor.
        """
        z = F.relu(self.linear1(z))
        z = torch.sigmoid(self.linear2(z))
        return z


class LinearVAE(nn.Module):
    """
    This class implements a linear variational autoencoder (VAE) using PyTorch. It consists of an encoder and a decoder, both of which are implemented as separate modules. The encoder takes in an input tensor and produces a latent representation (compressed representation), while the decoder takes in the latent representation and produces a reconstructed output tensor. The VAE is trained to minimize the reconstruction error while also regularizing the latent representation to follow a prior distribution (usually a standard normal distribution).

    ## Class Example
    from vz_recommender.models.encoders import LinearVAE

    # create a LinearVAE instance with latent dimension 10 and input dimension 784
    model = LinearVAE(latent_dims=10, input_dim=784)

    # generate random input data
    x = torch.randn(32, 784)

    # pass the input data through the model and get the output and its shape
    output = model(x)
    print(output)
    print(output.shape)
    """

    def __init__(self, latent_dims, input_dim):
        """
        ## Method Comment - This method initializes the LinearVAE class by creating an instance of the VariationalEncoder and Decoder classes.
        ## Method Arguments - 
        - latent_dims (int): The number of dimensions in the latent representation.
        - input_dim (int): The number of dimensions in the input tensor.
        ## Method Return - None
        ## Method Shape - N/A
        """
        super().__init__()
        self.encoder = VariationalEncoder(latent_dims=latent_dims, input_dim=input_dim)
        self.decoder = Decoder(latent_dims=latent_dims, input_dim=input_dim)

    def forward(self, x):
        """
        ## Method Comment - This method performs a forward pass through the LinearVAE model by passing the input tensor through the encoder to obtain a latent representation, and then passing the latent representation through the decoder to obtain a reconstructed output tensor. The reconstructed output tensor is returned.
        ## Method Arguments - 
        - x (torch.Tensor): The input tensor to the model.
        ## Method Return - 
        - output (torch.Tensor): The reconstructed output tensor.
        ## Method Shape - Same as input tensor.
        """
        z = self.encoder(x)
        return self.decoder(z)  # , kl