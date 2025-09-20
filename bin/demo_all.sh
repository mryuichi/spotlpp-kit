#!/usr/bin/env bash
set -euo pipefail
IMAGE=${IMAGE:-spotlpp-kit:latest}
docker build -t "$IMAGE" .
echo "== UD -> SPOTL++ =="
docker run --rm "$IMAGE" python converters/run_convert_demo.py converters/demo_ud.jsonl
echo "== Verdict demo =="
docker run --rm "$IMAGE" python examples/run_pipeline_demo.py
