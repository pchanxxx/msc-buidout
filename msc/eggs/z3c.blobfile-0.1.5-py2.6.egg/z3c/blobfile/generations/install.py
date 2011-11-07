
from z3c.blobfile.generations import package_name


def evolve(context):
    """run all evolutions beginning with generation 1"""

    print "SchemaManager(%s): install" % package_name
    generation = 1
    while True:
        name = "%s.evolve%d" % (package_name, generation)
        try:
            evolver = __import__(name, {}, {}, ['*'])
        except ImportError:
            break
        else:
            print "SchemaManager(%s): evolve%s" % (package_name, generation)
            evolver.evolve(context)
            generation += 1
