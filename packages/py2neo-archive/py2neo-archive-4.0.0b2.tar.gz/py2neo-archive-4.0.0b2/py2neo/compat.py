#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2017, Nigel Small
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


try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from io import StringIO
import os
from sys import version_info


if version_info >= (3,):
    ReprIO = StringIO

    integer = int
    number = (int, float)
    string = (bytes, str)
    unicode = str
    unichr = chr

    unicode_repr = str

    def bstr(s, encoding="utf-8"):
        if isinstance(s, bytes):
            return s
        elif isinstance(s, bytearray):
            return bytes(s)
        elif isinstance(s, str):
            return bytes(s, encoding)
        else:
            return bytes(str(s), encoding)

    def ustr(s, encoding="utf-8"):
        """ Convert argument to unicode string.
        """
        if isinstance(s, str):
            return s
        try:
            return s.decode(encoding)
        except AttributeError:
            return str(s)

    def xstr(s, encoding="utf-8"):
        """ Convert argument to string type returned by __str__.
        """
        if isinstance(s, str):
            return s
        elif isinstance(s, bytes):
            return s.decode(encoding)
        else:
            return str(s)

    class PropertiesParser(SafeConfigParser):

        def read_properties(self, filename, section=None):
            if not section:
                basename = os.path.basename(filename)
                if basename.endswith(".properties"):
                    section = basename[:-11]
                else:
                    section = basename
            with open(filename) as f:
                data = f.read()
            self.read_string("[%s]\n%s" % (section, data), filename)

else:
    import codecs

    integer = (int, long)
    number = (int, long, float)
    string = (str, unicode)
    unicode = unicode
    unichr = unichr

    def unicode_repr(s):
        return s.encode("utf-8")

    class ReprIO(StringIO):

        def getvalue(self, *args, **kwargs):
            return StringIO.getvalue(self, *args, **kwargs).encode("utf-8")

    def bstr(s, encoding="utf-8"):
        if isinstance(s, bytes):
            return s
        elif isinstance(s, bytearray):
            return bytes(s)
        elif isinstance(s, unicode):
            return s.encode(encoding)
        else:
            return str(s)

    def ustr(s, encoding="utf-8"):
        """ Convert argument to unicode string.
        """
        if isinstance(s, unicode):
            return s
        else:
            try:
                return unicode(s)
            except UnicodeDecodeError:
                return str(s).decode(encoding)

    def xstr(s, encoding="utf-8"):
        """ Convert argument to string type returned by __str__.
        """
        if isinstance(s, str):
            return s
        else:
            return unicode(s).encode(encoding)

    class PropertiesParser(SafeConfigParser):

        def read_properties(self, filename, section=None):
            if not section:
                basename = os.path.basename(filename)
                if basename.endswith(".properties"):
                    section = basename[:-11]
                else:
                    section = basename
            data = StringIO()
            data.write("[%s]\n" % section)
            with codecs.open(filename, encoding="utf-8") as f:
                data.write(f.read())
            data.seek(0, os.SEEK_SET)
            self.readfp(data)
