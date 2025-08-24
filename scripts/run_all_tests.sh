#!/bin/bash
echo "Running all Babbel tests..."
pytest tests/ --tb=short -q
