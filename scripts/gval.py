#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# remove o dir. do script do sys.path para não haver problemas de importação
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

import gval.script

if __name__ == '__main__':
    script = gval.script.Script()
    script.executar(*sys.argv)
