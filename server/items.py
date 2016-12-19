import json


class Item(object):
    def __init__(self, name, **kwargs):
        self._param_list = ['name']
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)
            self._param_list.append(key)

    def serialize(self):
        params = {}
        for key in self._param_list:
            params[key] = getattr(self, key)
        return params

    def contains(self, **kwargs):
        params_left = len(kwargs.keys())
        if params_left > 0:
            for key, value in kwargs.items():
                if getattr(self, key, None) == value:
                    params_left -= 1
            return not bool(params_left)
        return True


class ItemStore(object):
    # _item = [] is replaced by def __init__ to support db init @Janos
    #_items = []
    def __init__(self):
        self._items = []

    def _exists(self, name, ret_item=False):
        for index, item in enumerate(self._items):
            if item.name == name:
                if ret_item:
                    return True, item
                return True, index
        return False, -1

    def _filter(self, **kwargs):
        filtered = []
        for item in self._items:
            if item.contains(**kwargs):
                filtered.append(item)
        return filtered

    def list_items(self, **kwargs):
        return self._filter(**kwargs)

    def add_item(self, **kwargs):
        name = kwargs.pop('name', None)
        if not name:
            return False, {'error': 'Name required!'}
        exists, index = self._exists(name)
        if exists:
            return False, {'error': 'Duplicate name: {}'.format(name)}
        item = Item(name, **kwargs)
        self._items.append(item)
        return True, item.serialize()

    def del_item(self, name):
        exists, index = self._exists(name)
        if not exists:
            return False, {'error': 'Item not found: {}'.format(name)}
        self._items.pop(index)
        return True, {}

    def get_item(self, name):
        exists, item = self._exists(name, ret_item=True)
        if not exists:
            return False, {'error': 'Item not found: {}'.format(name)}
        return True, item.serialize()


def create_store():
    print 'Initializing...'
    store = ItemStore()
    for i in xrange(5):
        print store.add_item(name='item_{}'.format(i))
    return store

# Added to support db init @Janos
def initialize_store(store, **kwargs):
    init = kwargs.pop('init', None)
    if not init:
        return False, {'init': 'error'}
    if init == 'server':
        store.__init__()
        for i in xrange(5):
            # print store.add_item(name='item_{}'.format(i))
            store.add_item(name='item_{}'.format(i))
        return True, {'init': 'server'}
    return False, {'init': 'unknown request'}
