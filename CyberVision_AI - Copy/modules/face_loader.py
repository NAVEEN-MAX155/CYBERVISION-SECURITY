import os
import numpy as np

USERS_FOLDER = "faces/users"


def load_known_faces():

    known_encodings = []
    known_names = []

    if not os.path.exists(USERS_FOLDER):
        return known_encodings, known_names

    for user in os.listdir(USERS_FOLDER):

        user_folder = os.path.join(
            USERS_FOLDER,
            user
        )

        if not os.path.isdir(user_folder):
            continue

        feature_path = os.path.join(
            user_folder,
            "feature.npy"
        )

        if os.path.exists(feature_path):

            try:
                feature = np.load(feature_path)

                known_encodings.append(feature)
                known_names.append(user)

            except Exception as e:
                print(f"Error loading {user}: {e}")

    return known_encodings, known_names


if __name__ == "__main__":

    encodings, names = load_known_faces()

    print(f"Loaded Users: {len(names)}")
    print(names)