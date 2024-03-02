TOTAL_PRESS_ONCE_TASKS = 3

flag = [0]*TOTAL_PRESS_ONCE_TASKS


def press_once(key, func, flag_indx, list, reset=True):
    """This function enables you to press a button and report it only once in a task
    instead of continuously reporting a button as down until it is unpressed.
    Use this function in a task function and pass number of the task being called. 
    Also change the TOTAL_PRESS_ONCE_TASKS value accordingly."""
    
    if not base.mouseWatcherNode.isButtonDown(key) and flag[flag_indx] == 2:
        flag[flag_indx] = 0
            
    if base.mouseWatcherNode.isButtonDown(key) and flag[flag_indx] == 0:
        flag[flag_indx] = 1
        
    if flag[flag_indx] == 1:
        if reset: list[1].reset_rotations()
        func(list)
        flag[flag_indx] = 2