#!/bin/bash
# Starts the Streamlit app with New Relic instrumentation
set -e
cd "$(dirname "$0")"         # always run from the script's own directory
source .venv/bin/activate
export AZURE_OPENAI_DISABLE_SSL=true   # bypass corporate proxy SSL inspection
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program streamlit run app.py --server.port 8501 --server.headless false
