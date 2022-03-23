
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont

from matplotlib import pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

from utils.constants import CV_KEY, CV_ENDPOINT, PROJECT_ID, MODEL_NAME

tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)

credentials = ApiKeyCredentials(in_headers={"Prediction-key": CV_KEY})
predictor = CustomVisionPredictionClient(endpoint=CV_ENDPOINT, credentials=credentials)
model = load_model('flag_detector.h5')

LABELS = ['Argentina', 'Belgium', 'Brazil', 'Columbia', 'Croatia', 'Denmark', 'England', 'France', 'Japan', 'Mexico', 'Portugal', 'Russia', 'Spain', 'Sweden', 'Switzerland', 'Uruguay']

def detect_single_object(img_file):
    img = image.load_img(img_file, target_size = (64, 64))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    predict_func = tf.autograph.experimental.do_not_convert(model.predict) 
    result = predict_func(img)
    y_classes = result.argmax(axis=-1)
    predicted_label = sorted(LABELS)[y_classes[0]]

    return predicted_label

def detect_single_object_cloud(img_file):
    with open(img_file, mode="rb") as data:
        results = predictor.detect_image(PROJECT_ID, MODEL_NAME, data)

    return results.predictions[0].tag_name 

def detect_multi_object(img_file):
    img = Image.open(img_file)
    img_h, img_w, img_ch = np.array(img).shape
    with open(img_file, mode="rb") as data:
        results = predictor.detect_image(PROJECT_ID, MODEL_NAME, data)


    draw = ImageDraw.Draw(img)
    lineWidth = int(np.array(img).shape[1]/100)
    for prediction in results.predictions:
        color = 'red'
        if (prediction.probability*100) > 10:
            left = prediction.bounding_box.left * img_w 
            top = prediction.bounding_box.top * img_h 
            height = prediction.bounding_box.height * img_h
            width =  prediction.bounding_box.width * img_w
            points = ((left,top), (left+width,top), (left+width,top+height), (left,top+height),(left,top))
            draw.line(points, fill=color, width=lineWidth)
            plt.annotate(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100),(left,top), backgroundcolor=color)

    try:
        plt.imshow(img)
        plt.show()
    except:
        pass
