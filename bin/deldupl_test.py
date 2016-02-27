#!/usr/bin/python

from pyfakefs import fake_filesystem
import unittest

import deldupl


class TestFileRegistry(unittest.TestCase):

    def setUp(self):
        self._filesystem = fake_filesystem.FakeFilesystem()
        os_module = fake_filesystem.FakeOsModule(self._filesystem)

        self._orig_os = deldupl.os
        self._orig_open = __builtins__.open
        deldupl.os = os_module
        __builtins__.open = fake_filesystem.FakeFileOpen(self._filesystem)

    def tearDown(self):
        __builtins__.open = self._orig_open
        deldupl.os = self._orig_os

    def test_registry(self):
        fn1 = '/tree1/silly/file1'
        fn2 = '/tree1/silly/file2'
        fnA = '/tree2/foo/file1'
        fnB = '/tree2/bar/file2'
        f1 = self._filesystem.CreateFile(fn1, contents='FooContents')
        f2 = self._filesystem.CreateFile(fn2, contents='FooContents')
        fA = self._filesystem.CreateFile(fnA, contents='BarContents')
        fB = self._filesystem.CreateFile(fnB, contents='FooContents')

        reg = deldupl.FileRegistry()
        reg.add_tree('/tree1')
        prunelist = reg.get_prune_candidates('/tree2')
        self.assertEqual([fnB], prunelist)


if __name__ == '__main__':
    unittest.main()
