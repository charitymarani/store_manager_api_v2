def list_iterator(list_):
    for listitem in list_:
        if listitem is None or not listitem:
            return False
def check_is_int(list_):
    for listitem in list_:
        if not isinstance(listitem,int):
            return False


