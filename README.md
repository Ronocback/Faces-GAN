# Faces-GAN

Attempt at creating GAN for generating artificial faces using PyTorch.

Uses cropped faces dataset found [here](https://susanqq.github.io/UTKFace/).

## Epoch 0

### Batch 0

![Epoch 0 batch 0](./img_readme/_epoch_0_batch_0.png)

The generator initially creates random static with no discernible patterns.

### Batch 200

![Epoch 0 batch 200](./img_readme/_epoch_0_batch_200.png)

By the 200th batch the static has already been transformed into a recognizable human face.
Each face still looks near identical at this point and are androgynous in appearance.

### Batch 3900

![Epoch 0 batch 3900](./img_readme/_epoch_0_batch_3900.png)

By the end of the first epoch you can actually start to discern traits such as gender, race and age group. The faces are still fairly "ghostly" in appearance and lack some fine detail.

## Epoch 3

![Epoch 3](./img_readme/_epoch_3_batch_0.png)

By the third epoch facial features such as eyebrows have started to become slightly more distinct and interestingly there seems to be a greater variety of facial expressions on show, with some faces showing varying states of happiness while others remain more neutral.

## Epoch 8

![Epoch 8](./img_readme/_epoch_8_batch_1400.png)

At epoch 8 you can see some of the images blurriness, particularly at the edges of generated images, has started to become more subtle. Features such as facial hair are more defined and the contours of the face seem more detailed.

# TODO

## Face Seed

I'm keen to try using a human face as an input for the generator, in place of the static which is the current random seed. Theoretically, this should transform the given face into a new one which is still based on the original subject. Effectively "normalizing" them.
