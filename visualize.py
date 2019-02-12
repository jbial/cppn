import matplotlib.pyplot as plt
import numpy as np
import images2gif
import glob
import os
from PIL import Image
from datetime import datetime

#######################################
## Methods for CPPN visualization
#######################################

def get_zs(size, distribution):
    """Get a randomly sampled latent vector
    """
    dist_dict = dict([('normal', np.random.normal), ('uniform', np.random.uniform)])
    return dist_dict[distribution](size=(2, 1, size))

def show_image(image):
    """Show a single image
    """
    plt.imshow(image, interpolation='nearest')
    plt.axis('off')
    plt.show()

def show_images(images, num_images):
    """Show sampled images
    """
    fig, axes = plt.subplots(num_images, num_images)
    indices = np.random.choice(images.shape[0], 
                    (num_images, num_images), replace=False)
    for i, row_inds in zip(axes, indices):
            for j, inds in zip(i, row_inds):
                j.set_axis_off()
                j.imshow(images[inds])
    plt.show()

def save_image(image, name, path='images/'):
    """Save generated images
    """
    im = np.uint8(255 * image)
    im = Image.fromarray(im)
    im.save(path + name)

def save_images(images):
    """Save a batch of generated images
    """
    for i, im in enumerate(images):
        save_image(im, 
        'img-{0}-{1}.png'.format(datetime.now().strftime('%d-%M-%S'), i))

def to_image(image):
    """Converts numpy to PIL
    """
    return Image.fromarray(np.uint8(255 * image.squeeze()))

def clear_image_dir():
    """Empty the gif image directory to produce a new gif
    """
    for f in glob.glob('gifs/gif_imgs/*'):
        os.remove(f)

def generate_gif(model, frames, size, name, distribution='normal'):
    """Generate an interpolation gif
    """
    im_path = 'gifs/gif_imgs/'

    # Get interpolation information
    z1, z2 = get_zs(size, distribution)
    coeff = np.linspace(0, 1, frames+2)
    interp = lambda a: (1-a) * z1 + a * z2    

    # Store the interpolated images
    images = [to_image(model(latent_code=interp(l))[0]) for l in coeff]
    
    # append the reverse sequence
    images += images[::-1][1:]
    durations = [0.5] + frames*[0.1] + [1.0] + frames*[0.1] + [0.5]
        
    # Write to GIF
    print("Writing images to gif")
    images2gif.writeGif('gifs/'+name, images, duration=durations)