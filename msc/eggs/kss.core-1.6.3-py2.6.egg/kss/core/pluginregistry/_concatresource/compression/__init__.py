'''\
Preprocess resource files by applying compression on them
'''

__all__ = ('compress', )

from javascript import compress as compress_javascript

def compress(data, content_type, compress_level):
    'Returns compressed text for a given content type'
    js = ['application/javascript', 'application/x-javascript']
    assert content_type in js, 'Unsupported content type %s.' % content_type
    return compress_javascript(data, compress_level)
