"""These are the manually defined rules for defining what 
rotations should the second box perform before it is eligible to be joined with the first box
on the desired faces.

For later implementation, use some sort of pattern instead for these rules to improve efficiency."""


_rotation_rules = {
    'front': {
        'front': 2*[0],
        'top': 3*[1],
        'left': [0],
        'right': 3*[0],
        'bottom': [1],
        'back': []
    },
    'top': {
        'front': [1],
        'top': 2*[2],
        'left': [2],
        'right': 3*[2],
        'bottom': [],
        'back': 3*[1]
    },
    'left': {
        'front': 3*[0],
        'top': 3*[2],
        'left': 2*[0],
        'right': [],
        'bottom': [2],
        'back': [0]
    },
    'right': {
        'front': [0],
        'top': [2],
        'left': [],
        'right': 2*[0],
        'bottom': 3*[2],
        'back': 3*[0]
    },
    'bottom': {
        'front': [0],
        'top': [],
        'left': 3*[2],
        'right': [2],
        'bottom': 2*[2],
        'back': [1]
    },
    'back': {
        'front': [],
        'top': [1],
        'left': 3*[0],
        'right': [0],
        'bottom': 3*[1],
        'back': 2*[0]
    }
}