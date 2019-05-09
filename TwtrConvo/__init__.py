import os
from . import twtrconvo, tweets, plots

__version__ = '0.1.0'
__license__ = 'MIT'
__author__ = 'Lee Alessandrini'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'twtrconvo',
    'tweets',
    'plots'
]