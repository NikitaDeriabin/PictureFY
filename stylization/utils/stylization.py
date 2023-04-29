import numpy as np

from tensorflow import keras
import tensorflow as tf

from PIL import Image

from .config import *

amount_picture_layer = len(main_picture_layer)
amount_style_layer = len(style_layer)

# connect vgg19 network with weights from trained imagenet
vgg_net = keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
vgg_net.trainable = False


def prepare_images(main, style):
    main_image = Image.open(main)
    style_image = Image.open(style)

    main_image = main_image.convert('RGB')
    style_image = style_image.convert('RGB')

    main_image = main_image.resize(image_size, Image.BILINEAR)
    style_image = style_image.resize(image_size, Image.BILINEAR)

    return main_image, style_image


def bgr2rgb(bgr_img):
    img_copy = bgr_img.copy()

    if len(img_copy.shape) == 4:
        img_copy = np.squeeze(img_copy, 0)

    if len(img_copy.shape) != 3:
        raise Exception("Error with dimensions!")

    img_copy[:, :, 0] += aver_B
    img_copy[:, :, 1] += aver_G
    img_copy[:, :, 2] += aver_R
    img_copy = img_copy[:, :, ::-1]

    img_copy = np.clip(img_copy, 0, 255).astype('uint8')
    return img_copy


def get_output_layers(picture_layers, style_layers, vgg_net):
    style_outputs = [vgg_net.get_layer(name).output for name in style_layers]
    picture_outputs = [vgg_net.get_layer(name).output for name in picture_layers]
    return picture_outputs, style_outputs


def get_gram_matrix(tensor):
    channels = int(tensor.shape[-1])
    tensor_2d = tf.reshape(tensor, [-1, channels])
    n_elements = tf.shape(tensor_2d)[0]
    gram = tf.matmul(tensor_2d, tensor_2d, transpose_a=True)
    return gram / tf.cast(n_elements, tf.float32)


def get_features_map(model, main_x, style_x):
    content_outputs = model(main_x)
    content_feat_maps = [picture_layer[0] for picture_layer in content_outputs[amount_style_layer:]]

    style_outputs = model(style_x)
    style_feat_map = [style_layer[0] for style_layer in style_outputs[:amount_style_layer]]

    return style_feat_map, content_feat_maps


def loss_func(primary_cont, final_cont):
    loss = tf.reduce_mean(tf.square(primary_cont - final_cont))
    return loss


def style_loss_func(primary_style, target_gram):
    gram_style = get_gram_matrix(primary_style)
    loss = tf.reduce_mean(tf.square(gram_style - target_gram))
    return loss


def common_loss(model, loss_weights, init_image, gram_style_features_map, picture_features_map):
    style_weight, picture_weight = loss_weights

    model_outputs = model(init_image)

    content_output_features = model_outputs[amount_style_layer:]
    style_output_features = model_outputs[:amount_style_layer]

    style_loss_score = 0
    picture_loss_score = 0

    # Accumulate style losses from all layers
    weight_per_style_layer = 1.0 / float(amount_style_layer)
    for target_style, comb_style in zip(gram_style_features_map, style_output_features):
        style_loss_score += weight_per_style_layer * style_loss_func(comb_style[0], target_style)

    # Accumulate content losses from all layers
    weight_per_content_layer = 1.0 / float(amount_picture_layer)
    for target_content, comb_content in zip(picture_features_map, content_output_features):
        picture_loss_score += weight_per_content_layer * loss_func(comb_content[0], target_content)

    style_loss_score *= style_weight
    picture_loss_score *= picture_weight

    loss = style_loss_score + picture_loss_score
    return loss, style_loss_score, picture_loss_score


# getting specific layers from vgg19
output_layers = get_output_layers(main_picture_layer, style_layer, vgg_net)
model_output_layers = output_layers[0] + output_layers[1]

# creating vgg19 duplicate with needed output layers
new_model = keras.models.Model(vgg_net.input, model_output_layers)


def run_process(picture, style):
    # preprocess_input: from RGB -> BGR, subtracts averages B - 103.939, G - 116.779, R - 123.68
    main_x = keras.applications.vgg19.preprocess_input(np.expand_dims(picture, axis=0))
    style_x = keras.applications.vgg19.preprocess_input(np.expand_dims(style, axis=0))

    iterations = 5
    alpha = 1e3  # picture_weights importance
    beta = 1e-2  # style_weights importance

    style_features_map, picture_features_map = get_features_map(new_model, main_x, style_x)
    gram_style_features = [get_gram_matrix(style_feature) for style_feature in style_features_map]

    primary_image = tf.Variable(np.copy(main_x), dtype=tf.float32)

    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=3, beta1=0.5, epsilon=1e-1)

    less_loss = float('inf')
    best_image = None

    loss_weights = (beta, alpha)

    configuration = {
          'model': new_model,
          'loss_weights': loss_weights,
          'init_image': primary_image,
          'gram_style_features_map': gram_style_features,
          'picture_features_map': picture_features_map
    }

    norm_means = np.array([aver_B, aver_G, aver_R])
    clip_max = 255 - norm_means
    clip_min = -norm_means

    for i in range(iterations):
        with tf.GradientTape() as tape:
            all_loss = common_loss(**configuration)

        loss, style_loss, picture_loss = all_loss
        grads = tape.gradient(loss, primary_image)
        optimizer.apply_gradients([(grads, primary_image)])
        clipped = tf.clip_by_value(primary_image, clip_min, clip_max)
        primary_image.assign(clipped)

        if loss < less_loss:
            less_loss = loss
            best_image = bgr2rgb(primary_image.numpy())

            print('Iteration: ' + str(i))

    image = Image.fromarray(best_image.astype('uint8'), 'RGB')
    print("Min of loss: " + str(less_loss))

    return image








