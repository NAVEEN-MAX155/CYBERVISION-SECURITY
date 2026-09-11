import cv2
import os

MODEL_PATH = os.path.join(
    "models",
    "yunet",
    "face_detection_yunet_2023mar.onnx"
)

detector = cv2.FaceDetectorYN.create(
    MODEL_PATH,
    "",
    (640, 480),
    score_threshold=0.8,
    nms_threshold=0.3,
    top_k=5000
)


def detect_faces(frame):

    h, w = frame.shape[:2]

    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    if faces is None:
        return []

    return faces