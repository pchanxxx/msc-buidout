
from zope.app.generations.generations import SchemaManager


package_name = 'z3c.blobfile.generations'

BlobFileSchemaManager = SchemaManager(
     minimum_generation=1,
     generation=2,
     package_name=package_name)
