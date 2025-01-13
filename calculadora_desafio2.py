# Necessario instalar o pacote requests e beautifulsoup #

import requests
from bs4 import BeautifulSoup

def obter_tarifa(classe: str, bandeira: str) -> float:
    url = "https://www.cemig.com.br/atendimento/valores-de-tarifas-e-servicos/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a página. Código HTTP: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    if classe == "Residencial":
        tarifa_element = soup.find("span", {"id": "tarifa_residencial"})
    elif classe == "Comercial":
        tarifa_element = soup.find("span", {"id": "tarifa_comercial"})
    elif classe == "Industrial":
        tarifa_element = soup.find("span", {"id": "tarifa_industrial"})
    else:
        raise ValueError("Classe inválida!")
    
    if tarifa_element:
        tarifa = float(tarifa_element.text.replace(",", "."))
    else:
        raise ValueError("Não foi possível encontrar a tarifa no site.")
    
    if bandeira == "Verde":
        tarifa *= 1.0
    elif bandeira == "Amarela":
        tarifa *= 1.1
    elif bandeira == "Vermelha":
        tarifa *= 1.2
    else:
        raise ValueError("Bandeira inválida!")

    return tarifa

def calculadora(consumo: list, classe: str, bandeira: str) -> tuple:
    tarifa = obter_tarifa(classe, bandeira)
    media_consumo = sum(consumo) / len(consumo)

    if media_consumo < 10000:
        descontos = {"Residencial": 0.18, "Comercial": 0.16, "Industrial": 0.12}
        cobertura = 0.90
    elif 10000 <= media_consumo < 20000:
        descontos = {"Residencial": 0.22, "Comercial": 0.18, "Industrial": 0.15}
        cobertura = 0.95
    else:
        descontos = {"Residencial": 0.25, "Comercial": 0.22, "Industrial": 0.18}
        cobertura = 0.99

    desconto_aplicado = descontos[classe]
    economia_mensal = media_consumo * tarifa * desconto_aplicado * cobertura
    economia_anual = economia_mensal * 12

    return (
        round(economia_anual, 2),
        round(economia_mensal, 2),
        round(desconto_aplicado, 2),
        round(cobertura, 2),
    )


    if __name__ == "__main__":
      print("Testando...")

    assert calculadora([1518, 1071, 968], "Industrial", "BANDEIRA VERMELHA 2") == (
        1349.86,
        112.49,
        0.12,
        0.90,
    ) 

    assert calculadora([1000, 1054, 1100], "Residencial", "BANDEIRA VERMELHA 1") == (
        1725.61,
        143.8,
        0.18,
        0.90
    )

    assert calculadora([973, 629, 726], "Comercial", "BANDEIRA AMARELA") == (
        1097.6,
        91.47,
        0.16,
        0.90
    )

    assert calculadora([15000, 14000, 16000], "Industrial", "BANDEIRA VERMELHA 1") == (
        21656.81,
        1804.73,
        0.15,
        0.95
    )

    assert calculadora([12000, 11000, 11400], "Residencial", "BANDEIRA VERDE") == (
        22997.8,
        1916.48,
        0.22,
        0.95
    )

    assert calculadora([17500, 16000, 16400], "Comercial", "BANDEIRA AMARELA") == (
        27938.08,
        2328.17,
        0.18,
        0.95
    )

    assert calculadora([30000, 29000, 29500], "Industrial", "BANDEIRA VERMELHA 1") == (
        53262.07,
        4438.51,
        0.18,
        0.99
    )

    assert calculadora([22000, 21000, 21400], "Residencial", "BANDEIRA AMARELA") == (
        52186.84,
        4348.9,
        0.25,
        0.99
    )

    assert calculadora([25500, 23000, 21400], "Comercial", "BANDEIRA VERDE") == (
        48697.35,
        4058.11,
        0.22,
        0.99
    )

print("Todos os testes passaram!")