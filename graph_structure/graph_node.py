class GNode(object):
    def __init__(self, parent_s, child_s, name):
        self.child_s = child_s
        self.parent_s = parent_s
        self.name = name
    
    def add_child_s(self, child_s):
        for child in child_s:
            self.child_s.append(child)
    
    def remove_child_s(self, child_name_s):
        new_child_s = []
        for child in self.child_s:
            if child.name in child_name_s:
                pass
            new_child_s.append(child)
        self.child_s = new_child_s
    
    def add_parent_s(self, parent_s):
        for parent in parent_s:
            self.parent_s.append(parent)
    
    def remove_parent_s(self, parent_name_s):
        new_parent_s = []
        for child in self.parent_s:
            if parent.name in parent_name_s:
                pass
            new_parent_s.append(parent)
        self.parent_s = new_parent_s

class Start(GNode):
    def __init__(self, child_s=[]):
        super(Start, self).__init__([], child_s, "Start")

class Key(GNode):
    def __init__(self, lock_s=[], parent_s=[], child_s=[], name=""):
        super(Key, self).__init__(parent_s, child_s, name)
        self.lock_s = lock_s
    
    def add_lock_s(self, lock_s):
        for lock in lock_s:
            self.lock_s.append(lock)
    
    def remove_lock_s(self, lock_name_s):
        new_lock_s = []
        for lock in self.lock_s:
            if lock.name in lock_name_s:
                pass
            new_lock_s.append(lock)
        self.lock_s = new_lock_s

class Lock(GNode):
    def __init__(self, key_s=[], parent_s=[], child_s=[], name=""):
        super(Lock, self).__init__(parent_s, child_s, name)
        self.key_s = key_s
    
    def add_key_s(self, key_s):
        for key in key_s:
            self.key_s.append(key)
    
    def remove_key_s(self, key_s):
        new_key_s = []
        for key in self.key_s:
            if key.name in key_s:
                pass
            new_key_s.append(key)
        self.key_s = new_key_s


class End(GNode):
    def __init__(self, parent_s=[]):
        super(End, self).__init__(parent_s, [], "End")