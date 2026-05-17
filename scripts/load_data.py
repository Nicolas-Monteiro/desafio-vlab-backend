import os
import random
import sys
import time

import httpx
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.security import SECRET_API_KEY

fake = Faker("pt_BR")

API_URL = "http://api:8000/api/v1/abastecimentos/"
CHECK_URL = "http://api:8000/docs"


def esperar_carregamento_api():
    print("Aguardando a API inicializar completamente")
    while True:
        try:
            with httpx.Client() as client:
                response = client.get(CHECK_URL, timeout=1.0)
                if response.status_code == 200:
                    print("API detectada e online, Iniciando os motores de estresse")
                    break
        except (httpx.ConnectError, httpx.ConnectTimeout):
            time.sleep(1)


def gerar_dados_abastecimento():
    data_aleatoria = fake.date_time_between(start_date="-30d", end_date="now")

    return {
        "id_posto": random.randint(1, 10),
        "data_hora": data_aleatoria.isoformat(),
        "tipo_combustivel": random.choice(["GASOLINA", "ETANOL", "DIESEL"]),
        "preco_por_litro": round(random.uniform(4.00, 6.50), 2),
        "volume_abastecido": round(random.uniform(10.0, 55.0), 2),
        "cpf_motorista": fake.cpf(),
    }


def disparar_teste(total_requisicoes: int):
    print(f"Iniciando teste de estresse: Enviando {total_requisicoes} requisições")

    sucessos = 0
    erros = 0

    headers = {"X-API-Key": SECRET_API_KEY}

    with httpx.Client(follow_redirects=True, headers=headers) as client:
        for i in range(total_requisicoes):
            payload = gerar_dados_abastecimento()
            try:
                response = client.post(API_URL, json=payload, timeout=5.0)
                if response.status_code == 201 or response.status_code == 200:
                    sucessos += 1
                else:
                    erros += 1
            except httpx.RequestError as exc:
                print(f"Erro de conexão na requisição {i + 1}: {exc}")
                erros += 1

    print(f"Fim da rajada: {sucessos} com sucesso, {erros} falhas.")


if __name__ == "__main__":
    print("Serviço de carga contínua inicializado.")

    esperar_carregamento_api()
    while True:
        disparar_teste(total_requisicoes=50)

        print("Aguardando 30 segundos para a próxima")
        time.sleep(30)
