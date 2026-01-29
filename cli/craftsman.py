import sys

def start_server():
    print("Starting the Backside Framework server...")
    #Logica crear controlador
    sys.exit(0)

def make_controller():
    print("Creating a new controller...")
    #Logica crear controlador
    sys.exit(0)

commands = {
    'server':start_server,
    'devise:controller':make_controller,
}

if __name__ == '__main__':
    cmd = sys.argv[1]
    commands.get(cmd, lambda: print('Comando no encontrado'))()

