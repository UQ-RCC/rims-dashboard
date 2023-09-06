import copy

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

   
    def group_check(self):
        """
        check if current instance is a state_group
        REMOVE
        """        
        if not ( type(self.indicators) is list):
            raise TypeError(f"State {self.key} is not group of states")

    def add(self, indicator):   
        """
        add an instance of state if current instance is a state_group
        """   

        #recursive, takes instance of State(), not sure how to type hint
        #   check by attributes
        if ( hasattr(indicator, 'key') and hasattr(indicator, 'label') and hasattr(indicator, 'state') ):
            for i in self.indicators:
                if i.key == indicator.key:
                    raise ValueError(f"State {indicator.key} already in group {self.indicators}")

            self.indicators.append(indicator)     
        else:
            raise ValueError(f"{indicator.key} is not valid state to append")
   

    def assign(self, keys, state):
        """
        assign value to state from list of keys
        """ 
        if type(keys) is str:
            keys = [ keys ]
        if type(keys) is list:
            pass

        else:
            raise TypeError(f"unexpected type for keys {keys}")

        #move into nested groups using keys list
        i=0
        current=self
        while i < len(keys):
            if ( hasattr(sub, 'indicators')):
                for sub in current.indicators:
                    if sub.key == keys[i]:
                        current = sub
                        i+=1
            else:
                raise TypeError(f"expected subgroup at {sub.key}, aborting assignment")

        #assign only if types match
        if ( hasattr(current, 'indicators')) and ( type(state) is list ):
                current.indicators = state
        elif ( hasattr(current, 'state')) and ( type(state) is str ):
                current.state = state
        else:
            raise TypeError(f"mismatch between input {type(state)} and target {current.key}")


    def get_state(self, key):
        """
        return state from key

        to-do: correct this for nested groups similar to assign()
        """

        for i in self.indicators:
            if i.key == key:
                return(i.state)

    def to_dict(self):
        """
        return as nested dicts
        """

        sub_result = [] 
        for i in self.indicators:
            sub_result.append(i.to_dict())

        return { 'key': self.key, 'label': self.label, 'indicators': sub_result }

    def flat(self):
        """
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

