#!/usr/bin/python

"""A tool for deleting duplicate copies of files.

This tool does a full comparison for all files with matching
filenames. If you are looking for a tool that finds duplicates
irrespective of filename, try fdupes.
"""

import os, sys

blocksize = 16384


class FileRegistry(object):
    """A registry of files, keyed by filename (not full path)."""

    def __init__(self):
        self._files = {}
        self._delete_list = []

    def add(self, filepath):
        """Add a file to the registry."""
        if os.path.isfile(filepath):
            path, filename = os.path.split(filepath)
            self._files.setdefault(filename, []).append(filepath)
            print 'Scan: %s' % os.path.join(filepath)

    def _do_add(self, arg, d, files):
        """A function for os.path.walk for adding files to the registry."""
        for i in files:
            self.add(os.path.join(d, i))

    def add_tree(self, dirpath):
        """Recursively add all files in a tree."""
        os.path.walk(dirpath, self._do_add, None)

    def is_duplicate(self, candidate):
        """Check if a candidate is a duplicate of a file in the registry.

        Only regular files are ever considered duplicates.
        """
        if not os.path.isfile(candidate):
            return False
        path, filename = os.path.split(candidate)
        if not filename in self._files:
            return False
        for keeper in self._files[filename]:
            if keeper == candidate:
                print 'Confused between keep and del paths!'
                continue
            print 'Comparing %s (keeper) and %s:' % (keeper, candidate),
            with open(keeper) as f1:
                with open(candidate) as f2:
                    while True:
                        d1 = f1.read(blocksize)
                        d2 = f2.read(blocksize)
                        if d1 != d2:
                            print 'No match.'
                            break
                        elif d1 == '' and d2 == '':
                            print 'MATCH!'
                            return True

    def _do_get_prune_candidates(self, deletion_candidates, d, files):
        """A function for os.path.walk for collecting files to prune."""
        for i in files:
            candidate = os.path.join(d, i)
            if self.is_duplicate(candidate):
                deletion_candidates.append(candidate)

    def get_prune_candidates(self, dirpath):
        """Find files in a tree that are duplicates of registered files."""
        deletion_candidates = []
        os.path.walk(dirpath, self._do_get_prune_candidates,
                     deletion_candidates)
        return deletion_candidates


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print '''\
    %s <keep_dir> <del_dir>

    %s deletes all files in del_dir that are the same as in keep_dir.
    ''' % ((sys.argv[0],)*2)
        sys.exit(1)

    keep_dir = sys.argv[1]
    del_dir = sys.argv[2]

    keep_reg = FileRegistry()
    keep_reg.add_tree(keep_dir)
    deletion_candidates = keep_reg.get_prune_candidates(del_dir)

    print 'Will now delete:'
    for i in sorted(deletion_candidates):
        print i
    if raw_input('Continue? [y/n]') == 'y':
        for i in deletion_candidates:
            os.unlink(i)
        print 'DELETED.'
