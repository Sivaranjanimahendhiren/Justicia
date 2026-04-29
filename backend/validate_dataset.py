import json, os
path = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'legal_cases_dataset.json')
with open(path) as f:
    data = json.load(f)
print(f"Valid JSON. Total cases: {len(data)}")
cats = {}
for c in data:
    cats[c["category"]] = cats.get(c["category"], 0) + 1
for k, v in sorted(cats.items()):
    print(f"  {k}: {v} cases")
print("\nSample case:")
print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500])
