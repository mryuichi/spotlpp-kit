
# SPOTL++ (English) mini-kit with UD->SPOTL++ demo

This branch adds SPOTL++ roles (M/A/C/R/Qn) and a tiny UD->SPOTL++ converter demo
covering "reported/said" (A), "as of YEAR" (C/T), "higher than ..." (R), and "may" (M).

## Quick start
1) UD->SPOTL++ conversion:
```
python converters/run_convert_demo.py converters/demo_ud.jsonl
```
2) Toy verdict using SPOTL++ dicts:
```
python examples/run_pipeline_demo.py
```

> This is a didactic scaffold. Replace the converter with real UD parses (stanza/spaCy) and
> extend patterns (negation scope, only, per-capita, correlation vs causation, etc.).
