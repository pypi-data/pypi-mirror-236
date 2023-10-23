from typing import Optional, Sequence, Tuple, Dict, List, Union
from abc import ABC, abstractmethod, abstractproperty

import torch
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

from stochastic_matrix import TransitionMatrix, ProbabilityVector # type: ignore
from utils import ConvergenceHandler # type: ignore


class BaseHMM(ABC): 
    """
    Base Abstract Class for HMM
    ----------
    Base Class of Hidden Markov Models (HMM) class that provides a foundation for building specific HMM models.
    """

    def __init__(self,
                 n_states: int,
                 params_init: bool = False,
                 alpha: float = 1.0,
                 verbose: bool = True,
                 random_state: Optional[int] = None,
                 device: Optional[torch.device] = None):

        self.n_states = n_states
        self.seed = random_state
        self.verbose = verbose

        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device

        if params_init:
            self._initial_vector, self._transition_matrix = self.sample_chain_params(alpha,random_state)

    @property
    def transition_matrix(self) -> TransitionMatrix:
        return self._transition_matrix

    @transition_matrix.setter
    def transition_matrix(self, matrix):
        assert (self.n_states,self.n_states) == matrix.shape, 'Matrix dimensions differ from HMM model'
        if isinstance(matrix, TransitionMatrix):
            self._transition_matrix = matrix
        elif isinstance(matrix, torch.Tensor):
            self._transition_matrix = TransitionMatrix(n_states=self.n_states,
                                                       matrix=matrix,
                                                       device=self.device)
        else:
            raise NotImplementedError('Matrix type not supported')

    @property
    def initial_vector(self) -> ProbabilityVector:
        return self._initial_vector

    @initial_vector.setter
    def initial_vector(self, vector):
        assert (self.n_states,) == vector.shape, 'Matrix dimensions differ from HMM model'
        if isinstance(vector, ProbabilityVector):
            self._initial_vector = vector
        elif isinstance(vector, torch.Tensor):
            self._initial_vector = ProbabilityVector(n_states=self.n_states, 
                                                     vector=vector,
                                                     device=self.device)
        else:
            raise NotImplementedError('Matrix type not supported')

    @property
    def fit_score(self) -> float:
        if len(self.train_lengths) == 1:
            return self._log_alpha[0,:,-1].logsumexp(dim=0).item()
        else:
            score = 0.0
            for i, length in enumerate(self.train_lengths):
                score += self._log_alpha[i,:,length-1].logsumexp(dim=0).item()
            return score
        
    @property
    def _check_params(self):
        """Check if the model parameters are set."""
        return self.params

    @abstractproperty
    def params(self) -> Dict[str, torch.Tensor]:
        """Returns the parameters of the model."""
        pass

    @abstractproperty   
    def n_fit_params(self) -> Dict[str, int]:
        """Return the number of trainable model parameters."""
        pass
    
    @abstractproperty
    def dof(self) -> int:
        """Returns the degrees of freedom of the model."""
        pass

    @abstractmethod
    def map_emission(self, emission: torch.Tensor) -> torch.Tensor:
        """Get emission probabilities for a given sequence of observations."""
        pass

    @abstractmethod
    def _check_sequence(self, 
                        sequence: Union[torch.Tensor,np.ndarray], 
                        lengths: Optional[List[int]]=None) -> Sequence[torch.Tensor]:
        """Check if the sequence is valid, encode, transform if necessary."""
        pass

    @abstractmethod
    def _check_theta(self, theta: Optional[torch.Tensor]=None) -> Optional[torch.Tensor]:
        """Returns the parameters of the model."""
        pass

    @abstractmethod
    def sample_B_params(self, seed: Optional[int] = None):
        """Sample the emission parameters."""
        pass

    @abstractmethod
    def update_B_params(self, X: Sequence[torch.Tensor]):
        """Update the emission parameters."""
        pass

    def sample_chain_params(self, alpha: float, seed: Optional[int] = None) -> Tuple[ProbabilityVector, TransitionMatrix]:
        """Initialize the model parameters."""
        return (ProbabilityVector(self.n_states, rand_seed=seed, alpha=alpha, device=self.device), 
                TransitionMatrix(self.n_states, rand_seed=seed, alpha=alpha, device=self.device))

    def _init_train_vars(self,
                         sequence_list: Sequence[torch.Tensor],
                         lengths: Optional[Sequence[int]]=None,
                         theta: Optional[torch.Tensor]=None):
        """Initialize the variables for the forward-backward algorithm."""
        self.n_sequences = len(sequence_list)
        self.n_samples = sequence_list[0].size(0) if lengths is None else max(lengths)
        self.train_lengths = [self.n_samples] if lengths is None else lengths
        
        self._log_alpha = torch.zeros(size=(self.n_sequences, self.n_states, self.n_samples), 
                                      dtype=torch.float64,
                                      device=self.device)
        self._log_beta = torch.zeros(size=(self.n_sequences, self.n_states, self.n_samples), 
                                     dtype=torch.float64, 
                                     device=self.device)
        self._log_gamma = torch.zeros(size=(self.n_sequences, self.n_states, self.n_samples), 
                                      dtype=torch.float64, 
                                      device=self.device)
        self._log_xi = torch.zeros(size=(self.n_sequences, self.n_samples - 1, self.n_states, self.n_states),
                                   dtype=torch.float64, 
                                   device=self.device)

    def _reset_train_vars(self):
        """Reset the variables for the forward-backward algorithm."""
        self._log_alpha.zero_()
        self._log_beta.zero_()
        self._log_gamma.zero_()
        self._log_xi.zero_()
        
    def _viterbi(self, X:torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Viterbi algorithm for decoding the most likely sequence of hidden states."""
        # Check if params are initialized
        self._check_params

        # Tranform sequence to indices
        X_valid = self._check_sequence(X)[0]
        n_samples = X_valid.shape[0]

        # Initialize matrices
        viterbi_path = torch.empty(size=(n_samples,), 
                                   dtype=torch.int32,
                                   device=self.device)
        
        viterbi_prob = torch.empty(size=(self.n_states, n_samples), 
                                       dtype=torch.float64,
                                       device=self.device)
        psi = viterbi_prob.clone()

        # Initialize first column
        viterbi_prob[:,0] = self._initial_vector + self.map_emission(X_valid[0])
        for t in range(1, n_samples):
            trans_seq = viterbi_prob[:,t-1] + self.map_emission(X_valid[t])
            trans_seq = self._transition_matrix + trans_seq.reshape((-1, 1))
            viterbi_prob[:,t] = torch.max(trans_seq, dim=0).values
            psi[:,t] = torch.argmax(trans_seq, dim=0)

        # Backtrack the most likely sequence
        viterbi_path[-1] = torch.argmax(viterbi_prob[:, -1])
        for t in reversed(range(n_samples - 1)):
            viterbi_path[t] = psi[viterbi_path[t + 1], t + 1]

        return viterbi_path, viterbi_prob

    def _forward(self, X:Sequence[torch.Tensor]):
        """Forward pass of the forward-backward algorithm."""
        for i,seq in enumerate(X):
            self._log_alpha[i,:,0].add_(self._initial_vector + self.map_emission(seq[0]))
            for t in range(1, self.train_lengths[i]):
                self._log_alpha[i,:, t].add_(
                    self.map_emission(seq[t])
                    + torch.logsumexp(self._log_alpha[i,:, t - 1].reshape(-1, 1) + self._transition_matrix, dim=0)
                )

    def _backward(self, X:Sequence[torch.Tensor]):
        """Backward pass of the forward-backward algorithm."""
        for i,seq in enumerate(X):
            for t in reversed(range(self.train_lengths[i] - 1)):
                self._log_beta[i,:,t].add_(torch.logsumexp(
                    self._transition_matrix
                    + self.map_emission(seq[t+1])
                    + self._log_beta[i,:, t + 1], dim=1)
                )

    def _gamma(self):
        """Compute the log-Gamma variable in Hidden Markov Model."""
        denom = self._log_alpha + self._log_beta
        self._log_gamma.add_(denom - torch.logsumexp(denom, dim=1, keepdim=True))

    def _xi(self, X:Sequence[torch.Tensor]):
        """Compute the log-Xi variable in Hidden Markov Model."""
        for i,seq in enumerate(X):
            for t in range(self.train_lengths[i] - 1):
                self._log_xi[i,t,:,:].add_(
                    self._log_alpha[i,:, t].reshape(-1, 1)
                    + self._transition_matrix
                    + self.map_emission(seq[t+1])
                    + self._log_beta[i,:,t+1]
                )
                max_t = self.train_lengths[i]
                self._log_xi[i,t,:,:].sub_(torch.logsumexp(self._log_alpha[i,:,max_t-1], dim=0))

    def _E_step(self, X: Sequence[torch.Tensor]):
        """Execute the forward-backward algorithm and compute the log-Gamma and log-Xi variables."""
        self._forward(X)
        self._backward(X)
        self._gamma()
        self._xi(X)
    
    def _M_step(self, X, theta) -> Dict[str, torch.Tensor]:
        """Compute the updated parameters for the model."""

        # Compute the posteriors
        self._E_step(X)

        return {
            'pi': self._accum_pi(),
            'A': self._accum_A()
        }
    
    def _accum_pi(self) -> torch.Tensor:
        """Accumulate the statistics for the initial vector."""
        seq_sum = self._log_gamma[:,:,0].logsumexp(dim=0)
        normed_sum = seq_sum - seq_sum.logsumexp(dim=0)
        return normed_sum

    def _accum_A(self) -> torch.Tensor:
        """Accumulate the statistics for the transition matrix."""
        seq_sum = torch.logsumexp(self._log_xi, dim=(0,1))
        normed_sum = seq_sum - seq_sum.logsumexp(dim=1, keepdim=True)
        return normed_sum
    
    def _update_chain(self, X: Sequence[torch.Tensor], theta: Optional[torch.Tensor] = None):
        """Update the model parameters."""
        new_params = self._M_step(X, theta)
        self._transition_matrix.matrix.copy_(new_params['A'])
        self._initial_vector.matrix.copy_(new_params['pi'])

    def fit(self,
            X: torch.Tensor,
            tol: float = 1e-2,
            max_iter: int = 20,
            n_init: int = 1,
            alpha: float = 1.0,
            post_conv_iter: int = 3,
            plot_score: bool = False,
            ignore_conv: bool = False,
            lengths: Optional[List[int]] = None,
            theta: Optional[torch.Tensor] = None) -> Tuple[Dict[str, torch.Tensor], torch.Tensor]:
        """Fit the model to the given sequence using the EM algorithm."""
        
        # Check if params are initialized
        self._check_params

        # Check sequence parameters and transform if lengths
        X_valid = self._check_sequence(X, lengths)
        valid_theta = self._check_theta(theta)
        self._init_train_vars(X_valid, lengths, valid_theta)

        # Initialize convergence handler
        conv = ConvergenceHandler(tol=tol, 
                                  max_iter=max_iter, 
                                  n_init=n_init,
                                  post_conv_iter=post_conv_iter,
                                  device=self.device, 
                                  verbose=self.verbose)

        distinct_models = {}
        for i in range(n_init):
            if i > 0:
                conv.iter = 0
                self.sample_chain_params(alpha)
                self.sample_B_params()
            
            for _ in range(max_iter):
                # Reset training variables
                self._reset_train_vars()
            
                # Estimate and Update Model parameters
                self._update_chain(X_valid, theta)
                self.update_B_params(X_valid)

                # Check convergence
                if conv.check(new_score=self.fit_score, rank=i) and not ignore_conv:
                    break
                
                # Update iteration count and reset training variables
                conv.iter += 1

            # Save model parameters
            distinct_models[i] = self.params

        # Update params with best model based on score (log-likelihood)
        masked_conv = conv.score.masked_fill(torch.isnan(conv.score), float('-inf'))
        max_scores = torch.max(masked_conv, dim=0).values
        best_model = distinct_models[int(torch.argmax(max_scores).item())]

        # TODO: Set model parameters to best model
        # self._set_params(best_model)

        if plot_score:
            # Define input for plot
            labels = [f'Log-likelihood - Run #{i+1}' for i in range(n_init)]

            # Plot setting
            plt.style.use('ggplot')
            _, ax = plt.subplots(figsize=(10, 7))
            ax.plot(torch.arange(max_iter), 
                    conv.score.cpu(), 
                    linewidth=2, 
                    marker='o', 
                    markersize=5, 
                    label=labels)
            
            ax.set_title('HMM Model Log-Likelihood Convergence')
            ax.set_xlabel('# Iterations')
            ax.set_ylabel('Log-likelihood')
            ax.legend(loc='lower right')
            plt.show()
        
        return best_model, max_scores

    def predict(self, X: torch.Tensor) -> torch.Tensor:
        """Compute the most likely sequence of hidden states."""
        viterbi_path, _ = self._viterbi(X)
        return viterbi_path

    def predict_proba(self, X: torch.Tensor) -> torch.Tensor:
        """Compute the log probability of the most likely sequence of hidden states."""
        _, viterbi_prob = self._viterbi(X)
        return viterbi_prob 
    
    def score(self, X: torch.Tensor, lengths: Optional[Sequence[int]] = None) -> float:
        """Compute the log-likelihood of the given sequence."""
        X_valid = self._check_sequence(X)
        self._init_train_vars(X_valid,lengths)
        self._forward(X_valid)
        return self.fit_score

    def ic(self, X: torch.Tensor, criterion: str = 'AIC') -> float:
        """
        Calculates the information criteria for a given model.

        Parameters:
        ----------
        criterion : str
            The information criterion to compute. Options are 'AIC', 'BIC', and 'HQC'. Default is 'AIC'.
        """

        dof = self.dof
        log_likelihood = self.score(X)
        
        if criterion == 'BIC':
            return -2.0 * log_likelihood + dof * np.log(X.shape[0])
        elif criterion == 'AIC':
            return -2.0 * log_likelihood + 2.0 * dof
        elif criterion == 'HQC':
            return -2.0 * log_likelihood + 2.0 * dof * np.log(np.log(X.shape[0]))
        else:
            raise NotImplementedError(f'{criterion} is not a valid information criterion. Valid options are "AIC", "BIC", and "HQC".')

    def view_params(self):
        """Print the model parameters."""
        for param in self.params.values():
            param.view()
            print('\n')





