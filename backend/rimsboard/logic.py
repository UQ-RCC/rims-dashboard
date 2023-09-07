import copy

import rimsboard.utils as utils

class IState():
    """
    collection of valid states to hand back
    """
    def __init__(self):
        #standard--------
        self.off = 'off'
        self.incomplete = 'incomplete'
        self.waiting = 'waiting'
        self.waiting_external = 'waiting_external'
        self.ready = 'ready'
        self.extended = 'extended'
        self.disabled = 'disabled'
        #error------------
        self.warn = 'warn'
        self.fail = 'fail'
        self.na = 'na'

ISTATES = IState()



class IndicatorState():
    """
    class to hold state values, and lists of state values
    """      
    def __init__(self, key: str, state: str, label:str =None):
        self.key = key
        self.state = state

        if label == None:
            self.label = key        
        else:
            self.label = label
    def to_dict(self):
        """
        return as nested dicts
        """

        return { 'key': self.key, 'label': self.label, 'state': self.state }


class IndicatorStateGroup():
    """
    class to hold state values, and lists of state values
    """      
    def __init__(self, key: str, indicators: list, label:str =None):
        self.key = key
        self.indicators = indicators

        if label == None:
            self.label = key        
        else:
            self.label = label

    def check(self):
        """
        check all keys are unique, including ISG key itself
        """           
        label_list = [ self.key ]

        for substate in self.indicators:
            label_list.append(substate.key)

        if not (utils.all_unique(label_list)):
            raise ValueError(f"non-unique keys in {label_list}")
     
    def add(self, indicator: IndicatorState):   
        """
        add a state to group
        """   
        for i in self.indicators:
            if i.key == indicator.key:
                raise ValueError(f"State {indicator.key} already in group {self.indicators}")

        self.indicators.append(indicator)     

    def assign(self, key: str, state: str):
        """
        assign value to state from list of keys
        """ 
        for i in self.indicators:
            if i.key == key:
                i.state = state

    def get(self, key):
        """
        return state from key
        
        """
        for i in self.indicators:
            if i.key == key:
                return(i.state)

    def getlabel(self, key):
        """
        return label from key
        
        """
        for i in self.indicators:
            if i.key == key:
                return(i.label)


    def to_dict(self):
        """
        return as nested dicts
        """

        sub_result = [] 
        for i in self.indicators:
            sub_result.append(i.to_dict())

        return { 'key': self.key, 'label': self.label, 'indicators': sub_result }



class MetaStateGroup():
    """
    TO-DO: unused
    """
    def __init__(self, key: str, indicators: list, label:str =None):
            self.key = key
            self.indicators = indicators

            if label == None:
                self.label = key        
            else:
                self.label = label


    def flat(self):
        """
        TO-DO: unused, taken from IndicatorSG()

        flatten nested subgroups into parent
        """        

        _target = copy.deepcopy(self)

        remove_list = []

        for subgroup in _target.indicators:

            #check if subcomponent is group
            if ( hasattr(subgroup, 'indicators')):
                try:
                    #check for further nesting and flatten recursively if needed
                    for substate in subgroup.indicators:
                        if ( hasattr(substate, 'indicators')):
                            subgroup = subgroup.flat()
                            break   #only need to run flat() once, will flatten out all sub-subgroups

                    #add sub-state to parent
                    for substate in subgroup.indicators:        
                        _target.add(substate)
                    
                    #flag subgroup for removal
                    remove_list.append(subgroup)

                except:
                    print(f"WARNING: flattening state instance {_target}, {_target.key} failed at {subgroup.key}, {substate.key}")
                    #remove any added js if there is a failure
        
        for subgroup in remove_list:
            _target.indicators.remove(subgroup)

        return _target

