# Mini Projeto 3 — Consumo de APIs

> ⚠️ Este repositório é um projeto didático. Não utilize este código em produção sem revisar as configurações de segurança.

API de previsão do tempo construída com **FastAPI**.  
O servidor expõe endpoints que consultam a [OpenWeatherMap API](https://openweathermap.org/api).  
O cliente consome esses endpoints via `requests`.

---

## Estrutura

```
meu_projeto_fastapi/
├── README.md
├── requirements.txt
├── server/
│   ├── .env.example
│   └── main.py
└── client/
    ├── .env.example
    └── main.py
```

---

## Pré-requisitos

- Python 3.10+
- Chave de API gratuita da OpenWeatherMap → https://home.openweathermap.org/users/sign_up DETALHE IMPORTANTE: A chave API do OpenWeatherMap pode demorar até 2 horas para ser validada.

---

## Criando o ambiente (VS Code)

**1. Abra a pasta do projeto no VS Code e abra o terminal integrado (Ctrl+').**

**2. Crie e ative o ambiente virtual:**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

Após ativar, o terminal exibirá `(venv)` no início da linha. O VS Code também vai detectar automaticamente e perguntar se deseja usar o interpretador do venv — clique em **Yes**.

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

---

## Configurando e rodando o servidor

**1. Copie o arquivo de variáveis de ambiente:**
```bash
cd server
cp .env.example .env
```

**2. Preencha a chave da OpenWeatherMap no `.env`:**
```
OPENWEATHER_API_KEY=sua_chave_aqui
```

**3. Rode o servidor:**
```bash
cd server (caso tenha fechado o terminal após o passo 1 e 2)
uvicorn main:app --reload
```

O servidor ficará disponível em `http://127.0.0.1:8000`.

> **Dica:** o FastAPI gera automaticamente uma documentação interativa em `http://127.0.0.1:8000/docs` onde você pode testar os endpoints direto pelo navegador.

### Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/api/weather?city=<cidade>` | Clima atual da cidade |
| GET | `/api/forecast?city=<cidade>` | Previsão para os próximos 5 dias |

---

## Configurando e rodando o cliente

```bash
cd client
cp .env.example .env
python main.py
```

Ou passando a cidade direto como argumento:
```bash
python main.py Campinas
```

---

## Exemplo de resposta — `/api/weather?city=Campinas`

```json
{
  "city": "Campinas",
  "country": "BR",
  "temperature_c": 24.3,
  "feels_like_c": 23.8,
  "humidity_pct": 72,
  "description": "céu limpo",
  "wind_speed_ms": 3.1,
  "icon": "01d"
}
```
