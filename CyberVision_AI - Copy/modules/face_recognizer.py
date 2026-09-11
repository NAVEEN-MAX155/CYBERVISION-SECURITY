import os
import cv2
import numpy as np

MODEL_PATH = os.path.join(
    "models",
    "sface",
    "face_recognition_sface_2021dec.onnx"
)

recognizer = cv2.FaceRecognizerSF.create(
    MODEL_PATH,
    ""
)


def get_embedding(frame, face):

    aligned = recognizer.alignCrop(frame, face)

    feature = recognizer.feature(aligned)

    return feature


def match_face(feature, database, threshold=0.363):

    best_name = "Unknown"
    best_score = 0.0

    for name, db_feature in database.items():

        score = recognizer.match(
            feature,
            db_feature,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        if score > threshold and score > best_score:
            best_score = score
            best_name = name

    return best_name, best_score