import os, sys
JCMROOT = os.environ['JCMROOT']
module_path = f'{JCMROOT}/ThirdPartySupport/Python'
sys.path.append(module_path)
# do not import * due to syntax error in jcmwave/__init__.py line 51

from jcmwave import (
    startup, set_num_threads, info, jcmt2jcm, nested_dict, 
    geo, solve, view, edit, loadtable, loadcartesianfields,
    Resultbag, daemon, call_templates, convert2powerflux, optimizer
    )

__all__ = ['startup', 'set_num_threads', 'info',
           'jcmt2jcm', 'nested_dict', 
           'geo', 'solve', 'view', 'edit', 
           'loadtable', 'loadcartesianfields',
           'Resultbag', 'daemon', 'call_templates',
           'convert2powerflux', 'optimizer'] 