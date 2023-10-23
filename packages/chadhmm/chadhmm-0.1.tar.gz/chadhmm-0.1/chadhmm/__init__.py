"""
ChadHMM
======

Ultra Chad Implementation of Hidden Markov Models in Pytorch (available only to true sigma males)

But seriously this package needs you to help me make it better. I'm not a professional programmer, I'm just a guy who likes to code. 
If you have any suggestions, please let me know. I'm open to all ideas.
"""

# Set version
__version__ = '0.0.1'
__author__ = 'GarroshIcecream'
__license__ = 'MIT'

# Import HMM objects
from .hmm.CategoricalHMM import CategoricalHMM
from .hmm.GaussianHMM import GaussianHMM, GaussianMixtureHMM
from .hsmm.CategoricalHSMM import CategoricalHSMM
from .hsmm.GaussianHSMM import GaussianHSMM, GaussianMixtureHSMM