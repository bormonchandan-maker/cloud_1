p# Khoroch Tracker

Choto offline expense tracker: Python + Flask + SQLite. Internet lage na.

## 1) VS Code-e sorasori chalao (Docker chhara)
```
python -m venv .venv
.venv\Scripts\activate        # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Ba VS Code-e F5 chapo. Browser: http://127.0.0.1:5000

## 2) Docker diye chalao
```
docker compose up -d --build
```
Browser: http://localhost:5000

- Log: `docker compose logs -f`
- Bondho: `docker compose down` (data thake)
- Data-shoho muchhe fela: `docker compose down -v`

## File structure
- `app.py`  : pura backend (route + SQLite)
- `templates/index.html` : UI
- `Dockerfile`, `docker-compose.yml` : container setup
