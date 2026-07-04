setup:
	python3 -m venv venv
	./venv/bin/python -m pip install -r requirements.txt

dev:
	./scripts/dev.sh

backend:
	cd backend && ../venv/bin/python -m uvicorn main:app --reload --port 8000

frontend:
	./venv/bin/streamlit run streamlit_app.py --server.port 8501
