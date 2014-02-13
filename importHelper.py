

def importFrom(module, name):
    r'''This function imports the specified attribute from the specified file.
    '''
    module = __import__(module, fromlist=[name])
    return getattr(module, name)
