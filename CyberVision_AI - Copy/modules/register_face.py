import cv2
import numpy as np
import os
from tkinter import messagebox


def register_face(username):

    detector = cv2.FaceDetectorYN.create(
        "face_detection_yunet_2023mar.onnx",
        "",
        (320, 320)
    )

    recognizer = cv2.FaceRecognizerSF.create(
        "face_recognition_sface_2021dec.onnx",
        ""
    )

    user_folder = os.path.join("faces","users", username)

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    poses = [
        "Look Straight",
        "Slight Left",
        "More Left",
        "Slight Right",
        "More Right"
    ]

    capture_no = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        h, w = frame.shape[:2]

        detector.setInputSize((w, h))

        _, faces = detector.detect(frame)

        if capture_no < 5:

            cv2.putText(
                frame,
                poses[capture_no],
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Press SPACE to capture",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

        if faces is not None:

            face = faces[0]

            x, y, fw, fh = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                (0, 255, 0),
                2
            )

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            brightness = np.mean(gray)

            if brightness < 90:

                cv2.putText(
                    frame,
                    "Low Light! Move to brighter place",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            elif fw < 120 or fh < 120:

                cv2.putText(
                    frame,
                    "Move closer to camera",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

        cv2.imshow(
            "Face Registration",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if (
            key == ord(" ")
            and faces is not None
        ):

            if brightness < 90:
                continue

            if fw < 120 or fh < 120:
                continue

            aligned = recognizer.alignCrop(
                frame,
                face
            )

            feature = recognizer.feature(
                aligned
            )

            file_no = capture_no + 1

            np.save(
                os.path.join(
                    user_folder,
                    f"{file_no}.npy"
                ),
                feature
            )

            cv2.imwrite(
                os.path.join(
                    user_folder,
                    f"{file_no}.jpg"
                ),
                aligned
            )

            capture_no += 1

            if capture_no == 5:

                cv2.putText(
                    frame,
                    "Registration Successful!",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.imshow(
                    "Face Registration",
                    frame
                )

                cv2.waitKey(1500)

                cap.release()
                cv2.destroyAllWindows()

                messagebox.showinfo(
                    "Success",
                    f"{username} registered successfully!"
                )

                return

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()