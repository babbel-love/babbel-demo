#!/bin/bash
source .venv/bin/activate
pytest tests/ --tb=short -q
