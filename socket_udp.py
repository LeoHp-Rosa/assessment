import json
import os
import re
import socket
import sys
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

load_dotenv()

UDP_IP = "127.0.0.1"
UDP_PORT = 7000

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_sock.bind((UDP_IP, UDP_PORT))

try:
    db_connect = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    db_cursor = db_connect.cursor()
    print("Conexão com o PostgreSQL bem-sucedida.")
except Exception as e:
    print(f"Erro durante a conexão com o PostgreSQL: {e}")
    sys.exit(1)



db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS dev_status (
        type INTEGER,
        protocolo INTEGER,
        data TIMESTAMP,
        status INTEGER,
        id VARCHAR(3)
    )
''')
db_connect.commit()

def parse_and_store_data(data):
    parts = data.split(',')
    type_val, protocolo, yymmddhhmmss, status_id = re.sub(r'\D', '', parts[0][4:]), parts[1], parts[2], parts[3][0]
    id_val = parts[4][3:-1]
    date = datetime.strptime(yymmddhhmmss, '%y%m%d%H%M%S')

    db_cursor.execute('''
        INSERT INTO dev_status (type, protocolo, data, status, id)
        VALUES (%s, %s, %s, %s, %s)
    ''', (int(type_val), int(protocolo), date, int(status_id), id_val))
    db_connect.commit()

    return {
        "type": int(type_val),
        "protocolo": int(protocolo),
        "data": date.strftime('%Y-%m-%d %H:%M:%S'),
        "status": int(status_id),
        "id": id_val
    }

while True:
    data, addr = serv_sock.recvfrom(1024)
    received_data = data.decode('utf-8')
    print(f"Recebido: {received_data}") 

    if received_data.startswith('>DATA') and received_data.endswith('<'):
        parsed_data = parse_and_store_data(received_data)
        json_data = json.dumps(parsed_data, indent=4)
        sys.stdout.flush()
        print("Dados recebidos e armazenados:")
        print(json_data)

    