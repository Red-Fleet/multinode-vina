from app import app
import threading
import time


# from app.system.docking_system import DockingSystem


# def runAutomatedServices():
#     with app.app_context():
#         from app.automates_services.automated_notification_service import AutomatedNotificationService
#         AutomatedNotificationService.start()

if __name__ == '__main__':
    port = 7000
    # x = threading.Thread(target=runAutomatedServices)
    # x.start()
    # docking_system = DockingSystem(total_cores=6)
    # docking_system.start()
    app.run(host="0.0.0.0", debug=False, port=port)

