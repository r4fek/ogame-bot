# -*- coding: utf-8 -*-

# HELPER FUNCTIONS 
def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(self):
        if not self.logged_in:
            self.login()
        return fn(self)
    return wrapper

def load_sms_gateway(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod