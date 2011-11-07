list = []
for p, v in context.metatag_properties.propertyItems():
    if v:
        list.append((p, v))
return tuple(list)