#!/bin/bash
echo "Running all Babbel tests..."
PYTHONPATH=. pytest tests/ --tb=short -q
