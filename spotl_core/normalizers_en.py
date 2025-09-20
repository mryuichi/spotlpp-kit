
import re
from typing import Optional, Tuple

MONTHS = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
          "july":7,"august":8,"september":9,"october":10,"november":11,"december":12}

def month_to_num(m: str) -> Optional[int]:
    return MONTHS.get(m.lower())

def norm_number(s: str) -> Optional[float]:
    if not s: return None
    t = s.replace(",", "").strip().lower()
    m = re.match(r"^(-?\d+(?:\.\d+)?)(?:\s*(k|m|b|million|billion))?$", t)
    if not m: return None
    val = float(m.group(1))
    suf = m.group(2) or ""
    if suf == "k": val *= 1e3
    elif suf in ("m","million"): val *= 1e6
    elif suf in ("b","billion"): val *= 1e9
    return val

def norm_percent(s: str) -> Optional[float]:
    if not s: return None
    t = s.replace(",", "").strip().lower()
    m = re.match(r"^(-?\d+(?:\.\d+)?)\s*%$", t)
    if not m: return None
    return float(m.group(1))/100.0

def norm_money(s: str) -> Optional[float]:
    t = (s or "").replace(",", "").strip().lower()
    m = re.match(r"^\$?\s*(\d+(?:\.\d+)?)\s*(billion|million|k)?\b", t)
    if not m: return None
    val = float(m.group(1))
    suf = m.group(2) or ""
    if suf == "k": val *= 1e3
    elif suf == "million": val *= 1e6
    elif suf == "billion": val *= 1e9
    return val

def norm_date(s: str) -> Optional[Tuple[int,int,int]]:
    t = (s or "").strip()
    import re as _re
    m = _re.match(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$", t)
    if m: return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = _re.match(r"^(\d{4})[-/](\d{1,2})$", t)
    if m: return (int(m.group(1)), int(m.group(2)), 1)
    m = _re.match(r"^([A-Za-z]+)\s+(\d{4})$", t)
    if m: 
        mm = MONTHS.get(m.group(1).lower(), 1)
        return (int(m.group(2)), mm, 1)
    m = _re.match(r"^(\d{4})$", t)
    if m: return (int(m.group(1)), 1, 1)
    return None
