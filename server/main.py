import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"

app = FastAPI(
    title="API de Previsão do Tempo",
    description="Servidor que consome a OpenWeatherMap e expõe endpoints de clima.",
    version="1.0.0",
)


# ── Modelos de resposta ────────────────────────────────────────────────────────

class ClimaAtual(BaseModel):
    city: str
    country: str
    temperature_c: float
    feels_like_c: float
    humidity_pct: int
    description: str
    wind_speed_ms: float
    icon: str


class ItemPrevisao(BaseModel):
    datetime: str
    temperature_c: float
    feels_like_c: float
    humidity_pct: int
    description: str
    icon: str


class Previsao(BaseModel):
    city: str
    country: str
    forecast: list[ItemPrevisao]


# ── Função auxiliar ────────────────────────────────────────────────────────────

async def fetch_openweather(endpoint: str, city: str) -> dict:
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OPENWEATHER_API_KEY não configurada.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Cidade '{city}' não encontrada.")
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Chave da API inválida.")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Não foi possível conectar à OpenWeatherMap.")


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/api/weather", response_model=ClimaAtual, summary="Clima atual")
async def clima_atual(city: str = Query(..., description="Nome da cidade. Ex: Campinas")):
    """Retorna o clima atual da cidade informada."""
    data = await fetch_openweather("weather", city)

    return ClimaAtual(
        city=data["name"],
        country=data["sys"]["country"],
        temperature_c=data["main"]["temp"],
        feels_like_c=data["main"]["feels_like"],
        humidity_pct=data["main"]["humidity"],
        description=data["weather"][0]["description"],
        wind_speed_ms=data["wind"]["speed"],
        icon=data["weather"][0]["icon"],
    )


@app.get("/api/forecast", response_model=Previsao, summary="Previsão 5 dias")
async def previsao(city: str = Query(..., description="Nome da cidade. Ex: São Paulo")):
    """Retorna a previsão de tempo para os próximos 5 dias (intervalos de 3h)."""
    data = await fetch_openweather("forecast", city)

    return Previsao(
        city=data["city"]["name"],
        country=data["city"]["country"],
        forecast=[
            ItemPrevisao(
                datetime=item["dt_txt"],
                temperature_c=item["main"]["temp"],
                feels_like_c=item["main"]["feels_like"],
                humidity_pct=item["main"]["humidity"],
                description=item["weather"][0]["description"],
                icon=item["weather"][0]["icon"],
            )
            for item in data["list"]
        ],
    )
