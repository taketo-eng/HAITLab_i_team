#@title Imports and function definitions
from absl import logging

import imageio
import PIL.Image
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
#tf.random.set_seed(0)

import tensorflow_hub as hub
from tensorflow_docs.vis import embed
import time

import random
# try:
#   from google.colab import files
# except ImportError:
#   pass

#from IPython import display
from skimage import transform

# We could retrieve this value from module.get_input_shapes() if we didn't know
# beforehand which module we will be using.
latent_dim = 512


# Interpolates between two vectors that are non-zero and don't both lie on a
# line going through origin. First normalizes v2 to have the same norm as v1. 
# Then interpolates between the two vectors on the hypersphere.
def interpolate_hypersphere(v1, v2, num_steps):
  v1_norm = tf.norm(v1)
  v2_norm = tf.norm(v2)
  v2_normalized = v2 * (v1_norm / v2_norm)

  vectors = []
  for step in range(num_steps):
    interpolated = v1 + (v2_normalized - v1) * step / (num_steps - 1)
    interpolated_norm = tf.norm(interpolated)
    interpolated_normalized = interpolated * (v1_norm / interpolated_norm)
    vectors.append(interpolated_normalized)
  return tf.stack(vectors)



# Given a set of images, show an animation.
def animate(images):
  images = np.array(images)
  converted_images = np.clip(images * 255, 0, 255).astype(np.uint8)
  imageio.mimsave('./static/images/uploads/animation.gif', converted_images)

logging.set_verbosity(logging.ERROR)


progan = hub.load("https://tfhub.dev/google/progan-128/1").signatures['default']



image_from_module_space = False  # @param { isTemplate:true, type:"boolean" }

def get_module_space_image():
  vector = tf.random.normal([1, latent_dim])
  images = progan(vector)['default'][0]
  return images

def upload_image(file):
  image = imageio.imread(file)
  return transform.resize(image, [128, 128])

#tf.random.set_seed(random.random()*100) #固定したくないからコメントアウト
#initial_vector = tf.random.normal([1, latent_dim]) #更新のためfind_closest_latent_vector関数内で定義




num_optimization_steps=200 #default = 200
steps_per_image=5 #default = 5

def find_closest_latent_vector(num_optimization_steps,
                               steps_per_image, target_image):
  images = []
  losses = []

  #関数が呼び出された時に更新したいからinitial_vectorは関数内で定義
  initial_vector = tf.random.normal([1, latent_dim])
  vector = tf.Variable(initial_vector)  
  #print(vector)
  optimizer = tf.optimizers.Adam(learning_rate=0.01)
  loss_fn = tf.losses.MeanAbsoluteError(reduction="sum")

  for step in range(num_optimization_steps):
    if (step % 10)==0:
      print(step)
    print('.', end='')
    with tf.GradientTape() as tape:
      image = progan(vector.read_value())['default'][0]
      if (step % steps_per_image) == 0:
        images.append(image.numpy())

      #最後の結果だけ長めに見れるように用意
      if step == (num_optimization_steps-1):
        print('True')
        for _ in range(10):
          images.append(image.numpy())
      target_image_difference = loss_fn(image, target_image[:,:,:3])
      # The latent vectors were sampled from a normal distribution. We can get
      # more realistic images if we regularize the length of the latent vector to 
      # the average length of vector from this distribution.
      regularizer = tf.abs(tf.norm(vector) - np.sqrt(latent_dim))
      
      loss = target_image_difference + regularizer
      losses.append(loss.numpy())
    grads = tape.gradient(loss, [vector])
    optimizer.apply_gradients(zip(grads, [vector]))
    
  return images, losses

