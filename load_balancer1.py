import socket
import random
import time
import json

SERVICE_HOSTS = [('service_ia', 5003)]
LB2_HOST = 'load_balancer2'
LB2_PORT = 5005

HOST = '0.0.0.0'
PORT = 5002

def process_via_services(data):
    service = random.choice(SERVICE_HOSTS)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(service)
            s.sendall(data)
            return s.recv(4096)
    except:
        return json.dumps({"resposta": "[Erro S1]", "tempos": {}}).encode()

def encaminhar_para_lb2(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LB2_HOST, LB2_PORT))
        s.sendall(data)
        return s.recv(4096)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("LB1 pronto na porta 5002")

    while True:
        conn, addr = s.accept()
        with conn:
            payload = conn.recv(4096)
            if not payload:
                continue

            t3 = time.time()
            data = json.loads(payload.decode())
            tempos = data.get("tempos", {})
            tempos["T3"] = t3
            data["tempos"] = tempos

            # Geração de features para IA leve
            data["features"] = [5.1, 3.5, 1.4, 0.2]
            resp_s1 = process_via_services(json.dumps(data).encode())

            intermediate_data = json.loads(resp_s1.decode())
            data["msg"] = intermediate_data.get("resposta", "")
            data["tempos"] = intermediate_data.get("tempos", tempos)

            resp_lb2 = encaminhar_para_lb2(json.dumps(data).encode())
            conn.sendall(resp_lb2)