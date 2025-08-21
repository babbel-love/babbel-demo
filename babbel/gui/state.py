session_state = {
    'emotion': None,
    'tone': None,
    'node': None,
    'memory': [],
    'strict': True
}

def update_state(metadata: dict):
    session_state['emotion'] = metadata.get('emotion')
    session_state['tone'] = metadata.get('tone')
    session_state['node'] = metadata.get('node')
    session_state['memory'].append(metadata)

