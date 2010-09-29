#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Sep 29, 2010

@author: vak
'''
from sys import stdin, stdout, stderr
import unittest
import sys


def _line_emitter(input):
    line_to_emit = ''
    
    for line in input:        
        if line.endswith('\\'):
            line_to_emit += line[:-1]
            #print >>stderr, "line_to_emit=<%s>" % line_to_emit 
        else:
            line_to_emit += line
            yield line_to_emit
            line_to_emit = ''

import re
_pat_colon = re.compile(':')
def _dependency_emitter(lines):
    for line in lines:
        if len(line) == 0 or line[0] in ['\t', '#'] or line.find('=') > 0 or line.find('?') > 0:
            continue
            
        parts = _pat_colon.split(line)
        if len(parts) == 1:
            continue
        elif len(parts) == 2:
            if len(parts[1]) == 0 or parts[1][0] != '=':
                yield tuple(parts)
        else:
            print >> stderr, 'more then one ":" not yet implemented ;)\n got the following:\n%s' % parts



_pat_whitespacing = re.compile('[ \t]+')
def _single_dot_dep_emitter(out_deps_pairs):
    for outs_str, deps_str in out_deps_pairs:
        for out in _pat_whitespacing.split(outs_str.strip()):            
            yield '\t"%s"\n' % out
            deps = _pat_whitespacing.split(deps_str.strip())
            for dep in deps:
                if dep:
                    if dep[0] == '#':
                        break
                    yield '\t"%s" -> "%s"\n' % (dep, out)
                
                

def makefile2dot():
    '''
    Visalizer of Makefiles. 
    Don't even think we use a grammar parser. 
    '''
    stdout.write('digraph G {\n\trankdir="BT"\n')
    for line in _single_dot_dep_emitter(_dependency_emitter(_line_emitter(''.join(stdin).split('\n')))):
        stdout.write(line)
    stdout.write('}\n')



class Test(unittest.TestCase):

    def test_emitters(self):
        self.assertEqual(list(_line_emitter([''])), [''])
        self.assertEqual(list(_line_emitter(['', ''])), ['', ''])
        self.assertEqual(list(_line_emitter(['a', 'b'])), ['a', 'b'])
        self.assertEqual(list(_line_emitter(['a\\', 'b', 'c'])), ['ab', 'c'])

        self.assertEqual(list(_dependency_emitter(_line_emitter(['']))), [])
        self.assertEqual(list(_dependency_emitter(_line_emitter(['macro', 'out:dep1\\', ' dep2', '\tcommand']))), [('out', 'dep1 dep2')])
        self.assertEqual(list(_dependency_emitter(_line_emitter(['macro', 'out:dep1\\', ' dep2', '\tcommand', 'out2:dep3\\', ' dep4', '\tcommand2']))),
                         [('out', 'dep1 dep2'), ('out2', 'dep3 dep4')])
        self.assertEqual(list(_dependency_emitter(_line_emitter(['default:', '', '']))), [('default','')])

        inp = ['macro', 'out:dep1\\', ' dep2', '\tcommand', '', 'out2:dep3\\', ' dep4', '\tcommand2']
        self.assertEqual(list(_single_dot_dep_emitter(_dependency_emitter(_line_emitter(inp)))),
                         ['\t"out"\n', '\t"dep1" -> "out"\n', '\t"dep2" -> "out"\n', '\t"out2"\n', '\t"dep3" -> "out2"\n', '\t"dep4" -> "out2"\n'])

        inp = ['default:', '\techo']
        self.assertEqual(list(_single_dot_dep_emitter(_dependency_emitter(_line_emitter(inp)))),
                         ['\t"default"\n'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
    if len(sys.argv) > 1:
        print >> stderr, 'Usage:\n\tmakefile2dot <Makefile >out.dot\nor\n\tmakefile2dot <Makefile |dot -Tpng > out.png'
    else:
        makefile2dot()
    
