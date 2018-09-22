# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Tests for the documentation.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import os.path
import unittest
import doctest

import manuel.capture
import manuel.codeblock
import manuel.doctest
import manuel.ignore
import manuel.testing

from zope.testing import renormalizing

checker = renormalizing.RENormalizing([
    # Python 3 unicode removed the "u".
    (re.compile("u('.*?')"), r"\1"),
    (re.compile('u(".*?")'), r"\1"),
    # Python 3 bytes added the "b".
    (re.compile("b('.*?')"), r"\1"),
    (re.compile('b(".*?")'), r"\1"),
])


def test_suite():
    here = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(here, 'setup.py')):
        prev, here = here, os.path.dirname(here)
        if here == prev:
            # Let's avoid infinite loops at root
            raise AssertionError('could not find my setup.py')

    docs = os.path.join(here, 'docs')
    api_docs = os.path.join(docs, 'api')

    doc_files_to_test = (
        'narr.rst',
    )

    api_files_to_test = (
        'config.rst',
        'docutils.rst',
        'fields.rst',
        'xmlconfig.rst',
    )

    paths = [os.path.join(docs, f) for f in doc_files_to_test]
    paths += [os.path.join(api_docs, f) for f in api_files_to_test]

    m = manuel.ignore.Manuel()
    m += manuel.doctest.Manuel(checker=checker, optionflags=(
        doctest.NORMALIZE_WHITESPACE
        | doctest.ELLIPSIS
        | doctest.IGNORE_EXCEPTION_DETAIL
    ))
    m += manuel.codeblock.Manuel()
    m += manuel.capture.Manuel()

    suite = unittest.TestSuite()
    suite.addTest(
        manuel.testing.TestSuite(
            m,
            *paths
        )
    )

    return suite
