import cv2
import numpy as np
import os
import time
import threading
import pyttsx3

from modules.screen_blur import blur
from modules.logger import log_event
from modules.notifier import show_notification


# =====================================================
# VOICE
# =====================================================

voice_lock = threading.Lock()

last_voice_time = 0
VOICE_COOLDOWN = 5


def speak(text):

    global last_voice_time

    now = time.time()

    if now - last_voice_time < VOICE_COOLDOWN:
        return

    last_voice_time = now

    def run_voice():

        try:

            with voice_lock:

                engine = pyttsx3.init()

                engine.setProperty(
                    "rate",
                    165
                )

                engine.setProperty(
                    "volume",
                    1.0
                )

                engine.say(text)

                engine.runAndWait()

                engine.stop()

        except Exception as e:

            print(
                "Voice Error:",
                e
            )

    threading.Thread(
        target=run_voice,
        daemon=True
    ).start()


# =====================================================
# PRIVACY GUARD
# =====================================================

def privacy_guard():

    cap = None

    blur_active = False

    state = "NORMAL"

    last_notification = 0

    try:

        # =================================================
        # FACE DETECTOR
        # =================================================

        detector = cv2.FaceDetectorYN.create(

            "face_detection_yunet_2023mar.onnx",

            "",

            (640, 480),

            score_threshold=0.6,

            nms_threshold=0.3,

            top_k=5000
        )


        # =================================================
        # FACE RECOGNIZER
        # =================================================

        recognizer = cv2.FaceRecognizerSF.create(

            "face_recognition_sface_2021dec.onnx",

            ""
        )


        # =================================================
        # USERS FOLDER
        # =================================================

        users_folder = os.path.join(
            "faces",
            "users"
        )


        # =================================================
        # CAMERA
        # =================================================

        cap = cv2.VideoCapture(
            0,
            cv2.CAP_DSHOW
        )

        cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        cap.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )


        if not cap.isOpened():

            print(
                "Camera not found."
            )

            speak(
                "Please check your camera."
            )

            return


        window_name = "Privacy Guard Camera"


        cv2.namedWindow(
            window_name,
            cv2.WINDOW_NORMAL
        )

        cv2.setWindowProperty(
            window_name,
            cv2.WND_PROP_TOPMOST,
            1
        )


        # =================================================
        # MAIN LOOP
        # =================================================

        while True:

            ret, frame = cap.read()


            # =================================================
            # CAMERA FAILURE
            # =================================================

            if not ret:

                if state != "CAMERA_ERROR":

                    state = "CAMERA_ERROR"

                    if not blur_active:

                        blur.show(
                            "📷 PLEASE CHECK YOUR CAMERA",
                            "Camera disconnected."
                        )

                        blur_active = True

                    speak(
                        "Please check your camera. "
                        "Camera disconnected."
                    )

                break


            # =================================================
            # FRAME SIZE
            # =================================================

            h, w = frame.shape[:2]

            detector.setInputSize(
                (w, h)
            )


            # =================================================
            # BRIGHTNESS
            # =================================================

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            brightness = float(
                np.mean(gray)
            )


            # =================================================
            # FACE DETECTION
            # =================================================

            _, faces = detector.detect(
                frame
            )


            # =================================================
            # CAMERA COVERED
            # =================================================

            if brightness < 35:

                new_state = "CAMERA_COVERED"


                if state != new_state:

                    state = new_state


                    if not blur_active:

                        blur.show(
                            "📷 PLEASE CHECK YOUR CAMERA",
                            "Camera is covered or blocked."
                        )

                        blur_active = True


                    speak(
                        "Please check your camera. "
                        "Camera is covered or blocked."
                    )


                    try:

                        log_event(
                            "Camera covered or blocked"
                        )

                    except Exception:
                        pass


                cv2.putText(
                    frame,
                    "PLEASE CHECK YOUR CAMERA",
                    (70, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 255),
                    3
                )


                cv2.putText(
                    frame,
                    "Camera is covered or blocked",
                    (100, 260),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )


            # =================================================
            # NO FACE
            # =================================================

            elif faces is None or len(faces) == 0:

                new_state = "NO_FACE"


                if state != new_state:

                    state = new_state


                    if blur_active:

                        blur.hide()

                        blur_active = False


                cv2.putText(
                    frame,
                    "Waiting for face...",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )


            # =================================================
            # MULTIPLE FACES
            # =================================================

            elif len(faces) > 1:

                new_state = "MULTIPLE_FACES"


                if state != new_state:

                    state = new_state


                    if not blur_active:

                        blur.show(
                            "🔒 PRIVACY MODE",
                            "Multiple Faces Detected"
                        )

                        blur_active = True


                    speak(
                        "Warning. Multiple faces detected."
                    )


                    try:

                        log_event(
                            "Multiple faces detected"
                        )

                    except Exception:
                        pass


                cv2.putText(
                    frame,
                    "MULTIPLE FACES DETECTED",
                    (70, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    3
                )


            # =================================================
            # SINGLE FACE
            # =================================================

            else:

                face = faces[0]


                x, y, fw, fh = face[:4].astype(
                    int
                )


                # ---------------------------------------------
                # ALIGN FACE
                # ---------------------------------------------

                aligned = recognizer.alignCrop(
                    frame,
                    face
                )


                current_feature = recognizer.feature(
                    aligned
                )


                matched_user = None

                best_score = 0.0


                # =================================================
                # SEARCH USERS
                # =================================================

                if os.path.exists(
                    users_folder
                ):

                    for user in os.listdir(
                        users_folder
                    ):

                        user_folder = os.path.join(
                            users_folder,
                            user
                        )


                        if not os.path.isdir(
                            user_folder
                        ):
                            continue


                        for file in os.listdir(
                            user_folder
                        ):

                            if not file.endswith(
                                ".npy"
                            ):
                                continue


                            feature_path = os.path.join(
                                user_folder,
                                file
                            )


                            try:

                                saved_feature = np.load(
                                    feature_path
                                )


                                score = recognizer.match(

                                    current_feature,

                                    saved_feature,

                                    cv2.FaceRecognizerSF_FR_COSINE
                                )


                                if score > best_score:

                                    best_score = score

                                    matched_user = user


                            except Exception as e:

                                print(
                                    "Feature Error:",
                                    e
                                )


                # =================================================
                # AUTHORIZED
                # =================================================

                if (

                    matched_user is not None

                    and best_score > 0.40

                ):

                    new_state = "AUTHORIZED"


                    if state != new_state:

                        state = new_state


                        if blur_active:

                            blur.hide()

                            blur_active = False


                    color = (
                        0,
                        255,
                        0
                    )


                    text = (
                        f"Welcome {matched_user} "
                        f"({best_score:.2f})"
                    )


                # =================================================
                # UNAUTHORIZED
                # =================================================

                else:

                    new_state = "UNAUTHORIZED"


                    if state != new_state:

                        state = new_state


                        if not blur_active:

                            blur.show(
                                "🔒 PRIVACY MODE",
                                "Unauthorized Person Detected"
                            )

                            blur_active = True


                        speak(
                            "Unauthorized person detected."
                        )


                        try:

                            log_event(
                                "Unauthorized Person Detected"
                            )

                        except Exception:
                            pass


                        current_time = time.time()


                        if (

                            current_time
                            - last_notification
                            > 5

                        ):

                            try:

                                show_notification(

                                    "CyberVision AI",

                                    "Unauthorized Person Detected!"

                                )

                            except Exception:
                                pass


                            last_notification = (
                                current_time
                            )


                    color = (
                        0,
                        0,
                        255
                    )


                    text = (
                        f"Unknown "
                        f"({best_score:.2f})"
                    )


                # =================================================
                # DRAW FACE
                # =================================================

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


            # =================================================
            # CAMERA WINDOW
            # =================================================

            cv2.imshow(
                window_name,
                frame
            )


            key = cv2.waitKey(
                1
            ) & 0xFF


            if (

                key == ord("q")

                or key == 27

            ):

                break


    except Exception as e:

        print(
            "Privacy Guard Error:",
            e
        )


    finally:

        if cap is not None:

            cap.release()


        if blur_active:

            blur.hide()


        cv2.destroyAllWindows()