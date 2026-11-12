"""Standalone native regression for the shared hole-free corner bracket.

The standalone model imports and runs the exact same CornerBracket class used
by assemblies. There is no wrapper class and no alternate geometry path.
"""
from components.corner_bracket import CornerBracket


CornerBracket()
