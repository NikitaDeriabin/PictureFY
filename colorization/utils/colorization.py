import random
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
from keras.models import model_from_json
import matplotlib.pyplot as plt

from .config import *


def load(json_model, h5_model):
    json_file = open(json_model, "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(h5_model)

    print("Model was loaded!")

    return loaded_model


def process_image_for_colorization(img):
    # imm = img.convert("LA")
    # plt.subplot(1, 3, 3)
    # plt.imshow(imm)
    # plt.show()

    img = img.convert('RGB')
    image_resized = img.resize((256, 256), Image.BILINEAR)
    image2array = np.array(image_resized, dtype=float)
    axes_size = image2array.shape
    lab = rgb2lab(1.0 / 255 * image2array)
    l = lab[:, :, 0]
    l = l.reshape(1, axes_size[0], axes_size[1], 1)

    return l, axes_size


model = load(json_model_file, h5_model_file)


def colorize(image, loaded_model=model):
    img = Image.open(image)
    x_predict, axes_size = process_image_for_colorization(img)

    x_predict = x_predict.reshape(1, axes_size[0], axes_size[1], 1)

    output = loaded_model.predict(x_predict)

    output *= 128
    min_ab_border, max_ab_border = -128, 127
    ab = np.clip(output[0], min_ab_border, max_ab_border)

    res_image_array = np.zeros((axes_size[0], axes_size[1], 3))
    res_image_array[:, :, 0] = np.clip(x_predict[0][:, :, 0], 0, 100)
    res_image_array[:, :, 1:] = ab

    rgb_image_array = lab2rgb(res_image_array)

    rgb_image_array = rgb_image_array
    res_img = Image.fromarray((rgb_image_array * 255).astype('uint8'), "RGB")

    return res_img.resize((512, 512))
