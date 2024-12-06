import logging

import rimsdash.config as config

logger = logging.getLogger('rimsdash')



def log_sync_error(label, id):
    """
    logs an error during syncing
    handles the case that the id itself does not exist
    """
    try:
        logger.error(f"Failure syncing {label} at id: {id}")
    except:
        logger.error(f"Failure syncing item, id/label missing", exc_info=True)

def log_processing_error(label, id):
    """
    logs an error during processing
    handles the case that the id itself does not exist
    """
    try:
        logger.error(f"Failure processing {label} at id: {id}")
    except:
        logger.error(f"Failure processing item, id/label missing", exc_info=True)


def match_project_account_pair(projectaccount_list: list[dict], bcode: str, project_id: int) -> dict:
    """
    find the corresponding project-account pair in a rims projacc list
    
    does not check for duplicates    
    """

    for __projacc in projectaccount_list:
        if __projacc['bcode'] == bcode and __projacc['project_id'] == project_id:
            return __projacc     

    #if not found, warn and return the ids with valid = None
    logger.warn(f"pair | pid: {project_id} | bcode: {bcode} | not found in RIMS project-account report, setting valid = None")    
    return { 'bcode': bcode, 'project_id': project_id, 'valid': None }
