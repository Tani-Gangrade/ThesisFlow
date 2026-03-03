.PHONY: dev backend frontend streamlit

dev:
	bash scripts/dev.sh

backend:
	bash -lc 'cd backend && source ../venv/bin/activate && python -m uvicorn main:app --port 8000'

frontend:
	cd frontend && npm run dev

streamlit:
	bash -lc 'cd /Users/tanishagangrade/Desktop/ThesisFlow && source venv/bin/activate && streamlit run streamlit_app.py'
