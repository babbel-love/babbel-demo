#!/bin/bash
source .venv/bin/activate
black .
isort .
echo "Code formatted."
