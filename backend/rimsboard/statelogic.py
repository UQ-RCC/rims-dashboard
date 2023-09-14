from dataclasses import dataclass, asdict, field
from enum import Enum

red2 = "yes"

class Istate(Enum):
    """
    enum for indicator state values
    """    
    #in progress------- 
    off = 'off'
    incomplete = 'incomplete'
    waiting = 'waiting'
    ready = 'ready'
    extended = 'extended'    
    disabled = 'disabled'   
    #error------------
    warn = 'warn'
    fail = 'fail'
    na = 'na'

@dataclass
class UserState:
    total: str = Istate.off
    active: str = Istate.off
    access_aibn: str = Istate.off
    access_hawken: str = Istate.off
    access_chem: str = Istate.off
    access_qbp: str = Istate.off

    def labs_as_list(self):
        return [ self.access_aibn, self.access_hawken, self.access_chem, self.access_qbp]

    def assign_by_lab(self, lab: str, value: str):

        a=1

        if lab == "aibn":
            self.access_aibn = value
        elif lab == "hawken":
            self.access_hawken = value
        elif lab == "chem":
            self.access_chem = value
        elif lab == "qbp":
            self.access_qbp = value
        else:
            raise ValueError(f"invalid lab {lab}")

@dataclass
class ProjectState:
    total: str = Istate.off
    active: str = Istate.off
    billing: str = Istate.off
    ohs: str = Istate.off
    rdm: str = Istate.off
    phase: str = Istate.off

class UserStateLabels(Enum):
    total = 'OK'
    active = 'Active'
    access_aibn = 'AIBN'
    access_hawken = 'Hawken'
    access_chem = 'Chem'
    access_qbp = 'QBP'

class ProjectStateLabels(Enum):
    total = 'OK'
    active = 'Active'
    billing = 'Billing'
    ohs = 'OHS'
    rdm = 'RDM'
    phase = 'Phase'