
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


# ── Helpers ────────────────────────────────────────────────────────────────────

def separador(char="─", largura=50):
    print(char * largura)


def cabecalho(titulo):
    separador("═")
    print(f"  {titulo}")
    separador("═")


# ── Consumo da API ─────────────────────────────────────────────────────────────

def buscar_clima_atual(city: str) -> dict | None:
    try:
        resp = requests.get(f"{BASE_URL}/api/weather", params={"city": city}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print(f"\n[ERRO] Não foi possível conectar ao servidor em {BASE_URL}.")
        print("  Verifique se o servidor FastAPI está rodando.\n")
        return None
    except requests.exceptions.HTTPError:
        print(f"\n[ERRO] {resp.status_code} — {resp.json().get('detail', 'Erro desconhecido')}\n")
        return None


def buscar_previsao(city: str) -> dict | None:
    try:
        resp = requests.get(f"{BASE_URL}/api/forecast", params={"city": city}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print(f"\n[ERRO] Não foi possível conectar ao servidor em {BASE_URL}.")
        print("  Verifique se o servidor FastAPI está rodando.\n")
        return None
    except requests.exceptions.HTTPError:
        print(f"\n[ERRO] {resp.status_code} — {resp.json().get('detail', 'Erro desconhecido')}\n")
        return None


# ── Exibição ───────────────────────────────────────────────────────────────────

def exibir_clima_atual(dados: dict):
    cabecalho(f"Clima Atual — {dados['city']}, {dados['country']}")
    print(f"    Temperatura  : {dados['temperature_c']:.1f} °C")
    print(f"    Sensação     : {dados['feels_like_c']:.1f} °C")
    print(f"    Umidade      : {dados['humidity_pct']} %")
    print(f"    Vento        : {dados['wind_speed_ms']} m/s")
    print(f"    Condição     : {dados['description'].capitalize()}")
    separador()


def exibir_previsao(dados: dict):
    cabecalho(f"Previsão 5 Dias — {dados['city']}, {dados['country']}")
    for item in dados["forecast"]:
        print(f"\n    {item['datetime']}")
        print(f"      Temp      : {item['temperature_c']:.1f} °C  (sensação {item['feels_like_c']:.1f} °C)")
        print(f"      Umidade   : {item['humidity_pct']} %")
        print(f"      Condição  : {item['description'].capitalize()}")
    separador()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "═" * 50)
    print("   CLIENTE — API de Previsão do Tempo")
    print("═" * 50)

    city = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("\nDigite o nome da cidade: ").strip()

    if not city:
        print("[ERRO] Nenhuma cidade informada. Encerrando.")
        sys.exit(1)

    print(f"\nConsultando dados para: {city!r}\n")

    clima = buscar_clima_atual(city)
    if clima:
        exibir_clima_atual(clima)

    previsao = buscar_previsao(city)
    if previsao:
        exibir_previsao(previsao)


if __name__ == "__main__":
    main()
