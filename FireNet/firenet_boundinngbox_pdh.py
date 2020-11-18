import cv2
import requests, json
import tempfile

import numpy as np
from PIL import Image
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

from imageai.Detection.Custom import CustomObjectDetection, CustomVideoObjectDetection
import os

execution_path = os.getcwd()
detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
detector.loadModel()

def train_detection_model():
    from imageai.Detection.Custom import DetectionModelTrainer

    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory="fire-dataset")
    trainer.setTrainConfig(object_names_array=["fire"], batch_size=8, num_experiments=100,
                           train_from_pretrained_model="pretrained-yolov3.h5")
    trainer.trainModel()

def imread(img):
    if type(img) is np.ndarray:
        return img
    if not img.startswith("http"):
        return cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    
    def JPG_PNG(img):
        return cv2.imdecode(np.asarray(bytearray(img), dtype="uint8"), cv2.IMREAD_COLOR)
    
    return {
      ".gif": (lambda img:
        np.array(
          Image.open(BytesIO(img)).convert('RGB')
        )[:, :, ::-1].copy()
      ),
      ".jpg": JPG_PNG,
      ".png": JPG_PNG
    }[Path(img).suffix](urlopen(img).read())

output = tempfile.NamedTemporaryFile(suffix='.jpg').name

def detect_from_image(url):
    img = imread(url)
    detections = detector.detectObjectsFromImage(input_image = img,
                                                input_type='array',
                                                output_image_path = output,
                                                minimum_percentage_probability=40)
    """
    'detectObjectsFromImage()' function is used to detect objects observable in the given image:
                    * input_image , which can be a filepath or image numpy array in BGR
                    * output_image_path (only if output_type = file) , file path to the output image that will contain the detection boxes and label, if output_type="file"
                    * input_type (optional) , filepath/numpy array of the image. Acceptable values are "file" and "array"
                    * output_type (optional) , file path/numpy array/image file stream of the image. Acceptable values are "file" and "array"
                    * extract_detected_objects (optional) , option to save each object detected individually as an image and return an array of the objects' image path.
                    * minimum_percentage_probability (optional, 30 by default) , option to set the minimum percentage probability for nominating a detected object for output.
                    * nms_threshold (optional, o.45 by default) , option to set the Non-maximum suppression for the detection
                    * display_percentage_probability (optional, True by default), option to show or hide the percentage probability of each object in the saved/returned detected image
                    * display_display_object_name (optional, True by default), option to show or hide the name of each object in the saved/returned detected image
                    * thread_safe (optional, False by default), enforce the loaded detection model works across all threads if set to true, made possible by forcing all Keras inference to run on the default graph
    """
    height, width = img.shape
    data = {
            "image": url,
            "labels": {
                "fire": []
            }
        }
    
    for detection in detections:
        [x1,y1,x2, y2] = detection["box_points"]
        box_height = abs(y1-y2)
        box_width = abs(x1-x2)
        
        top_ratio = round(y1/height, 2)
        bot_ratio = round((height-y2)/height, 2)
        l_ratio = round(x1/width, 2)
        r_ratio = round((width-x2)/width, 2)
        
        data['labels']['fire'].append({
            "top": top_ratio,
            "bottom": bot_ratio,
            "left": l_ratio,
            "right": r_ratio
        })

    print(data)
    res = requests.post('https://proxy.hwangsehyun.com/SmartCity/1234', json=data)

detect_from_image('https://raw.githubusercontent.com/OlafenwaMoses/FireNET/master/images/2-detected.jpg')