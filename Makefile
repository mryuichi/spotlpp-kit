
IMAGE ?= spotlpp-kit:latest

.PHONY: build sh demo-convert demo-verdict

build:
	docker build -t $(IMAGE) .

sh: build
	docker run --rm -it $(IMAGE)

demo-convert: build
	docker run --rm $(IMAGE) python converters/run_convert_demo.py converters/demo_ud.jsonl

demo-verdict: build
	docker run --rm $(IMAGE) python examples/run_pipeline_demo.py
