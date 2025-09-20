# Run the SPOTL++ kit in Docker

## 0) Build the image
```bash
docker build -t spotlpp-kit:latest .
# or: make build
```

## 1) UD -> SPOTL++ conversion demo (4 toy sentences)
```bash
docker run --rm spotlpp-kit:latest \
  python converters/run_convert_demo.py converters/demo_ud.jsonl
# or: make demo-convert
```

## 2) Minimal verdict demo (as-of example)
```bash
docker run --rm spotlpp-kit:latest \
  python examples/run_pipeline_demo.py
# or: make demo-verdict
```

## 3) Interactive shell
```bash
docker run --rm -it spotlpp-kit:latest /bin/bash
# or: make sh
```

## 4) Using your own UD JSON
Mount your current folder into the container and point the converter to your file:
```bash
docker run --rm -v "$PWD":/workspace -w /workspace spotlpp-kit:latest \
  python converters/run_convert_demo.py path/to/your_ud.jsonl
```

> Notes
> - The demo does **not** parse UD by itself; it only converts a simplified UD JSON into SPOTL++.
> - To integrate real UD parsers (stanza / spaCy), add them to `requirements.txt` and rebuild the image.
