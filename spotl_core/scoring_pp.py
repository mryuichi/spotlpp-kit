from typing import Dict, Any, List, Tuple
from .normalizers_en import norm_number, norm_percent, norm_date

def jaccard_chars(a: str, b: str, n: int = 3) -> float:
    if not a or not b: return 0.0
    def ngrams(s):
        s = ''.join(s.lower().split())
        return {s[i:i+n] for i in range(len(s)-n+1)} if len(s)>=n else {s.lower()}
    A,B = ngrams(a), ngrams(b)
    if not A or not B: return 0.0
    return len(A & B)/len(A | B)

def role_alignment_pp(claim: Dict[str,Any], ev: Dict[str,Any]) -> Dict[str, Dict[str, float]]:
    out = {}
    for R in ["S","P","O","T","L"]:
        ent, con = 0.0, 0.0
        for c in claim.get(R, []):
            for e in ev.get(R, []):
                if R=="O":
                    pc, pe = None, None
                    if isinstance(c,str): pc = norm_percent(c)
                    if isinstance(e,str): pe = norm_percent(e)
                    if pc is not None and pe is not None:
                        diff = abs(pc-pe)
                        ent = max(ent, max(0.0, 1.0 - diff*10.0))
                        con = max(con, 1.0 if diff>0.25 else con)
                        continue
                    nc = norm_number(c) if isinstance(c,str) else None
                    ne = norm_number(e) if isinstance(e,str) else None
                    if nc is not None and ne is not None:
                        rel = abs(nc-ne)/max(1.0, max(abs(nc),abs(ne)))
                        ent = max(ent, max(0.0, 1.0 - rel*4.0))
                        con = max(con, 1.0 if rel>0.6 else con)
                        continue
                if R=="T":
                    dc = norm_date(c) if isinstance(c,str) else None
                    de = norm_date(e) if isinstance(e,str) else None
                    if dc and de:
                        yd = abs(dc[0]-de[0]) + abs(dc[1]-de[1])/12.0
                        ent = max(ent, 1.0 if yd==0 else (0.7 if yd<=1 else 0.4))
                        con = max(con, 0.8 if yd>2 else con)
                        continue
                ent = max(ent, jaccard_chars(str(c), str(e)))
        out[R] = {"ent": round(ent,3), "con": round(con,3), "nei": round(1.0-max(ent,con),3)}
    return out

def aggregate_sentence_pp(scores: Dict[str, Dict[str, float]], critical: List[str]) -> Tuple[float,float,float]:
    ents = [scores.get(r,{}).get("ent",0.0) for r in critical]
    cons = [scores.get(r,{}).get("con",0.0) for r in critical]
    supp = min(ents) if ents else 0.0
    refu = max(cons) if cons else 0.0
    cov  = sum(1 for x in ents if x>0.0)/max(1,len(ents))
    return round(supp,3), round(refu,3), round(cov,3)

def verdict_from_scores_pp(doc_scores: List[Tuple[float,float,float]], theta_S=0.6, theta_R=0.6, theta_cov=0.5):
    Splus = max((s for s,_,_ in doc_scores), default=0.0)
    Rplus = max((r for _,r,_ in doc_scores), default=0.0)
    Gamma = max((c for _,_,c in doc_scores), default=0.0)
    if Gamma < theta_cov: return "NEI", {"S+":Splus, "R+":Rplus, "coverage":Gamma}
    if Splus >= theta_S and Rplus < theta_R: return "Supported", {"S+":Splus, "R+":Rplus, "coverage":Gamma}
    if Rplus >= theta_R and Splus < theta_S: return "Refuted", {"S+":Splus, "R+":Rplus, "coverage":Gamma}
    return "Conflicting", {"S+":Splus, "R+":Rplus, "coverage":Gamma}
