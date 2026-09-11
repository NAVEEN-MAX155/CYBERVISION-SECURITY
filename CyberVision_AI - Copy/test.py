import cv2
from modules.face_detector import detect_faces

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    faces = detect_faces(frame)

    print(faces)

    cv2.imshow("Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()