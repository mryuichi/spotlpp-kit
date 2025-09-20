from spotl_core.scoring_pp import role_alignment_pp, aggregate_sentence_pp, verdict_from_scores_pp

claim = {"S":["service"], "P":["free"], "T":["2024"], "C":["as-of"]}
evidences = [
    {"S":["service"], "P":["free"], "T":["2024"], "C":["as-of"]},
    {"S":["service"], "P":["free"], "T":["2022"], "C":["as-of"]},
    {"S":["service"], "P":["fee required"], "T":["2024"], "C":["as-of"]},
]
critical = ["S","P","T"]
doc_scores = []
for ev in evidences:
    sc = role_alignment_pp(claim, ev)
    s,r,cov = aggregate_sentence_pp(sc, critical)
    doc_scores.append((s,r,cov))
label, meta = verdict_from_scores_pp(doc_scores, 0.6, 0.6, 0.5)
print("VERDICT:", label, meta)
for i,(s,r,c) in enumerate(doc_scores,1):
    print(f"EV{i}: supp={s:.2f} refu={r:.2f} cov={c:.2f}")
