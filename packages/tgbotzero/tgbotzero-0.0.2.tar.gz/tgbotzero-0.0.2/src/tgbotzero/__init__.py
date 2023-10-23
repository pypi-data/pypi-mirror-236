"""
tgbotzero
========
A zero-boilerplate simple telegram bots.
"""

from .utils.botzero import run_bot, help, Button
from .utils.copy_examples import copy_examples

__all__ = ['help', 'run_bot', 'Button', 'copy_examples']
