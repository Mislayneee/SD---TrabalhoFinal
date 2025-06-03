import socket
import time
import csv
import json
import os

HOST = 'load_balancer1'
PORT = 5002

# 1) espera o LB1 subir
for i in range(30):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
        break
    except Exception as e:
        print(f"[{i+1}/30] Esperando load_balancer1... {e}")
        time.sleep(1)
else:
    exit("Erro: LB1 não respondeu.")

# 2) garante que a pasta logs existe dentro do container
os.makedirs("logs", exist_ok=True)

# 3) abre o CSV dentro de logs/
with open('logs/tempos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Mensagem', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'MRT'])

    for i in range(5):
        msg = f"mensagem_{i}"
        t1 = time.time()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            payload = json.dumps({"msg": msg, "tempos": {"T1": t1}}).encode()
            s.sendall(payload)
            t2 = time.time()
            response = s.recv(4096)

        data = json.loads(response.decode())
        tempos = data.get("tempos", {})
        tempos["T2"] = t2
        tempos["T6"] = time.time()

        if "T1" not in tempos:
            print(f"[ERRO] T1 não retornado! tempos = {tempos}")
            mrt = -1
        else:
            mrt = tempos["T6"] - tempos["T1"]

        print(f"\n{msg} -> {data.get('resposta', '[sem resposta]')}")
        print(
            f"T1: {tempos.get('T1', 0):.4f} | "
            f"T2: {t2:.4f} | "
            f"T3: {tempos.get('T3', 0):.4f} | "
            f"T4: {tempos.get('T4', 0):.4f} | "
            f"T5: {tempos.get('T5', 0):.4f} | "
            f"T6: {tempos.get('T6', 0):.4f} | "
            f"MRT: {mrt:.4f}"
        )

        writer.writerow([
            msg,
            tempos.get("T1", ""),
            tempos.get("T2", ""),
            tempos.get("T3", ""),
            tempos.get("T4", ""),
            tempos.get("T5", ""),
            tempos.get("T6", ""),
            mrt
        ])

# 4) mostra dentro do container para conferência
print("Conteúdo da pasta logs dentro do container:")
print(os.listdir("logs"))
