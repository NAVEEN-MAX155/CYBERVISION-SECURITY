import cv2
import numpy as np
import os


def scan_face():

    detector = cv2.FaceDetectorYN.create(
        "face_detection_yunet_2023mar.onnx",
        "",
        (320, 320)
    )

    recognizer = cv2.FaceRecognizerSF.create(
        "face_recognition_sface_2021dec.onnx",
        ""
    )

    users_folder = os.path.join("faces", "users")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    window_name = "Face Login"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        window_name,
        cv2.WND_PROP_TOPMOST,
        1
    )

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        h, w = frame.shape[:2]

        detector.setInputSize((w, h))

        _, faces = detector.detect(frame)

        if faces is not None:

            for face in faces:

                x, y, fw, fh = face[:4].astype(int)

                aligned = recognizer.alignCrop(frame, face)

                current_feature = recognizer.feature(aligned)

                matched_user = None
                best_score = 0.0

                if os.path.exists(users_folder):

                    for user in os.listdir(users_folder):

                        user_folder = os.path.join(
                            users_folder,
                            user
                        )

                        if not os.path.isdir(user_folder):
                            continue

                        for file in os.listdir(user_folder):

                            if file.endswith(".npy"):

                                saved_feature = np.load(
                                    os.path.join(user_folder, file)
                                )

                                score = recognizer.match(
                                    current_feature,
                                    saved_feature,
                                    cv2.FaceRecognizerSF_FR_COSINE
                                )

                                if score > best_score:
                                    best_score = score
                                    matched_user = user

                if matched_user is not None and best_score > 0.40:

                    color = (0, 255, 0)
                    text = f"{matched_user} ({best_score:.2f})"

                else:

                    color = (0, 0, 255)
                    text = "Unknown"

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + fw, y + fh),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    text,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2
                )

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()