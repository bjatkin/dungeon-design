import numpy as np

class GNode(object):
    def __init__(self, parent_s, child_s, name):
        self.child_s = child_s
        self.parent_s = parent_s
        self.name = name

    @staticmethod
    def add(list_, items):
        if not isinstance(items, list): # Gracefully handle the input whether its a list or not
            items = [items]
        list_.extend(items) # Modify list_ in place so we don't have to return a value

    @staticmethod
    def remove(list_, item_names):
        if not isinstance(item_names, list):
            item_names = [item_names]
        list_[:] = filter(lambda x: x.name not in item_names, list_) # Modify list_ in place so we don't have to return a value
    
    def add_child_s(self, child_s):
        # Instead of having the code to add a child/parent/key here, we call a static method
        # passing it the list that we want to modify.
        GNode.add(self.child_s, child_s) 
    
    def remove_child_s(self, child_name_s):
        GNode.remove(self.child_s, child_name_s)
    
    def add_parent_s(self, parent_s):
        GNode.add(self.parent_s, parent_s)
    
    def remove_parent_s(self, parent_name_s):
        GNode.remove(self.parent_s, parent_name_s)

    def __repr__(self):
        parent_names = [n.name for n in self.parent_s]
        child_names = [n.name for n in self.child_s]
        class_name = type(self).__name__
        string = "{}(\'{}\', parents={}, children={})".format(class_name, self.name, parent_names, child_names)
        return string


class Start(GNode):
    def __init__(self, child_s=[]):
        super(Start, self).__init__([], child_s, "Start")

class Key(GNode):
    def __init__(self, lock_s=[], parent_s=[], child_s=[], name=""):
        super(Key, self).__init__(parent_s, child_s, name)
        self.lock_s = lock_s
    
    def add_lock_s(self, lock_s):
        GNode.add(self.lock_s, lock_s)
    
    def remove_lock_s(self, lock_name_s):
        GNode.remove(self.lock_s, lock_name_s)
        

class Lock(GNode):
    def __init__(self, key_s=[], parent_s=[], child_s=[], name=""):
        super(Lock, self).__init__(parent_s, child_s, name)
        self.key_s = key_s
    
    def add_key_s(self, key_s):
        GNode.add(self.key_s, key_s)
    
    def remove_key_s(self, key_s):
        GNode.remove(self.key_s, key_s)


class End(GNode):
    def __init__(self, parent_s=[]):
        super(End, self).__init__(parent_s, [], "End")