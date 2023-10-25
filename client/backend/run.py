from app import app
import argparse

# from app.system.docking_system import DockingSystem


# def runAutomatedServices():
#     with app.app_context():
#         from app.automates_services.automated_notification_service import AutomatedNotificationService
#         AutomatedNotificationService.start()

if __name__ == '__main__':
    #port = 7000

    parser = argparse.ArgumentParser(description="Multinode-vina Client")
    parser.add_argument("port", type=int, help="Client port")
    args = parser.parse_args()
    port = args.port

    app.run(host="0.0.0.0", debug=False, port=port)

