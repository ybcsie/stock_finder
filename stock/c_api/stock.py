# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_stock')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_stock')
    _stock = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_stock', [dirname(__file__)])
        except ImportError:
            import _stock
            return _stock
        try:
            _mod = imp.load_module('_stock', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _stock = swig_import_helper()
    del swig_import_helper
else:
    import _stock
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

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


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
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

def set_days_range(value):
    return _stock.set_days_range(value)
set_days_range = _stock.set_days_range

def set_delta_percentage_min(value):
    return _stock.set_delta_percentage_min(value)
set_delta_percentage_min = _stock.set_delta_percentage_min

def set_price_limit(value):
    return _stock.set_price_limit(value)
set_price_limit = _stock.set_price_limit

def work(work_arr_ptr, work_type):
    return _stock.work(work_arr_ptr, work_type)
work = _stock.work

def calc_days_e(work_arr_ptr, days, mppt, buy_rule_no, RoI_rule_no):
    return _stock.calc_days_e(work_arr_ptr, days, mppt, buy_rule_no, RoI_rule_no)
calc_days_e = _stock.calc_days_e

def calc_day_e(work_arr_ptr, date, mppt, buy_rule_no, RoI_rule_no):
    return _stock.calc_day_e(work_arr_ptr, date, mppt, buy_rule_no, RoI_rule_no)
calc_day_e = _stock.calc_day_e

def calc_month_e(work_arr_ptr, yyyymm, mppt, buy_rule_no, RoI_rule_no):
    return _stock.calc_month_e(work_arr_ptr, yyyymm, mppt, buy_rule_no, RoI_rule_no)
calc_month_e = _stock.calc_month_e
# This file is compatible with both classic and new-style classes.

cvar = _stock.cvar
WORK_TYPE_NEWHIGH = cvar.WORK_TYPE_NEWHIGH
WORK_TYPE_ATTACK = cvar.WORK_TYPE_ATTACK

