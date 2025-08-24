.PHONY: test run scan ci seed export-all
test:
	pytest -q
run:
	python -m streamlit run streamlit_babbel_app.py
scan:
	bash scripts/deny_scan.sh
ci: scan test
seed:
	python scripts/seed_sessions.py
export-all:
	python scripts/export_all.py
