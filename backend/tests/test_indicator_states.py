import sys, os

#PATHS
TEST_DIR=os.path.realpath(os.path.dirname(__file__))
BASE_DIR=os.path.dirname(TEST_DIR)
sys.path.append(BASE_DIR)

from rimsboard.logic import IndicatorState, IndicatorStateGroup, ISTATES


def utils_intialise_access():
    lab1 = IndicatorState('analytical_chem', ISTATES.off )
    lab2 = IndicatorState('radiography', ISTATES.fail, label="RAD")
    lab3 = IndicatorState('materials_science', ISTATES.ready)

    access = IndicatorStateGroup('Access', [lab1, lab2, lab3])
    
    return access

def test_create_state():
    lab1 = IndicatorState('analytical_chem', ISTATES.off )
    lab2 = IndicatorState('radiography', ISTATES.fail, label="RAD")

    expected1 = {'key': 'analytical_chem', 'label': 'analytical_chem', 'state': 'off'}
    expected2 = {'key': 'radiography', 'label': 'RAD', 'state': 'fail'}

    assert lab1.to_dict() == expected1
    assert lab2.to_dict() == expected2

def test_create_stategroup():
    access = utils_intialise_access()

    expected = {'key': 'Access',
                'label': 'Access',
                'indicators': [
                    {'key': 'analytical_chem', 'label': 'analytical_chem', 'state': 'off'},
                    {'key': 'radiography', 'label': 'RAD', 'state': 'fail'},
                    {'key': 'materials_science', 'label': 'materials_science', 'state': 'ready'}
                ]}    

    result = access.to_dict()

    assert result == expected

def test_get_substate():
    access = utils_intialise_access()

    expected = 'fail'    

    result = access.get('radiography')

    assert result == expected

def test_assign_substate():
    access = utils_intialise_access()

    expected = {'key': 'Access',
                'label': 'Access',
                'indicators': [
                    {'key': 'analytical_chem', 'label': 'analytical_chem', 'state': 'off'},
                    {'key': 'radiography', 'label': 'RAD', 'state': 'ready'},
                    {'key': 'materials_science', 'label': 'materials_science', 'state': 'ready'}
                ]}    

    access.assign('radiography', ISTATES.ready)

    result = access.to_dict()

    assert result == expected

    expected = ISTATES.ready    

    result = access.get('radiography')

    assert result == expected



def test_add_state():
    lab4 = IndicatorState('softmatter', ISTATES.ready, label="soft")
    access = utils_intialise_access()
    
    expected = {'key': 'Access',
                'label': 'Access',
                'indicators': [
                    {'key': 'analytical_chem', 'label': 'analytical_chem', 'state': 'off'},
                    {'key': 'radiography', 'label': 'RAD', 'state': 'fail'},
                    {'key': 'materials_science', 'label': 'materials_science', 'state': 'ready'},
                    {'key': 'softmatter', 'label': 'soft', 'state': 'ready'}
                ]}  
    
    access.add(lab4)

    result = access.to_dict()

    assert result == expected    


def UNUSED_test_add_subgroup():
    uprop1=IndicatorState('user_ready', ISTATES.off)
    uprop2=IndicatorState('has_account', ISTATES.ready)

    access = utils_intialise_access()

    user_properties=IndicatorStateGroup('Access', [uprop1, uprop2, access])

    expected = {'key': 'Access',
                'label': 'Access',
                'indicators': [
                    {'key': 'user_ready', 'label': 'user_ready', 'state': 'off'},
                    {'key': 'has_account', 'label': 'has_account', 'state': 'ready'},
                    {'key': 'Access',
                    'label': 'Access',
                    'indicators': [
                        {'key': 'analytical_chem','label': 'analytical_chem','state': 'off'},
                        {'key': 'radiography', 'label': 'RAD', 'state': 'fail'},
                        {'key': 'materials_science','label': 'materials_science','state': 'ready'}
                    ]}
                ]}

    result = user_properties.to_dict()

    assert result == expected   

def UNUSED_test_flatten_subgroup():
    uprop1=IndicatorState('user_ready', ISTATES.off)
    uprop2=IndicatorState('has_account', ISTATES.ready)

    access = utils_intialise_access()

    user_properties=IndicatorStateGroup('Access', [uprop1, uprop2, access])

    expected = {'key': 'Access',
                'label': 'Access',
                'indicators': [
                    {'key': 'user_ready', 'label': 'user_ready', 'state': 'off'},
                    {'key': 'has_account', 'label': 'has_account', 'state': 'ready'},
                    {'key': 'analytical_chem','label': 'analytical_chem','state': 'off'},
                    {'key': 'radiography', 'label': 'RAD', 'state': 'fail'},
                    {'key': 'materials_science','label': 'materials_science','state': 'ready'}
                    ]
                }   
    
    result = user_properties.flat()

    result = result.to_dict()

    assert result == expected    

def UNUSED_test_flatten_recursive():
    #to-do: check for double-stacked subgroups handled by recursive flattening in stategroup.flat()
    pass
