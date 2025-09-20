"""
Very light UD->SPOTL++ converter for English demo.
See README for the simplified UD JSON format.
"""
from typing import Dict, Any, List
from spotl_core.roles import SpotlPP

def _has(dep_list, dep, child=None, head=None):
    for d in dep_list:
        if d.get("dep")==dep and (child is None or d.get("child")==child) and (head is None or d.get("head")==head):
            return True
    return False

def convert_sentence(ud: Dict[str,Any]) -> SpotlPP:
    deps = ud.get("deps", [])
    txt  = ud.get("text","")
    out = SpotlPP()
    # Attribution
    for verb in ("said","reported","claimed","announced"):
        if any(d.get("head")==verb for d in deps):
            speakers = [d.get("child") for d in deps if d.get("dep")=="nsubj" and d.get("head")==verb]
            if speakers: out.A.extend(speakers)
            contents = [d.get("child") for d in deps if d.get("dep") in ("ccomp","xcomp") and d.get("head")==verb]
            if contents:
                out.P.extend(["content:"+c for c in contents])
            break
    # Negation cue
    if _has(deps, "neg"):
        out.M.append("negated")
    # Modal auxiliaries
    for modal in ("may","might","likely","possibly","could"):
        if any(d.get("child")==modal and d.get("dep").startswith("aux") for d in deps):
            out.M.append(modal)
    # As-of time
    for d in deps:
        if d.get("dep").startswith("obl") and "as of" in (d.get("child","").lower()):
            out.C.append("as-of")
            yr = "".join([c for c in d.get("child") if c.isdigit() or c=="-"])
            if yr: out.T.append(yr)
    # Comparison "than ..."
    if any(d.get("child")=="than" or d.get("dep")=="mark:than" for d in deps):
        refs = [d.get("child") for d in deps if "than" in (d.get("head","")+d.get("child","")) and d.get("dep") in ("nmod","obl","nummod","amod")]
        if refs: out.R.extend(refs)
        comps = [d.get("head") for d in deps if d.get("child")=="than"]
        if comps: out.P.extend([f"comparative:{c}" for c in comps])
    # Basic S/O/T/P
    out.S.extend([d.get("child") for d in deps if d.get("dep")=="nsubj"])
    out.O.extend([d.get("child") for d in deps if d.get("dep") in ("obj","dobj")])
    out.T.extend([d.get("child") for d in deps if d.get("dep").startswith("obl:tmod") and "as of" not in (d.get("child","").lower())])
    out.P.extend([d.get("head") for d in deps if d.get("dep")=="root"])
    # Dedup
    for k in ["S","P","O","T","L","M","A","C","R","Qn"]:
        v = getattr(out,k)
        setattr(out,k, list(dict.fromkeys([x for x in v if x])))
    out.meta["source"] = "ud2spotlpp_demo"
    out.meta["text"] = txt
    return out

def convert_batch(rows: List[Dict[str,Any]]) -> List[Dict[str,Any]]:
    return [{"text": r.get("text",""), "spotlpp": convert_sentence(r).to_dict()} for r in rows]
