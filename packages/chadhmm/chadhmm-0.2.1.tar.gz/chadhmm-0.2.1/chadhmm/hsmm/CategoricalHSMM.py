from typing import Optional, Sequence

import torch
import numpy as np

from .BaseHSMM import BaseHSMM # type: ignore
from emission_dists import CategoricalEmissions # type: ignore


class CategoricalHSMM(BaseHSMM, CategoricalEmissions):
    """
    Categorical Hidden semi-Markov Model (HSMM)
    ----------
    Hidden semi-Markov model with categorical (discrete) emissions. This model is an extension of classical HMMs where the duration of each state is modeled by a geometric distribution.
    Duration in each state is modeled by a Categorical distribution with a fixed maximum duration.

    Parameters:
    ----------
    n_states (int):
        Number of hidden states in the model.
    n_emissions (int): 
        Number of emissions in the model.
    random_state (int):
        Random seed for reproducibility.
    params_init (bool):
        Whether to initialize the model parameters prior to fitting.
    init_dist (SAMPLING_DISTRIBUTIONS):
        Distribution to use for initializing the model parameters.
    alpha (float):
        Dirichlet concentration parameter for the prior over initial state probabilities and transition probabilities.
    verbose (bool):
        Whether to print progress logs during fitting.
    """
    def __init__(self,
                 n_states: int,
                 n_emissions: int,
                 max_duration: int,
                 alpha: float = 1.0,
                 params_init: bool = False,
                 verbose: bool = True,
                 random_state: Optional[int] = None, 
                 device: Optional[torch.device] = None):
        
        BaseHSMM.__init__(self,n_states,max_duration,params_init,alpha,verbose,random_state,device)
        
        CategoricalEmissions.__init__(self,n_states,n_emissions,params_init,alpha,random_state,device)

    def __str__(self):
        return f'CategoricalHSMM(n_states={self.n_states}, max_duration{self.max_duration}, n_emissions={self.n_emissions})'

    @property
    def params(self) -> dict:
        """Returns the parameters of the model."""
        return {
            'pi': self.initial_vector.matrix,
            'A': self.transition_matrix.matrix,
            'D': self.duration_matrix.matrix,
            'B': self.emission_matrix.matrix
        }

    @property    
    def n_fit_params(self) -> dict:
        """Return the number of trainable model parameters."""
        return {
            'states': self.n_states,
            'transitions': self.n_states**2,
            'durations': self.n_states * self.max_duration,
            'emissions': self.n_states * self.n_emissions
        }
    
    @property
    def dof(self) -> int:
        """Returns the degrees of freedom of the model."""
        return self.n_states ** 2 + self.n_states * self.n_emissions - 1
    
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

