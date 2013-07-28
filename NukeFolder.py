
import os


def NukeFolder(path, includeRoot = True):
    '''Use this function with *EXTREME* caution.
    This function deletes all contents of the folder specified by path.  If
    the specified folder should also be deleted, includeRoot should be set to
    True (the default).
    If the folder does not exist, False will be returned.  Otherwise, True
    will be returned.'''

    # If the specified path is not a directory, return immediately.
    if (not os.path.isdir(path)):
        return False

    # Delete everything reachable from the directory named in 'top',
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    for root, dirs, files in os.walk(path, topdown=False):

        # Delete the files.
        for name in files:
            curFile = os.path.join(root, name)
            NukeFile(curFile)

        # Delete the subdirectories.
        for name in dirs:
            curDir = os.path.join(root, name)
            os.rmdir(curDir)

    # If the caller wants to remove the specified folder as well, do it now.
    if (includeRoot):
        os.rmdir(path)

    return True


def NukeFile(fileName):
    r'''Deletes the specified file.  Will remove the read-only
    attribute if necessary.  Returns True if successful, False
    otherwise.'''

    try:
        os.remove(fileName) # Try to delete it.  Most times this will work.
    except:
        # Probably failed because it is not a normal file (it is
        # probably read-only).
        # win32api.SetFileAttributes(fileName, win32con.FILE_ATTRIBUTE_NORMAL)
        # os.remove(fileName) # Try to delete it again
        pass

    return not os.path.isfile(fileName)
