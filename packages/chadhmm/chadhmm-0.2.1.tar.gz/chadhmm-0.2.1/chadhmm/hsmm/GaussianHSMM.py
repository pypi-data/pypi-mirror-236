from typing import Optional, Sequence, Literal

import torch
import numpy as np

from .BaseHSMM import BaseHSMM # type: ignore
from mixtures import GaussianMixtureEmissions # type: ignore
from emission_dists import GaussianEmissions # type: ignore


class GaussianHSMM(BaseHSMM, GaussianEmissions):
    """
    Gaussian Hidden Semi-Markov Model (Gaussian HSMM)
    ----------
    This model assumes that the data follows a multivariate Gaussian distribution. 
    The model parameters (initial state probabilities, transition probabilities, duration probabilities,emission means, and emission covariances) 
    are learned using the Baum-Welch algorithm.

    Parameters:
    ----------
    n_states (int):
        Number of hidden states in the model.
    max_duration (int):
        Maximum duration of the states.
    n_features (int):
        Number of features in the emission data.
    n_components (int):
        Number of components in the Gaussian mixture model.
    params_init (bool):
        Whether to initialize the model parameters prior to fitting.
    alpha (float):
        Dirichlet concentration parameter for the prior over initial state probabilities and transition probabilities.
    covariance_type (COVAR_TYPES):
        Type of covariance parameters to use for the emission distributions.
    min_covar (float):
        Floor value for covariance matrices.
    random_state (Optional[int]):
        Random seed to use for reproducible results.
    verbose (bool):
        Whether to print progress logs during fitting.
    """

    COVAR_TYPES = Literal['spherical', 'tied', 'diag', 'full']

    def __init__(self,
                 n_states: int,
                 n_features: int,
                 max_duration: int,
                 params_init: bool = False,
                 alpha: float = 1.0,
                 covariance_type: COVAR_TYPES = 'full',
                 min_covar: float = 1e-3,
                 context_means: bool = False,
                 context_covars: bool = False,
                 verbose: bool = True,
                 random_state: Optional[int] = None,
                 device: Optional[torch.device] = None):

        self.context_means = context_means
        self.context_covars = context_covars

        BaseHSMM.__init__(self,n_states,max_duration,params_init,alpha,verbose,random_state,device)
        
        GaussianEmissions.__init__(self,n_states,n_features,params_init,covariance_type,
                                   min_covar,random_state,device)
                    
    def __str__(self):
        return f'GaussianHSMM(n_states={self.n_states}, n_durations={self.max_duration},n_features={self.n_features})'

    @property
    def n_fit_params(self):
        """Return the number of trainable model parameters."""
        return {
            'states': self.n_states,
            'transitions': self.n_states**2,
            'durations': self.n_states * self.max_duration,
            'means': self.n_states * self.n_features,
            'covars': {
                'spherical': self.n_states,
                'diag': self.n_states * self.n_features,
                'full': self.n_states * self.n_features * (self.n_features + 1) // 2,
                'tied': self.n_features * (self.n_features + 1) // 2,
            }[self.covariance_type],
        }
    
    @property
    def params(self):
        return {'pi': self.initial_vector.matrix,
                'A': self.transition_matrix.matrix,
                'D': self.duration_matrix.matrix,
                'B':{'means': self.means, 
                        'covars': self.covs}}

    @property
    def dof(self):
        return self.n_states**2 - 1 + self.means.numel() + self.covs.numel() 
    
    def _check_sequence(self, sequence, lengths=None) -> Sequence[torch.Tensor]:
        if isinstance(sequence, torch.Tensor):
            valid_seq = sequence.to(device=self.device)
        elif isinstance(sequence, np.ndarray):
            valid_seq = torch.from_numpy(sequence).to(dtype=torch.int64, device=self.device)
        else:
            raise NotImplementedError(f'Expected torch Tensor or numpy array, got {type(sequence)}')
        
        if valid_seq.ndim != 2:
            raise ValueError(f'Sequence must have shape (T,{self.n_features}). Got {sequence.shape}.')
        elif valid_seq.shape[1] != self.n_features:
            raise ValueError(f'Sequence must have shape (T,{self.n_features}). Got {sequence.shape}.')
        elif lengths is not None and sum(lengths) > valid_seq.size(dim=0):
            raise ValueError(f'Lengths sum ({sum(lengths)}) differ from sequence length ({valid_seq.size(dim=0)})')
       
        if lengths is not None:
            return torch.split(valid_seq, lengths)
        else:
            return [valid_seq]
        
    def _check_theta(self, theta: Optional[torch.Tensor]=None) -> Optional[torch.Tensor]:
        """Check the given contextual variables."""
        if (self.context_covars or self.context_means) and theta is None:
            raise ValueError('Theta must be given when using context means or covars.')
        elif theta is not None and not (self.context_covars or self.context_means):
            raise ValueError('Theta must be None when NOT using context means or covars.')
        else:
            if theta is None:
                return theta
            else:
                return torch.hstack((theta, torch.ones(size=(theta.shape[0],1), 
                                                       dtype=torch.float64, 
                                                       device=self.device)))
    
    def map_emission(self, emission: torch.Tensor) -> torch.Tensor:
        return GaussianEmissions.map_emission(self,emission)

    def sample_B_params(self, seed: Optional[int] = None) -> None:
        self._means,self._covs = GaussianEmissions.sample_emissions_params(self, seed)

    def update_B_params(self, X: Sequence[torch.Tensor]) -> None:
        GaussianEmissions.update_emissions_params(self,X,self._log_gamma.exp())


class GaussianMixtureHSMM(BaseHSMM, GaussianMixtureEmissions):
    """
    Gaussian Hidden Semi-Markov Model (Gaussian HSMM)
    ----------
    This model assumes that the data follow a multivariate Gaussian distribution. 
    The model parameters (initial state probabilities, transition probabilities, duration probabilities,emission means, and emission covariances) 
    are learned using the Baum-Welch algorithm.

    Parameters:
    ----------
    n_states (int):
        Number of hidden states in the model.
    max_duration (int):
        Maximum duration of the states.
    n_features (int):
        Number of features in the emission data.
    n_components (int):
        Number of components in the Gaussian mixture model.
    params_init (bool):
        Whether to initialize the model parameters prior to fitting.
    alpha (float):
        Dirichlet concentration parameter for the prior over initial state probabilities and transition probabilities.
    covariance_type (COVAR_TYPES):
        Type of covariance parameters to use for the emission distributions.
    min_covar (float):
        Floor value for covariance matrices.
    random_state (Optional[int]):
        Random seed to use for reproducible results.
    verbose (bool):
        Whether to print progress logs during fitting.
    """

    COVAR_TYPES = Literal['spherical', 'tied', 'diag', 'full']

    def __init__(self,
                 n_states: int,
                 n_features: int,
                 max_duration: int,
                 n_components: int = 1,
                 params_init: bool = False,
                 alpha: float = 1.0,
                 covariance_type: COVAR_TYPES = 'full',
                 min_covar: float = 1e-3,
                 context_means: bool = False,
                 context_covars: bool = False,
                 verbose: bool = True,
                 random_state: Optional[int] = None,
                 device: Optional[torch.device] = None):

        self.context_means = context_means
        self.context_covars = context_covars

        BaseHSMM.__init__(self,n_states,max_duration,params_init,alpha,verbose,random_state,device)
        
        GaussianMixtureEmissions.__init__(self,n_states,n_components,n_features,params_init,alpha,covariance_type,
                                          min_covar,random_state,device)
                    
    def __str__(self):
        return f'GaussianMixtureHSMM(n_states={self.n_states}, n_durations={self.max_duration},n_features={self.n_features}, n_components={self.n_components})'

    @property
    def n_fit_params(self):
        """Return the number of trainable model parameters."""
        fit_params_dict = {
            'states': self.n_states,
            'transitions': self.n_states**2,
            'durations': self.n_states * self.max_duration,
            'weights': self.n_states * self.n_components,
            'means': self.n_states * self.n_features * self.n_components,
            'covars': {
                'spherical': self.n_states,
                'diag': self.n_states * self.n_features,
                'full': self.n_states * self.n_features * (self.n_features + 1) // 2,
                'tied': self.n_features * (self.n_features + 1) // 2,
            }[self.covariance_type],
        }

        return fit_params_dict
    
    @property
    def params(self):
        param_dict = {'pi': self.initial_vector.matrix,
                    'A': self.transition_matrix.matrix,
                    'D': self.duration_matrix.matrix,
                    'B':{'weights': self.weights.matrix,
                         'means': self.means, 
                         'covars': self.covs}}
        return param_dict

    @property
    def dof(self):
        return self.n_states**2 - 1 + self.n_states*self.n_components - self.n_states + self.means.numel() + self.covs.numel() 
    
    def _check_sequence(self, sequence, lengths=None) -> Sequence[torch.Tensor]:
        if isinstance(sequence, torch.Tensor):
            valid_seq = sequence.to(self.device)
        elif isinstance(sequence, np.ndarray):
            valid_seq = torch.from_numpy(sequence).to(self.device)
        else:
            raise NotImplementedError(f'Expected torch Tensor or numpy array, got {type(sequence)}')
        
        if (n_dim:=valid_seq.ndim) != 2:
            raise ValueError(f'Sequence must be 2-dimensional. Got {n_dim}.')
        elif (F:=valid_seq.shape[1]) != self.n_features:
            raise ValueError(f'Sequence 2nd dim must be {self.n_features}. Got {F}.')
        elif lengths is not None and (n:=sum(lengths)) > (T:=valid_seq.size(dim=0)):
            raise ValueError(f'Lengths sum ({n}) differ from sequence length ({T})')
       
        if lengths is not None:
            return torch.split(valid_seq, lengths)
        else:
            return [valid_seq]
        
    def _check_theta(self, theta: Optional[torch.Tensor]=None) -> Optional[torch.Tensor]:
        """Check the given contextual variables."""
        if (self.context_covars or self.context_means) and theta is None:
            raise ValueError('Theta must be given when using context means or covars.')
        elif theta is not None and not (self.context_covars or self.context_means):
            raise ValueError('Theta must be None when NOT using context means or covars.')
        else:
            if theta is None:
                return theta
            else:
                return torch.hstack((theta, torch.ones(size=(theta.shape[0],1), 
                                                       dtype=torch.float64, 
                                                       device=self.device)))
    
    def map_emission(self, emission: torch.Tensor) -> torch.Tensor:
        return GaussianMixtureEmissions.map_emission(self,emission)

    def sample_B_params(self, seed: Optional[int] = None) -> None:
        self.means = GaussianMixtureEmissions.sample_emissions_params(self, seed)

    def update_B_params(self, X: Sequence[torch.Tensor]) -> None:
        posterior = torch.zeros(size=(self.n_sequences,self.n_states,self.n_components,self.n_samples), 
                                dtype=torch.float64, 
                                device=self.device)
        
        for i, seq in enumerate(X):
            posterior[i] = torch.exp(self._log_gamma[i,:,:seq.size(0)].unsqueeze(dim=-2).expand(self.n_states,self.n_components,-1) + self.compute_responsibilities(seq))

        GaussianMixtureEmissions.update_emissions_params(self,X,posterior)