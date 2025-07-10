from app import app, connection
import argparse
from app.models.connect import Connect
from app.http_services.server_http_service import ServerHttpService

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Multinode-vina Client")
    parser.add_argument("-p", "--port", type=int, help="Client port (default: 7000)", default=7000)
    parser.add_argument("-a", "--server_address", type=str, help="Server Address")
    parser.add_argument("-u", "--username", type=str, help="username")
    parser.add_argument("-c", "--max_cores", type=int, default=1, help="number of cores program can use. Each core will be assigned a thread (default = 1)")

    args = parser.parse_args()
    port = args.port

    
    

    from app.system.docking_system import DockingSystem
    with app.app_context():

        if args.server_address is not None and args.username is not None:
            try:
                clientId = ServerHttpService.connectWithServer(server_addr=args.server_address, clientId=args.username)
            except Exception as e:
                print('############# Server Connection Error ##############')
                clientId = None
            
            if clientId:
                print("sdsds")
                connection.address =  args.server_address
                connection.username = args.username
                connection.connected = True
        
        docking_system = DockingSystem(total_cores=args.max_cores)
        docking_system.start()

        
        
    app.run(host="0.0.0.0", debug=False, port=port)

