import os
import cv2
import pickle
import numpy as np

DATASET_PATH = "faces/users"
MODEL_PATH = "trainer.yml"
LABELS_PATH = "labels.pickle"


def train_model():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    label_ids = {}
    current_id = 0

    if not os.path.exists(DATASET_PATH):
        print("Dataset folder not found!")
        return

    for person in os.listdir(DATASET_PATH):

        person_path = os.path.join(DATASET_PATH, person)

        if not os.path.isdir(person_path):
            continue

        label_ids[current_id] = person

        for image in os.listdir(person_path):

            img_path = os.path.join(person_path, image)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            img = cv2.resize(img, (200, 200))

            faces.append(img)
            labels.append(current_id)

        current_id += 1

    if len(faces) == 0:
        print("No training images found!")
        return

    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)

    with open(LABELS_PATH, "wb") as f:
        pickle.dump(label_ids, f)

    print("\n==============================")
    print("✅ Model Trained Successfully")
    print("Users :", len(label_ids))
    print("Images:", len(faces))
    print("==============================\n")


if __name__ == "__main__":
    train_model()