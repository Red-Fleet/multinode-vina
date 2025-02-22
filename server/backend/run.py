from app import app
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Multinode-vina Server")
    parser.add_argument("-p", "--port", type=int, help="Server port (default: 5000)", default=5000)
    args = parser.parse_args()
    port = args.port

    # Initialize Services
    from app.services.docking_service import DockingService

    with app.app_context():
        DockingService.initDockingService()
    
    app.run(host="0.0.0.0", debug=False, port=port)
    

