import numpy as np
from tensorflow import keras
from PIL import Image
import os

FILENAME = "imagenet_classifications.txt"
FILEPATH = os.path.join(os.getcwd(), "object_recognition\\utils\\classification", FILENAME)

model = keras.applications.VGG16()
image_size = (224, 224)


def create_classification_dict(filename):
    classes = {}
    with open(filename) as fh:
        for line in fh:
            val, description = line.strip().strip(",").split(":")
            classes[val] = description

    return classes


def get_prediction(file):
    imgnet_dict = create_classification_dict(FILEPATH)

    try:
        image = Image.open(file)
    except:
        raise Exception("Cannot open the " + str(file.name) + " file!")

    try:
        image = image.convert('RGB')
        image = image.resize(image_size, Image.BILINEAR)

        image_array = np.array(image)
        image_array = image_array.astype('float32')

        input_data = image_array.reshape((1, image_array.shape[0], image_array.shape[1], image_array.shape[2]))
    except:
        raise Exception("Image preprocessing error.")

    try:
        res = model.predict(input_data)
    except:
        raise Exception("Prediction error.")

    return imgnet_dict[str(np.argmax(res))]


keras.applications.VGG16(
    include_top=True,
    weights="imagenet",
    classes=1000,
    classifier_activation="softmax",
)
