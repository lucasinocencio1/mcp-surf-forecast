
# Surf Forecast

Create an MVP in Python that uses Open-Meteo Marine (free, no API key required) to forecast swell height, swell period, swell direction, and wind conditions.

## Como rodar

```bash
# 1) criar e ativar venv (opcional)
python -m venv .venv
source .venv/bin/activate  # mac/linux
# .venv\Scripts\activate  # windows

# 2) instalar deps
pip install -r requirements.txt

#3) to check backend CRUD
uvicorn backend.main:app --reload

# to check the frontend use  (here you can check the informations from the spot)

python -m streamlit run frontend/app.py
