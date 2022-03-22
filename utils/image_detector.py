
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

from matplotlib import pyplot as plt
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

from utils.constants import CV_KEY, CV_ENDPOINT, PROJECT_ID, MODEL_NAME

credentials = ApiKeyCredentials(in_headers={"Prediction-key": CV_KEY})
predictor = CustomVisionPredictionClient(endpoint=CV_ENDPOINT, credentials=credentials)

def detect_multi_image(img_file):
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
