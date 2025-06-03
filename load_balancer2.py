import socket
import random
import time
import json

SERVICE_HOSTS = [('service_ia', 5003)]
HOST = '0.0.0.0'
PORT = 5005

def encaminhar_para_service(data):
    service = random.choice(SERVICE_HOSTS)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(service)
            s.sendall(data)
            return s.recv(4096)
    except:
        return json.dumps({"resposta": "[Erro S2]", "tempos": {}}).encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("LB2 pronto na porta 5005")

    while True:
        conn, addr = s.accept()
        with conn:
            payload = conn.recv(4096)
            t5 = time.time()

            data = json.loads(payload.decode())
            tempos = data.get("tempos", {})
            tempos["T5"] = t5
            data["tempos"] = tempos

            resposta = encaminhar_para_service(json.dumps(data).encode())
            conn.sendall(resposta)