#!/usr/bin/env python
# -*- coding: utf-8 -*-

# klctags.py wrapper, for avoiding FabricEngine`s stdout log like,
#  [FABRIC:MT] Fabric Engine version 2.1.0-auto-2016030820
#  ...snip...
#  [FABRIC:MT] IRCache: Not pruning since last prune was less than 24 hours ago
# and outputing to stdout only tags.

import os
import sys
import subprocess


d = os.path.dirname(__file__)
k = os.path.join(d, "KLTags.py")
i = sys.argv[1:]
cmd = "python {} {}".format(k, " ".join(i))

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_data, stderr_data = p.communicate()
print stdout_data
# print p.returncode, stdout_data, stderr_data
