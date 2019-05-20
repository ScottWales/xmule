#!/usr/bin/env python
# Copyright 2019 ARC Centre of Excellence for Climate Extremes
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xarray.backends.common import AbstractDataStore
from mule import load_umfile
import pandas
import hashlib


def field_id(group):
    return hashlib.md5(repr(group).encode('utf-8')).hexdigest()


class XMuleVariable():
    def __init__(self, path, fields):
        pass


class XMuleDataStore(AbstractDataStore):
    def __init__(self, filepath, stashmaster=None):
        """
        Args:
            filepath: Path to the input file
            stashmaster: Mule STASHMaster object
        """
        self._path = filepath
        self._umfile = load_umfile(filepath, stashmaster)

        self._field_df = pandas.DataFrame.from_records([{k: f._values[i]
                            for k, i in f.HEADER_MAPPING}
                            for f in self._umfile.fields])


    def group_fields(self):
        """
        Group the fields within this file into variables
        """
        # Fields constant within a single field
        group_fields = ['lbtim','lbcode','lbhem',
                        'lbrow','lbnpt','lbfc',
                        'lbproc','lbvc','lbexp','lbrsvd4',
                        'lbuser4',
                        'bdatum','bplat','bplon',
                        'bgor','bzy','bdy','bzx','bdx',
                        'bmdi']

        groups = self._field_df.groupby(group_fields)

        return groups


    def get_variables(self):
        """
        Return a dict with all variables in the file
        """

        return {field_id(k): XMuleVariable(self._path, v)
                for k, v in self.group_fields()}
