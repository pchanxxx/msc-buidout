import logging
import transaction

import zope.interface
import zope.component

from zope.app.generations.utility import findObjectsProviding
from zope.app.zopeappgenerations import getRootFolder

from zope.app.file.interfaces import IFile
import zope.app.file
from ZODB.blob import Blob
import z3c.blobfile.file
import z3c.blobfile.image


def replace(file, klass):
    """Replaces a file with it's blob counterpart."""
    blobfile = klass(file._data)
    blobfile.contentType = file.contentType
    container = file.__parent__
    name = file.__name__
    
    if hasattr(file, '__annotations__'):
        blobfile.__annotations__ = file.__annotations__
        
    del container[name]
    container[name] = blobfile
    
    zope.event.notify(
        z3c.blobfile.file.FileReplacedEvent(file, blobfile))
    
def evolveZopeAppFile(root):
    """Evolves all files in the containment hierarchy."""
    for file in findObjectsProviding(root, IFile):
        if isinstance(file, zope.app.file.Image):
            replace(file, z3c.blobfile.image.Image)
        elif isinstance(file, zope.app.file.File):
            replace(file, z3c.blobfile.file.File)
            
        else:
            logging.getLogger('z3c.blobfile.generations').warn(
            'Unknown zope.app.file.interfaces.IFile implementation %s.%s' % (
                file.__class__.__module__,
                file.__class__.__name__))
        file._p_changed = 1 # trigger persistence  
        transaction.savepoint(optimistic=True)
        
def evolve(context):
    """Replaces all zope.app.file objects with z3c.blobfile counterparts."""
    root = getRootFolder(context)
    evolveZopeAppFile(root)
