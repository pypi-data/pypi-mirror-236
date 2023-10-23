from typing import Optional, Sequence

import torch
import numpy as np

from .BaseHMM import BaseHMM # type: ignore
from emission_dists import CategoricalEmissions # type: ignore

class CategoricalHMM(BaseHMM, CategoricalEmissions):
    """
    Categorical Hidden Markov Model (HMM)
    ----------
    Hidden Markov model with categorical (discrete) emissions. This model is a special case of the HSMM model with a geometric duration distribution.

    Parameters:
    ----------
    n_states (int):
        Number of hidden states in the model.
    n_emissions (int): 
        Number of emissions in the model.
    random_state (int):
        Random seed for reproducibility.
    params_init (bool):
        Whether to initialize the model parameters.
    alpha (float):
        Dirichlet concentration parameter for the prior over initial distribution, transition amd emission probabilities.
    verbose (bool):
        Whether to print progress logs during fitting.
    device (torch.device):
        Device on which to fit the model.
    """

    def __init__(self,
                 n_states: int,
                 n_emissions: int,
                 alpha: float = 1.0,
                 params_init: bool = False,
                 verbose: bool = True,
                 random_state: Optional[int] = None, 
                 device: Optional[torch.device] = None):
        
        BaseHMM.__init__(self,n_states,params_init,alpha,verbose,random_state,device)
        
        CategoricalEmissions.__init__(self, n_states, n_emissions,params_init,alpha,random_state,device)
        
    def __str__(self):
        return f'CategoricalHMM(n_states={self.n_states}, n_emissions={self.n_emissions})'

    @property
    def params(self):
        return {
            'pi': self.initial_vector.matrix,
            'A': self.transition_matrix.matrix,
            'B': self.emission_matrix.matrix
        }

    @property    
    def n_fit_params(self):
        return {
            'initial_states': self.n_states,
            'transitions': self.n_states**2,
            'emissions': self.n_states * self.n_emissions
        }

    @property
    def dof(self):
        return self.n_states ** 2 + self.n_states * self.n_emissions - self.n_states - 1
    
    def _check_theta(self, theta):
        return None

    def _check_sequence(self, sequence, lengths):
        if isinstance(sequence, torch.Tensor):
            assert not sequence.is_floating_point(), 'Tensor must have integer dtype'
            valid_seq = sequence.to(self.device)
        elif isinstance(sequence, np.ndarray):
            assert sequence.dtype == np.integer, 'Array must have integer dtype'
            valid_seq = torch.from_numpy(sequence).to(self.device)
        else:
            raise NotImplementedError(f'Expected torch Tensor or numpy array, got {type(sequence)}')

        if (n_dim:=valid_seq.ndim) != 1:
            raise ValueError(f'Sequence must be 1-dimensional, got shape {n_dim}')
        elif torch.max(valid_seq).item() > (self.n_emissions - 1):
            raise ValueError('Invalid emission in sequence')
        elif lengths is not None and (n:=sum(lengths)) > (T:=valid_seq.numel()):
            raise ValueError(f'Lengths sum ({n}) differ from sequence length ({T})')
        
        if lengths is not None:
            return torch.split(valid_seq, lengths)
        else:
            return [valid_seq]

    def map_emission(self, emission: torch.Tensor) -> torch.Tensor:
        return CategoricalEmissions.map_emission(self,emission)

    def sample_B_params(self, alpha: float, seed: Optional[int] = None) -> None:
        self._emission_matrix = CategoricalEmissions.sample_emissions_params(self, alpha, seed)

    def update_B_params(self, X: Sequence[torch.Tensor]) -> None:
        CategoricalEmissions.update_emissions_params(self,X,self._log_gamma.exp())

