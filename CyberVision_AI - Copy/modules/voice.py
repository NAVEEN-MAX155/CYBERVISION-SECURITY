import pyttsx3
import threading
import time


_engine = None
_engine_lock = threading.Lock()

_last_spoken = {}
COOLDOWN = 5


def _get_engine():

    global _engine

    if _engine is None:
        _engine = pyttsx3.init()

        _engine.setProperty(
            "rate",
            165
        )

        _engine.setProperty(
            "volume",
            1.0
        )

    return _engine


def _speak(text):

    try:

        with _engine_lock:

            engine = _get_engine()

            engine.say(text)
            engine.runAndWait()

    except Exception as e:

        print("Voice Error:", e)


def speak(key, text):

    now = time.time()

    last_time = _last_spoken.get(key, 0)

    if now - last_time < COOLDOWN:
        return

    _last_spoken[key] = now

    threading.Thread(
        target=_speak,
        args=(text,),
        daemon=True
    ).start()


def reset(key):

    _last_spoken.pop(
        key,
        None
    )


def unauthorized():

    speak(
        "unauthorized",
        "Warning. Unauthorized person detected. Screen blur activated."
    )


def camera_blocked():

    speak(
        "camera_blocked",
        "Warning. Please check your camera. Camera is covered or blocked."
    )


def camera_disconnected():

    speak(
        "camera_disconnected",
        "Warning. Camera disconnected."
    )


def multiple_faces():

    speak(
        "multiple_faces",
        "Warning. Multiple faces detected."
    )