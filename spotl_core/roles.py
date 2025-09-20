
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SpotlPP:
    S: List[str] = field(default_factory=list)
    P: List[str] = field(default_factory=list)
    O: List[str] = field(default_factory=list)
    T: List[str] = field(default_factory=list)
    L: List[str] = field(default_factory=list)
    M: List[str] = field(default_factory=list)  # Modality
    A: List[str] = field(default_factory=list)  # Attribution
    C: List[str] = field(default_factory=list)  # Condition / As-of
    R: List[str] = field(default_factory=list)  # Reference (comparative base)
    Qn: List[str] = field(default_factory=list) # Quantifier type
    meta: Dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> Dict[str, Any]:
        return {"S":self.S,"P":self.P,"O":self.O,"T":self.T,"L":self.L,
                "M":self.M,"A":self.A,"C":self.C,"R":self.R,"Qn":self.Qn,"meta":self.meta}
