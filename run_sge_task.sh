#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

source /share/apps/source_files/python/python-3.11.9.source
export PATH=/share/apps/cuda-11.8/bin:/share/apps/openssl-1.1.1/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/cuda-11.8/lib64:/share/apps/openssl-1.1.1/lib:$LD_LIBRARY_PATH

cd "$SCRIPT_DIR"

source ./venv/bin/activate

python run_sge_task.py "$@"

