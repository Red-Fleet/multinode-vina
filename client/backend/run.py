from app import app
import threading
import time

def runAutomatedServices():
    with app.app_context():
        from app.automates_services.automated_notification_service import AutomatedNotificationService
        AutomatedNotificationService.start()

if __name__ == '__main__':
    port = 7000
    x = threading.Thread(target=runAutomatedServices)
    x.start()
    app.run(host="0.0.0.0", debug=False, port=port)

