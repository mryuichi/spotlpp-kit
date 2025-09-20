
import json, sys
from ud2spotlpp import convert_batch
def main(path):
    rows = [json.loads(x) for x in open(path, encoding="utf-8")]
    for o in convert_batch(rows):
        print(json.dumps(o, ensure_ascii=False))
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "demo_ud.jsonl")
