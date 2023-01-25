from app import app
import threading
import time

def runAutomatedServices():
    with app.app_context():
        from app.automates_services.automated_master_request_service import AutomatedMasterConnectionRequestService
        AutomatedMasterConnectionRequestService.start()

if __name__ == '__main__':
    x = threading.Thread(target=runAutomatedServices)
    x.start()
    app.run(debug=False, port=7000)

