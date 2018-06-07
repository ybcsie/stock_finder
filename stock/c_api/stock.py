# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_stock', [dirname(__file__)])
        except ImportError:
            import _stock
            return _stock
        if fp is not None:
            try:
                _mod = imp.load_module('_stock', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _stock = swig_import_helper()
    del swig_import_helper
else:
    import _stock
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



def new_stock_data_arr_ptr(size):
    return _stock.new_stock_data_arr_ptr(size)
new_stock_data_arr_ptr = _stock.new_stock_data_arr_ptr

def del_stock_data_arr(stock_data_arr_ptr):
    return _stock.del_stock_data_arr(stock_data_arr_ptr)
del_stock_data_arr = _stock.del_stock_data_arr

def new_stock_data_ptr(stock_id, ipo_date, trade_day_info_size):
    return _stock.new_stock_data_ptr(stock_id, ipo_date, trade_day_info_size)
new_stock_data_ptr = _stock.new_stock_data_ptr

def get_stock_id(stock_data_ptr):
    return _stock.get_stock_id(stock_data_ptr)
get_stock_id = _stock.get_stock_id

def add_stock_data(work_arr_ptr, stock_data_ptr):
    return _stock.add_stock_data(work_arr_ptr, stock_data_ptr)
add_stock_data = _stock.add_stock_data

def add_trade_day_info(stock_data_ptr, date, vol, first, highest, lowest, last, delta):
    return _stock.add_trade_day_info(stock_data_ptr, date, vol, first, highest, lowest, last, delta)
add_trade_day_info = _stock.add_trade_day_info

def work(work_arr_ptr, work_type, days_range, delta_percentage_min):
    return _stock.work(work_arr_ptr, work_type, days_range, delta_percentage_min)
work = _stock.work
# This file is compatible with both classic and new-style classes.

cvar = _stock.cvar
WORK_TYPE_NEWHIGH = cvar.WORK_TYPE_NEWHIGH
WORK_TYPE_ATTACK = cvar.WORK_TYPE_ATTACK

