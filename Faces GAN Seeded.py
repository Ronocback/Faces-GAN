
from IPython import display

from utils import Logger

import torch, gc
from torch import nn, optim
from torch.autograd.variable import Variable
from torchvision import transforms, datasets
from PIL import Image

print(torch.__version__)

gc.collect()
torch.cuda.empty_cache()

DATA_FOLDER = './utkcropped'
SELF_IMAGE = "E:\\ML Playground\\Faces-GAN\\self\\me.jpg"

compose = transforms.Compose(
        [transforms.Grayscale(),
         transforms.Resize((100,100)),
         transforms.ToTensor(),
         transforms.Normalize((.5,), (.5,))
        ])

# Load data
data = datasets.ImageFolder(root=DATA_FOLDER, transform=compose)
# Create loader with data, so that we can iterate over it
data_loader = torch.utils.data.DataLoader(data, batch_size=6, shuffle=True)
# Num batches
num_batches = len(data_loader)

# Networks

class DiscriminatorNet(torch.nn.Module):
    """
    A three hidden-layer discriminative neural network
    """
    def __init__(self):
        super(DiscriminatorNet, self).__init__()
        n_features = 10000
        n_out = 1
        
        self.hidden0 = nn.Sequential( 
            nn.Linear(n_features, 1024),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.hidden1 = nn.Sequential(
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.out = nn.Sequential(
            torch.nn.Linear(256, n_out),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        x = self.hidden0(x)
        print(str(x.size()) + "d0")
        x = self.hidden1(x)
        print(str(x.size()) + "d1")
        x = self.hidden2(x)
        print(str(x.size()) + "d2")
        x = self.out(x)
        return x
    
def images_to_vectors(images):
    print("Images to vec")
    return images.view(images.size(0), 10000)

def vectors_to_images(vectors):
    print("vec to image")
    return vectors.view(vectors.size(0), 1, 100, 100)


class GeneratorNet(torch.nn.Module):
    """
    A three hidden-layer generative neural network
    """
    def __init__(self):
        super(GeneratorNet, self).__init__()
        n_features = 100
        n_out = 10000
        
        self.hidden0 = nn.Sequential(
            nn.Linear(n_features, 256),
            nn.LeakyReLU(0.2)
        )
        self.hidden1 = nn.Sequential(            
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2)
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(128, 256),
            nn.LeakyReLU(0.2)
        )
        
        self.out = nn.Sequential(
            nn.Linear(256, n_out),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.hidden0(x)
        print(str(x.size()) + "g0")
        x = self.hidden1(x)
        print(str(x.size()) + "g1")
        x = self.hidden2(x)
        print(str(x.size()) + "g2")
        x = self.out(x)
        print("gen ret")
        return x


# Noise
def noise_tensor(size):
    n = Variable(torch.randn(size, 100))
    n.cpu()
    if torch.cuda.is_available():
        return n.cuda()
    print(n.size() + "")
    return n


# Img path to tensor
def image_tensor(path, size):
    img = Image.open(path)
    n = Variable(compose(img))
    n.resize_(size, 100)
    n.cpu()
    print(str(n.size()) + " image seed size")
    if torch.cuda.is_available():
        return n.cuda()
    return n


discriminator = DiscriminatorNet()
generator = GeneratorNet()
if torch.cuda.is_available():
    discriminator.cuda()
    generator.cuda()


# ## Optimization

# Optimizers
d_optimizer = optim.Adam(discriminator.parameters(), lr=0.0002)
g_optimizer = optim.Adam(generator.parameters(), lr=0.0002)

# Loss function
loss = nn.BCELoss()

# Number of steps to apply to the discriminator
d_steps = 1  # In Goodfellow et. al 2014 this variable is assigned to 1
# Number of epochs
num_epochs = 200


# ## Training


def real_data_target(size):
    '''
    Tensor containing ones, with shape = size
    '''
    print("real target")
    data = Variable(torch.ones(size, 1).cuda())
    data.cpu()
    if torch.cuda.is_available(): return data.cuda()
    return data


def fake_data_target(size):
    '''
    Tensor containing zeros, with shape = size
    '''
    print("fake target")
    data = Variable(torch.zeros(size, 1).cuda())
    data.cpu()
    if torch.cuda.is_available(): return data.cuda()
    return data


def train_discriminator(optimizer, real_data, fake_data):
    # Reset gradients
    optimizer.zero_grad()
    print(str(real_data.size()) + " real_data")
    #real_data = real_data.reshape([6,10000])
    # 1.1 Train on Real Data
    prediction_real = discriminator(real_data)
    # Calculate error and backpropagate
    error_real = loss(prediction_real, real_data_target(real_data.size(0)))
    error_real.backward()

    # 1.2 Train on Fake Data
    prediction_fake = discriminator(fake_data)
    # Calculate error and backpropagate
    error_fake = loss(prediction_fake, fake_data_target(real_data.size(0)))
    error_fake.backward()
    
    # 1.3 Update weights with gradients
    optimizer.step()
    
    # Return error
    return error_real + error_fake, prediction_real, prediction_fake


def train_generator(optimizer, fake_data):
    # 2. Train Generator
    # Reset gradients
    optimizer.zero_grad()
    # Sample noise and generate fake data
    prediction = discriminator(fake_data)
    # Calculate error and backpropagate
    error = loss(prediction, real_data_target(prediction.size(0)))
    error.backward()
    # Update weights with gradients
    optimizer.step()
    # Return error
    return error


# ### Generate Samples for Testing

num_test_samples = 16
test_noise = image_tensor(SELF_IMAGE, num_test_samples)


# ### Start training

logger = Logger(model_name='Face GAN', data_name='Self')

for epoch in range(num_epochs):
    for n_batch, (real_batch,_) in enumerate(data_loader):

        # 1. Train Discriminator
        print(str(real_batch.size()) + " batch")
        real_data = Variable(images_to_vectors(real_batch))
        #real_data=real_data.reshape(-1)
        print(str(real_data.size()) +" data")

        if torch.cuda.is_available(): real_data = real_data.cuda()
        # Generate fake data
        fake_data = generator(image_tensor(SELF_IMAGE, real_data.size(0))).detach()
        # Train D
        d_error, d_pred_real, d_pred_fake = train_discriminator(d_optimizer,
                                                                real_data, fake_data)

        # 2. Train Generator
        # Generate fake data
        fake_data = generator(image_tensor(SELF_IMAGE, real_data.size(0)))
        # Train G
        g_error = train_generator(g_optimizer, fake_data)
        # Log error
        logger.log(d_error, g_error, epoch, n_batch, num_batches)

        # Display Progress
        if (n_batch) % 100 == 0:
            display.clear_output(True)
            # Display Images
            test_images = vectors_to_images(generator(test_noise)).data.cpu()
            logger.log_images(test_images, num_test_samples, epoch, n_batch, num_batches)
            # Display status Logs
            logger.display_status(
                epoch, num_epochs, n_batch, num_batches,
                d_error, g_error, d_pred_real, d_pred_fake
            )
        # Model Checkpoints
        logger.save_models(generator, discriminator, epoch)

