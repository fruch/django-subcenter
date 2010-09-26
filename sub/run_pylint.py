import sys
import pylint.lint
args = ['../sub', '--rcfile=pylint_rc']

pylint.lint.Run(args, exit=False)
