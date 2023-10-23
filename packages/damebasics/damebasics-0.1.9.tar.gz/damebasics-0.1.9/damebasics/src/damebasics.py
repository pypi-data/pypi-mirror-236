#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damebasics; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import csv
import unittest
import collections
collections.Callable = collections.abc.Callable


class DameBasics(object):

    # FILES
    def eq_columns_in_csv(self, path):
        with open(path, 'r') as csvfile:
            first_line = csvfile.readline()
            ncol = first_line.count(',') + 1
            eqcol = True
            sreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in sreader:
                newcol = len(row)
                if (newcol == ncol):
                    eqcol = eqcol and True
                else:
                    eqcol = False
        return eqcol

    
    def elimDobles(self, l):
        if (len(l) == 0):
            return l
        else:
            rest = []
            for i in l:
                if (i != l[0]):
                    rest = rest + [i]
        return [l[0]] + self.elimDobles(rest)
