import random
import socket
import sys
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 7000


def generate_random_data():
    type_val = random.choice([1, 2])
    protocolo_val = random.choice([66, 67, 68])
    yymmddhhmmss_val = time.strftime('%y%m%d%H%M%S')
    status_val = random.choice([0, 1])
    id_val = ''.join(random.choices('123456789', k=3))

    return f">DATA {type_val},{protocolo_val},{yymmddhhmmss_val},{status_val},{id_val}<"



while True:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    data = generate_random_data().encode('utf-8')

    sock.sendto(data, (UDP_IP, UDP_PORT))
    print(f"Enviando dados: {data.decode('utf-8')}")
    sys.stdout.flush()
    time.sleep(5)
