#returns all the key in a dictionary
def get_key(data):
    key = [key for key, value in data.items()]
    return key

def clear_metadata(id, options, selected_option, metadata):
    if id == 'name':
        metadata = {}
        metadata['name'] = {}
        if metadata.get('arg2') != None:
            metadata['arg2'] = {}
        if metadata.get('arg3') != None:
            metadata['arg3'] = {}
        if metadata.get('arg4') != None:
            metadata['arg4'] = {}
        if metadata.get('arg5') != None:
            metadata['arg5'] = {}
        metadata['name']['options'] = options
        metadata['name']['selected_option'] = selected_option
    if id == 'arg2':
        metadata['arg2'] = {}
        if metadata.get('arg3') != None:
            metadata['arg3'] = None
        if metadata.get('arg4') != None:
            metadata['arg4'] = None
        if metadata.get('arg5') != None:
            metadata['arg5'] = None
        metadata['arg2']['options'] = options
        metadata['arg2']['selected_option'] = selected_option
    if id == 'arg3':
        metadata['arg3'] = {}
        if metadata.get('arg4') != None:
            metadata['arg4'] = None
        if metadata.get('arg5') != None:
            metadata['arg5'] = None
        metadata['arg3']['options'] = options
        metadata['arg3']['selected_option'] = selected_option
    if id == 'arg4':
        metadata['arg4'] = {}
        if metadata.get('arg5') != None:
            metadata['arg5'] = None
        metadata['arg4']['options'] = options
        metadata['arg4']['selected_option'] = selected_option
    if id == 'arg5':
        metadata['arg5'] = {}
        metadata['arg5'] = {}
        metadata['arg5']['options'] = options
        metadata['arg5']['selected_option'] = selected_option
    return metadata