import cv2
import spacy
import numpy as np
import os
from tensorflow.python.util import deprecation
import tensorflow as tf
from keras.models import model_from_json
from keras.optimizers import SGD
from keras import backend as K
from sklearn.externals import joblib
from core.model.vqa import VQA_MODEL
from core.model.cnn import VGG_16
import warnings
from django.conf import settings


class MyVQAModel():
    def __init__(self):
        # remove warinings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        deprecation._PRINT_DEPRECATION_WARNINGS = False
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        tf.logging.set_verbosity(tf.logging.ERROR)
        warnings.filterwarnings("ignore", category=DeprecationWarning)


        K.set_image_data_format('channels_first')
        K.common.image_dim_ordering()

        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MODEL_PATH = os.path.join(self.BASE_DIR, 'model')
        DATASET_PATH = os.path.join(MODEL_PATH, "dataset")
        self.VQA_weights_file_name   =  os.path.join(DATASET_PATH, "VQA_MODEL_WEIGHTS.hdf5")
        self.label_encoder_file_name = os.path.join(DATASET_PATH, "FULL_labelencoder_trainval.pkl")
        self.CNN_weights_file_name   = os.path.join(DATASET_PATH, "vgg16_weights.h5")

    def get_image_model(self):
        image_model = VGG_16(self.CNN_weights_file_name)
        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        image_model.compile(optimizer=sgd, loss='categorical_crossentropy')
        return image_model

    def get_image_features(self, fileimage_path):
        image_features = np.zeros((1, 4096))
        image_file_path = "/".join(fileimage_path.split("/")[2:])
        media_path = os.path.join(settings.MEDIA_ROOT, image_file_path)

        im = cv2.resize(cv2.imread(media_path), (224, 224))
        mean_pixel = [103.939, 116.779, 123.68]
        im = im.astype(np.float32, copy=False)
        for c in range(3):
            im[:, :, c] = im[:, :, c] - mean_pixel[c]

        im = im.transpose((2,0,1)) 
        im = np.expand_dims(im, axis=0) 

        image_features[0,:] = self.get_image_model().predict(im)[0]
        return image_features


    def get_VQA_model(self):
        vqa_model = VQA_MODEL()
        vqa_model.load_weights(self.VQA_weights_file_name)

        vqa_model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
        return vqa_model


    def get_question_features(self, question):
        word_embeddings = spacy.load('en_vectors_web_lg')
        tokens = word_embeddings(question)
        question_tensor = np.zeros((1, 30, 300))
        for j in range(len(tokens)):
                question_tensor[0,j,:] = tokens[j].vector
        return question_tensor


    def run(self, image_filepath = None, question = None):
        image_features = self.get_image_features(image_filepath)
        question_features = self.get_question_features(question)
        vqa_model = self.get_VQA_model()

        y_output = vqa_model.predict([question_features, image_features])
        y_sort_index = np.argsort(y_output)

        labelencoder = joblib.load(self.label_encoder_file_name)
        result = list()
        for label in reversed(y_sort_index[0,-5:]):
            result.append({
                "prediction": round(y_output[0,label]*100,2),
                "label": labelencoder.inverse_transform([label])[0]
            })
        return result


