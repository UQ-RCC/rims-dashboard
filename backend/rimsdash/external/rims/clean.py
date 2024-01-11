import re

#username cleanup
UQ_STUDENT_PATTERN = r'\s*\(\s*[sS]+[0-9]{5,8}\s*\)'
    #   brackets w/ "s" followed by 5-8 digits
UQ_STAFF_PATTERN = r'\s*\(\s*uq[a-z]{3,5}[a-z0-9]{0,2}\s*\)'
    #   brackets w/ "uq" followed by 3-5 lowercase and 0-2 lowercase or numbers
EXTERNAL_ID_PATTERN = r'\s*\(\s*[a-z0-9]+\.[a-z0-9]+\s*\)'
    #   brackets w/ lowercase/numbers + "." + lowercase/numbers

def strip_brackets(name: str):
    """
    remove usernames in brackets from user full names

    NB: want to keep aliases/nicknames while removing username-formatted content
    """
    pattern = UQ_STUDENT_PATTERN + '|' + UQ_STAFF_PATTERN + '|' + EXTERNAL_ID_PATTERN

    match = re.search(pattern, name)

    if match:
        return re.sub(pattern, '', name)
    else:
        return name

#title/description cleanup
GENERAL_SPECIALCHAR_PATTERN = r'\[\[.*\]\]'
SQUOTE_PATTERN = r'\[\[sqote\]\]'
DQUOTE_PATTERN = r'\[\[dqote\]\]'
AMPERSAND_PATTERN = r'\[\[and\]\]'
GREATERTHAN_PATTERN = r'\[\[gt\]\]'
LESSTHAN_PATTERN = r'\[\[lt\]\]'

def fix_special_chars(text: str):
    """
    cleanup RIMS internal subtitutions for special chars

    eg. [[sqote]], [[and]]
    """

    result = text

    if re.search(GENERAL_SPECIALCHAR_PATTERN, result):
        result = re.sub(SQUOTE_PATTERN, '\'', result)
        result = re.sub(DQUOTE_PATTERN, '\"', result)        
        result = re.sub(AMPERSAND_PATTERN, '&', result)
        result = re.sub(GREATERTHAN_PATTERN, '>', result)
        result = re.sub(LESSTHAN_PATTERN, '<', result)                

    return result