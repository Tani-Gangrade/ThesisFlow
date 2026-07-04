.PHONY: help setup dev backend frontend

help:
	@echo "ThesisFlow development commands:"
	@echo "  make setup     Create venv and install Python dependencies"
	@echo "  make dev       Start FastAPI backend and Streamlit frontend"
	@echo "  make backend   Start only the FastAPI backend"
	@echo "  make frontend  Start only the Streamlit frontend"

setup:
	python3 -m venv venv
	./venv/bin/python -m pip install -r requirements.txt

dev:
	./scripts/dev.sh

backend:
	cd backend && ../venv/bin/python -m uvicorn main:app --reload --port 8000

frontend:
	./venv/bin/streamlit run streamlit_app.py --server.port 8501
