from rimsdash.models import SystemRight, ProjectRight, IStatus, AdminRight


def consolidate_duplicate_rights(user_rights: list[dict]) -> list[dict]:
    """
    Tidy up user rights for a single user

    keeps highest right level where multiple rights for a single system are recorded

    defines highest right based on reverse of index where SystemRight is declared

    """

    #use the Enum indexes, as declared, for the sort key
    user_rights_sorted = sorted(user_rights, key=lambda d: list(SystemRight).index(d['status']), reverse=True)

    systems_encountered = []
    result = []

    for right in user_rights_sorted:
        if right['system_id'] not in systems_encountered:
            result.append(right)
            systems_encountered.append(right['system_id'])

    return result

