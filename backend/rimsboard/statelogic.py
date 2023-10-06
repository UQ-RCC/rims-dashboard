from dataclasses import dataclass, asdict, field, fields, Field
from enum import Enum
from typing import Tuple

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


@dataclass
class UserState:
    total: str = Istate.off
    active: str = Istate.off
    access_aibn: str = Istate.off
    access_hawken: str = Istate.off
    access_chem: str = Istate.off
    access_qbp: str = Istate.off

    #label enum as dict
    state_labels: dict = field(default_factory=lambda: {i.name: i.value for i in UserStateLabels})

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

    def get_header_list(self):
        result = []

        for key, value in self.state_labels.items():
            result.append(value)
        
        return result

    def as_indicators(self):

        result = []

        #initialise fields
        cls_fields: Tuple[Field, ...] = fields(self.__class__)
        
        for field in cls_fields:
            #iterate through fields, appending all str 
            if issubclass(field.type, str):
                local_state=getattr(self,field.name)

                field_result = {
                    'key': field.name,
                    'label': self.state_labels[str(field.name)],
                    'value': str(local_state.value),                    
                }
                result.append(field_result)
        
        return result


@dataclass
class ProjectState:
    total: str = Istate.off
    active: str = Istate.off
    billing: str = Istate.off
    ohs: str = Istate.off
    rdm: str = Istate.off
    phase: str = Istate.off

    #label enum as dict
    state_labels: dict = field(default_factory=lambda: {i.name: i.value for i in ProjectStateLabels})

    def get_header_list(self):
        result = []

        for key, value in self.state_labels.items():
            result.append(value)
        
        return result

    def as_indicators(self):

        result = []

        #initialise fields
        cls_fields: Tuple[Field, ...] = fields(self.__class__)
        
        for field in cls_fields:
            #iterate through fields, appending all str 
            if issubclass(field.type, str):
                local_state=getattr(self,field.name)

                field_result = {
                    'key': field.name,
                    'label': self.state_labels[str(field.name)],                    
                    'value': str(local_state.value),  
                }
                result.append(field_result)
        
        return result