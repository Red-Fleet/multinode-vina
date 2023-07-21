from app import app
import threading
import time
import argparse

def runAutomatedServices():
    with app.app_context():
        from app.automates_services.automated_notification_service import AutomatedNotificationService
        AutomatedNotificationService.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Multinode-vina Client")
    parser.add_argument("port", type=int, help="Client port")
    args = parser.parse_args()
    port = args.port
    x = threading.Thread(target=runAutomatedServices)
    x.start()
    app.run(host="0.0.0.0", debug=False, port=port)

