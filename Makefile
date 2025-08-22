.PHONY: install test scan check ci

install:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt -e .

test:
	pytest

scan:
	bash scripts/gpt_proof_scan.sh

check: scan test

ci: check
