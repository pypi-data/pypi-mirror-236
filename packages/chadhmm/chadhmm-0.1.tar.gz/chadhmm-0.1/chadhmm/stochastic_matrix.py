from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, Union, Sequence, List, TypeVar

import torch
import numpy as np
from torch.distributions import Categorical
from utils import print_table, states_names, init_matrix # type: ignore

class StochasticMatrix(ABC): ...
class EmissionMatrix(StochasticMatrix): ...
class TransitionMatrix(StochasticMatrix): ...
class ProbabilityVector(StochasticMatrix): ...
class DurationMatrix(StochasticMatrix): ...
class WeightsMatrix(StochasticMatrix): ...

MAT_OPS = TypeVar('MAT_OPS', bound=Union[StochasticMatrix, np.ndarray, torch.Tensor])
SAMP_DISTS = frozenset(("Dirichlet", "Uniform"))

torch.set_printoptions(precision=4, profile="full")

class StochasticMatrix(ABC):
    """ 
    Stochastic Matrix
    ----------
    This class is used to represent a stochastic matrix. It is a wrapper around a torch.Tensor with a
    torch.distributions.Categorical distribution.

    Parameters:
    ----------
    matrix (Categorical):
        The stochastic matrix.
    seed (Optional[int]):
        Random seed to use for reproducible results.
    
    Attributes:
    ----------
    matrix (torch.Tensor):
        The stochastic matrix.
    seed (Optional[int]):
        Random seed to use for reproducible results.
    shape (torch.Size):
        Shape of the stochastic matrix.
    """

    def __init__(self,
                 matrix: torch.Tensor,
                 device: Optional[torch.device] = None,
                 seed: Optional[int] = None):

        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
        
        self._matrix = matrix.to(self.device)
        self.seed = seed

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(shape={self.matrix.shape})"

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractproperty
    def view(self):
        pass

    @property
    def matrix(self) -> torch.Tensor:
        return self._matrix

    @matrix.setter
    def matrix(self, matrix: Union[torch.Tensor, np.ndarray]):
        assert self.shape == matrix.shape(), "Matrix must be the same shape as the original"
        self._matrix = Categorical(logits=matrix, validate_args=True)
        
    def __mul__(self, other: MAT_OPS) -> torch.Tensor:
        if isinstance(other, StochasticMatrix):
            return self.matrix * other.matrix
        elif isinstance(other, torch.Tensor):
            return self.matrix * other
        elif isinstance(other, np.ndarray):
            return self.matrix * torch.from_numpy(other)
        else:
            raise NotImplementedError(f'Expected one of {MAT_OPS}, got {type(other)}')
        
    def __rmul__(self, other: MAT_OPS) -> torch.Tensor:
        return self.__mul__(other)
    
    def __matmul__(self, other: MAT_OPS) -> torch.Tensor:
        if isinstance(other, StochasticMatrix):
            return self.matrix @ other.matrix
        elif isinstance(other, torch.Tensor):
            return self.matrix @ other
        elif isinstance(other, np.ndarray):
            return self.matrix @ torch.from_numpy(other)
        else:
            raise NotImplementedError(f'Expected one of {MAT_OPS}, got {type(other)}')
    
    def __rmatmul__(self, other: MAT_OPS) -> torch.Tensor:
        return self.__matmul__(other)

    def __truediv__(self, other: MAT_OPS) -> torch.Tensor:
        if isinstance(other, StochasticMatrix):
            return self.matrix / other.matrix
        elif isinstance(other, torch.Tensor):
            return self.matrix / other
        elif isinstance(other, np.ndarray):
            return self.matrix / torch.from_numpy(other)
        else:
            raise NotImplementedError(f'Expected one of {MAT_OPS}, got {type(other)}')
    
    def __rtruediv__(self, other: MAT_OPS) -> torch.Tensor:
        return self.__truediv__(other)

    def __add__(self, other: MAT_OPS) -> torch.Tensor:
        if isinstance(other, StochasticMatrix):
            return self.matrix + other.matrix
        elif isinstance(other, torch.Tensor):
            return self.matrix + other
        elif isinstance(other, np.ndarray):
            return self.matrix + torch.from_numpy(other)
        else:
            raise NotImplementedError(f'Expected one of {MAT_OPS}, got {type(other)}')
        
    def __radd__(self, other: MAT_OPS) -> torch.Tensor:
        return self.__add__(other)
    
    def __sub__(self, other: MAT_OPS) -> torch.Tensor:
        if isinstance(other, StochasticMatrix):
            return self.matrix - other.matrix
        elif isinstance(other, torch.Tensor):
            return self.matrix - other
        elif isinstance(other, np.ndarray):
            return self.matrix - torch.from_numpy(other)
        else:
            raise NotImplementedError(f'Expected one of {MAT_OPS}, got {type(other)}')
        
    def __rsub__(self, other: MAT_OPS) -> torch.Tensor:
        return self.__sub__(other)

    def __eq__(self, other: MAT_OPS) -> bool:
        if isinstance(other, StochasticMatrix):
            return torch.equal(self.matrix, other.matrix)
        elif isinstance(other, torch.Tensor):
            return torch.equal(self.matrix, other)
        elif isinstance(other, np.ndarray):
            return torch.equal(self.matrix, torch.from_numpy(other))
        else:
            raise NotImplementedError(f'Expected one of {MAT_OPS}, got {type(other)}')
    
    def __len__(self) -> int:
        return self.matrix.numel()
    
    def __getitem__(self, idx) -> torch.Tensor:
        if isinstance(idx, tuple):
            row_idx, col_idx = idx
            if isinstance(row_idx, slice) or isinstance(col_idx, slice):
                return self.matrix[row_idx, col_idx]
            else:
                return self.matrix[row_idx, col_idx]
        else:
            return self.matrix[idx]
    
    def __setitem__(self, row_idx, col_idx, value):
        self.matrix[row_idx, col_idx] = value


class EmissionMatrix(StochasticMatrix):
    """
    Emission Matrix
    ---------------
    A Class representing the Emission matrix of a finite Markov chain.
    """

    def __init__(self,
                 n_states: int,
                 n_emissions: int,
                 matrix: Optional[torch.Tensor] = None,
                 states: Optional[Sequence[str]]= None,
                 emissions: Optional[Sequence[str]]= None,
                 rand_seed: Optional[int] = None,
                 alpha: float = 1.0,
                 device: Optional[torch.device] = None):
        
        self._n_states = n_states
        self._n_emissions = n_emissions
        self.states = states_names(n=n_states, state_type='state') if states is None else states
        self.emissions = states_names(n=n_emissions, state_type='emission') if emissions is None else emissions

        if matrix is None:
            mat_size = (n_states, n_emissions)
            matrix = torch.log(init_matrix(prior = alpha, target_size=mat_size))

        super().__init__(matrix=matrix,
                         seed=rand_seed,
                         device=device)
        
    def __str__(self) -> str:
        return f"EmissionMatrix(n_states = {self.n_states}, n_emissions = {self.n_emissions})"

    def view(self, log_scale: bool = False):
        vals = self.matrix.exp() if not log_scale else self.matrix
        vals = torch.round(vals, decimals=3).tolist()
        
        trans = [[self.states[idx]] + row for idx, row in enumerate(vals)]

        print_table(title='Emission Matrix',
                    header=['State\Emission'] + self.emissions, 
                    rows=trans)

    @property
    def n_states(self) -> int:
        return self._n_states

    @property
    def n_emissions(self) -> int:
        return self._n_emissions

    @property
    def states(self) -> Optional[List[str]]:
        return self._states

    @states.setter
    def states(self, states: Sequence[str]):
        unique_names = len(set(states))

        if unique_names != self.n_states:
            raise ValueError(f'Expected {self.n_states} unique states, got {unique_names}')
        else:
            self._states = states

    @property
    def emissions(self) -> Optional[List[str]]:
        return self._emissions

    @emissions.setter
    def emissions(self, emissions: Sequence[str]):
        unique_names = len(set(emissions))
        
        if unique_names != self.n_emissions:
            raise ValueError(f'Expected {self.n_emissions} unique emissions, got {unique_names}')
        else:
            self._emissions = emissions

class TransitionMatrix(StochasticMatrix):
    """
    Transition Matrix
    --------
    A Class representing the Transition matrix of a finite Markov chain.

    Parameters
    ----------
    n_states : int
        Number of states in the system.
    matrix : Optional[torch.Tensor], optional
        An initial probability distribution matrix, by default `None`.
    states : Optional[List[str]], optional
        A list of names/labels for each state in the system, by default `None`.
    rand_seed : Optional[int], optional
        The seed for the random number generator, by default `None`.
    init_dist : Optional[SAMPLING_DISTRIBUTIONS], optional
        The distribution to use when initializing the matrix if not provided, by default `'Uniform'`.
    alpha : Optional[float], optional
        The prior to use when initializing the matrix if not provided, by default `1.0`.

    Note
    ----
    If `matrix` is provided, it will be used as the initial probability distribution. 
    If `matrix` is not provided, a distribution specified by `init_dist` will be used to initialize the matrix.
    """

    def __init__(self,
                 n_states: int,
                 matrix: Optional[torch.Tensor] = None,
                 states: Optional[Sequence[str]]= None,
                 rand_seed: Optional[int] = None,
                 alpha: float = 1.0,
                 semi_markov: bool = False,
                 device: Optional[torch.device] = None):
        
        self._n_states = n_states
        self.semi_markov = semi_markov
        self.states = states_names(n=n_states, state_type='state') if states is None else states

        if matrix is None:
            mat_size = (n_states, n_states)
            matrix = torch.log(init_matrix(prior = alpha, target_size=mat_size, semi=semi_markov))

        super().__init__(matrix=matrix,
                         seed=rand_seed,
                         device=device)

    def __str__(self) -> str:
        return f"TransitionMatrix(n_states = {self.n_states})"

    def view(self, log_scale: bool = False):
        vals = self.matrix.exp() if not log_scale else self.matrix
        vals = torch.round(vals, decimals=3).tolist()
        
        trans = [[self.states[idx]] + row for idx, row in enumerate(vals)]

        print_table(title='Transition Matrix',
                    header=['State\State'] + self.states, 
                    rows=trans)

    @property
    def n_states(self) -> int:
        return self._n_states

    @property
    def states(self) -> Optional[List[str]]:
        return self._states

    @states.setter
    def states(self, states: list):
        if len(set(states)) != self.n_states:
            raise ValueError(f'Expected {self.n_states} states, got {len(set(states))}')
        else:
            self._states = states


class DurationMatrix(StochasticMatrix):
    """
    Duration Matrix
    ---------------
    A Class representing the Duration matrix of a semi-Markov chain.
    """

    def __init__(self,
                 n_states: int,
                 max_dur: int,
                 matrix: Optional[torch.Tensor] = None,
                 states: Optional[Sequence[str]]= None,
                 durations: Optional[Sequence[str]]= None,
                 rand_seed: Optional[int] = None,
                 alpha: float = 1.0,
                 device: Optional[torch.device] = None):
        
        self._n_states = n_states
        self._max_dur = max_dur
        self.states = states_names(n=n_states, state_type='state') if states is None else states
        self.durations = states_names(n=max_dur, state_type='duration') if durations is None else durations

        if matrix is None:
            mat_size = (n_states, max_dur)
            matrix = torch.log(init_matrix(prior = alpha, target_size=mat_size))

        super().__init__(matrix=matrix,
                         seed=rand_seed,
                         device=device)
        
    def __str__(self) -> str:
        return f"DurationMatrix(states = {self.n_states}, max_duration = {self.max_duration})"

    def view(self, log_scale: bool = False):
        vals = self.matrix.exp() if not log_scale else self.matrix
        vals = torch.round(vals, decimals=3).tolist()
        
        trans = [[self.states[idx]] + row for idx, row in enumerate(vals)]

        print_table(title='Duration Matrix',
                    header=['State\Emission'] + self.durations, 
                    rows=trans)

    @property
    def n_states(self) -> int:
        return self._n_states

    @property
    def durations(self) -> Optional[List[str]]:
        return self._durations

    @durations.setter
    def durations(self, durations: list):
        if len(set(durations)) != self.max_duration:
            raise ValueError(f'Expected {self.max_duration} unique durations, got {len(set(durations))}')
        else:
            self._durations = durations

    @property
    def states(self) -> Optional[List[str]]:
        return self._states

    @states.setter
    def states(self, states: list):
        if len(set(states)) != self.n_states:
            raise ValueError(f'Expected {self.n_states} unique states, got {len(set(states))}')
        else:
            self._states = states

    @property
    def max_duration(self) -> int:
        return self._max_dur


class WeightsMatrix(StochasticMatrix):
    """
    Weights Matrix
    ---------------
    A Class representing the Weights matrix of a Gaussian Mixture HMM.
    """

    def __init__(self,
                 n_states: int,
                 n_components: int,
                 matrix: Optional[torch.Tensor] = None,
                 states: Optional[Sequence[str]] = None,
                 components: Optional[Sequence[str]] = None,
                 rand_seed: Optional[int] = None,
                 alpha: float = 1.0,
                 device: Optional[torch.device] = None):
        
        self._n_states = n_states
        self._n_components = n_components
        self.states = states_names(n=n_states, state_type='state') if states is None else states
        self.components = states_names(n=n_components, state_type='component') if components is None else components

        if matrix is None:
            mat_size = (n_states, n_components)
            matrix = torch.log(init_matrix(prior = alpha, target_size=mat_size))

        super().__init__(matrix=matrix,
                         seed=rand_seed,
                         device=device)
        
    def __str__(self) -> str:
        return f"WeightsMatrix(n_states = {self.n_states}, n_components = {self.n_components})"

    def view(self, log_scale: bool = False):
        vals = self.matrix.exp() if not log_scale else self.matrix
        vals = torch.round(vals, decimals=3).tolist()
        
        trans = [[self.states[idx]] + row for idx, row in enumerate(vals)]

        print_table(title='Weights Matrix',
                    header=['State\Component'] + self.components, 
                    rows=trans)

    @property
    def n_states(self) -> int:
        return self._n_states

    @property
    def n_components(self) -> int:
        return self._n_components

    @property
    def states(self) -> Optional[List[str]]:
        return self._states

    @states.setter
    def states(self, states: list):
        if len(set(states)) != self.n_states:
            raise ValueError(f'Expected {self.n_states} unique states, got {len(set(states))}')
        else:
            self._states = states

    @property
    def components(self) -> Optional[List[str]]:
        return self._components
    
    @components.setter
    def components(self, components: list):
        if len(set(components)) != self.n_components:
            raise ValueError(f'Expected {self.n_components} unique components, got {len(set(components))}')
        else:
            self._components = components


class ProbabilityVector(StochasticMatrix):
    """
    Probability Vector
    ------------------
    A class used to represent a probability vector.

    Parameters
    ----------
    n_states : int
        Number of states in the system.
    vector : Optional[torch.Tensor], optional
        An initial probability distribution vector, by default `None`.
    states : Optional[List[str]], optional
        A list of names/labels for each state in the system, by default `None`.
    rand_seed : Optional[int], optional
        The seed for the random number generator, by default `None`.
    init_dist : Optional[SAMPLING_DISTRIBUTIONS], optional
        The distribution to use when initializing the vector if not provided, by default `'Uniform'`.
    alpha : Optional[float], optional
        The prior to use when initializing the vector if not provided, by default `1.0`.

    Note
    ----
    If `vector` is provided, it will be used as the initial probability distribution. 
    If `vector` is not provided, a distribution specified by `init_dist` will be used to initialize the vector.
    """

    def __init__(self,
                 n_states: int,
                 vector: Optional[torch.Tensor] = None,
                 states: Optional[Sequence[str]]= None,
                 rand_seed: Optional[int] = None,
                 alpha: float = 1.0,
                 device: Optional[torch.device] = None):
        
        self._n_states = n_states
        self.states = states_names(n=n_states, state_type='state') if states is None else states

        if vector is None:
            mat_size = (n_states,)
            vector = torch.log(init_matrix(prior = alpha, target_size=mat_size))

        super().__init__(matrix=vector,
                         seed=rand_seed,
                         device=device)

    def __str__(self) -> str:
        return f"ProbabilityVector(n_states = {self.n_states})"
    
    def view(self, log_scale: bool = False):
        vals = self.matrix.exp() if not log_scale else self.matrix
        row_name = 'Log Prob' if log_scale else 'Prob'
        vals = torch.round(vals, decimals=3).tolist()
        
        print_table(title='Initial Distribution',
                    header=['State'] + self.states, 
                    rows=[[row_name] + vals])

    @property
    def n_states(self) -> int:
        return self._n_states

    @property
    def states(self) -> List[str]:
        return self._states

    @states.setter
    def states(self, states: list):
        if len(set(states)) == self.n_states:
            self._states = states
        else:
            raise ValueError(f'Expected {self.n_states} unique states, got {len(set(states))}')
        