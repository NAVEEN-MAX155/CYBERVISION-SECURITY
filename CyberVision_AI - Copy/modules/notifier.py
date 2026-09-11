from winotify import Notification

def show_notification(title, message):
    toast = Notification(
        app_id="CyberVision AI",
        title=title,
        msg=message
    )
    toast.show()