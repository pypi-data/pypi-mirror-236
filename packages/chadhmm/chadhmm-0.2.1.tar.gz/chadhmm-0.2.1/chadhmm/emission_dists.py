from typing import Optional, Sequence, Literal, Tuple
from sklearn.cluster import KMeans # type: ignore
import torch

from stochastic_matrix import EmissionMatrix # type: ignore
from utils import validate_means, validate_covars, fill_covars # type: ignore

class CategoricalEmissions:
    """
    Categorical emission distribution for HMMs.

    Parameters:
    ----------
    n_dims (int):
        Number of hidden states in the model.
    n_emissions (int):
        Number of emissions in the model.
    init_params (bool):
        Whether to initialize the emission parameters.
    alpha (float):
        Dirichlet concentration parameter for the prior over emission probabilities.
    seed (int):
        Random seed for reproducibility.
    device (torch.device):
        Device on which to fit the model.

    Attributes:
    ----------
    emission_matrix (EmissionMatrix):
        Emission matrix representing the categorical distribution.
    """

    def __init__(self,
                n_dims: int,
                n_emissions: int,
                init_params: bool = True,
                alpha: float = 1.0,
                seed: Optional[int] = None,
                device: Optional[torch.device] = None):
            
        self.n_dims = n_dims
        self.n_emissions = n_emissions
        self.device = device

        if init_params:
            self._emission_matrix = self.sample_emissions_params(alpha, seed)  

    @property
    def emission_matrix(self) -> EmissionMatrix:
        return self._emission_matrix
    
    @emission_matrix.setter
    def emission_matrix(self, matrix):
        assert (self.n_dims,self.n_emissions) == matrix.shape, f'Expected matrix shape {(self.n_dims,self.n_emissions)} but got {matrix.shape}'
        if isinstance(matrix, EmissionMatrix):
            self._emission_matrix = matrix
        elif isinstance(matrix, torch.Tensor):
            self._emission_matrix = EmissionMatrix(n_states=self.n_dims, 
                                                   n_emissions=self.n_emissions, 
                                                   matrix=matrix,
                                                   device=self.device)
        else:
            raise NotImplementedError('Matrix type not supported')

    def sample_emissions_params(self, 
                                alpha: float, 
                                seed: Optional[int]=None) -> EmissionMatrix:
        return EmissionMatrix(n_states=self.n_dims,
                            n_emissions=self.n_emissions,
                            rand_seed=seed,
                            alpha=alpha,
                            device=self.device)

    def map_emission(self, x: torch.Tensor) -> torch.Tensor:
        return self._emission_matrix[:,x].squeeze()

    def compute_emprobs(self, 
                        X: Sequence[torch.Tensor],
                        gamma: torch.Tensor) -> torch.Tensor:  
        """Compute the emission probabilities for each hidden state."""
        emission_mat = torch.zeros(size=(self.n_dims, self.n_emissions),
                                   dtype=torch.float64,
                                   device=self.device)

        for i, seq in enumerate(X):
            seq_size = seq.size(dim=0)
            
            # Creating masks for each emission and summing up gamma values
            masks = (seq.view(1, 1, seq_size) == torch.arange(self.n_emissions, device=self.device).view(1, -1, 1))
            gamma_i = gamma[i, :, :seq_size].unsqueeze(1)
            emission_mat += (gamma_i * masks).sum(dim=2)
                    
        # Normalizing the emission matrix
        emission_mat /= gamma.sum(dim=0).sum(dim=1, keepdim=True)

        return emission_mat.log()

    def update_emissions_params(self, X: Sequence[torch.Tensor], gamma: torch.Tensor):
        self._emission_matrix.matrix.copy_(self.compute_emprobs(X, gamma))
        

class GaussianEmissions:
    """
    Gaussian Distribution for HMM emissions.    
    
    Parameters:
    ----------
    n_dims (int):
        Number of mixtures in the model. This is equal to the number of hidden states in the HMM.
    n_components (int):
        Number of components in the mixture model.
    n_features (int):
        Number of features in the data.
    init_weights (bool):
        Whether to initialize the mixture weights prior to fitting.
    init_dist ():
        Distribution to use for initializing the mixture weights.
    alpha (float):
        Dirichlet concentration parameter for the prior over mixture weights.
    k_means (bool):
        Whether to initialize the mixture means using K-Means clustering.
    min_covar (float):
        Minimum covariance for the mixture components.
    covariance_type (COVAR_TYPES):
        Type of covariance matrix to use for the mixture components. One of 'spherical', 'tied', 'diag', 'full'.
    dims (Sequence[str]):
        Names of the mixtures in the model.
    seed (int):
        Random seed for reproducibility.
    device (torch.device):
        Device to use for computations.
    """

    COVAR_TYPES_HINT = Literal['spherical', 'tied', 'diag', 'full']

    def __init__(self, 
                 n_dims: int,
                 n_features: int,
                 params_init: bool = True,
                 covariance_type: COVAR_TYPES_HINT = 'full',
                 min_covar: float = 1e-3,
                 random_state: Optional[int] = None,
                 device: Optional[torch.device] = None):
        
        self.n_dims = n_dims
        self.n_features = n_features
        self.device = device
        self.min_covar = min_covar
        self.covariance_type = covariance_type

        if params_init:
            self._means, self._covs = self.sample_emissions_params(random_state)
            
    @property
    def means(self) -> torch.Tensor:
        return self._means
    
    @means.setter
    def means(self, means: torch.Tensor):
        valid_means = validate_means(means, self.n_dims, self.n_features)
        self._means = valid_means.to(self.device)

    @property
    def covs(self) -> torch.Tensor:
        return self._covs

    @covs.setter
    def covs(self, new_covars: torch.Tensor):
        """Setter function for the covariance matrices."""
        valid_covars = validate_covars(new_covars, self.covariance_type, self.n_dims, self.n_features)
        self._covs = fill_covars(valid_covars, self.covariance_type, self.n_dims, self.n_features).to(self.device)

    @property
    def pdf(self):
        return torch.distributions.MultivariateNormal(loc=self.means, 
                                                      covariance_matrix=self.covs)
    
    def map_emission(self, x: torch.Tensor) -> torch.Tensor:
        return self.pdf.log_prob(x)
    
    @property
    def params(self):
        return {'means': self.means, 
                'covs': self.covs}
    
    def sample_emissions_params(self,
                                seed: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        
        means = torch.zeros(size=(self.n_dims, self.n_features), 
                                    dtype=torch.float64, 
                                    device=self.device)
            
        covs = torch.eye(n=self.n_features, 
                                dtype=torch.float64,
                                device=self.device).expand((self.n_dims, self.n_features, self.n_features)).clone()
        # self._k_means = KMeans(n_clusters=(self.n_dims), 
        #                        random_state=seed, 
        #                        n_init="auto").fit(X)
        # torch.from_numpy(self._k_means.cluster_centers_).reshape(self.means.shape)
        return means, covs
    
    def compute_means(self, 
                      X: Sequence[torch.Tensor], 
                      gamma: torch.Tensor) -> torch.Tensor:
        """Compute the means for each hidden state"""
        new_mean = torch.zeros(size=(self.n_dims, self.n_features), 
                                dtype=torch.float64, 
                                device=self.device)
        
        for i, seq in enumerate(X):
            gamma_seq = gamma[i,:,:seq.size(dim=0)].unsqueeze(dim=-1)
            weighted_seq = gamma_seq.expand((-1, -1, self.n_features)) * seq
            new_mean += weighted_seq.sum(dim=-2)
            
        new_mean /= gamma.sum(dim=0).sum(dim=-1, keepdim=True)

        return new_mean

    def compute_covs(self, 
                     X: Sequence[torch.Tensor],
                     gamma: torch.Tensor) -> torch.Tensor:
        """Compute the covariances for each component."""
        new_covs = torch.zeros(size=(self.n_dims,self.n_features, self.n_features), 
                           dtype=torch.float64, 
                           device=self.device)

        for i, seq in enumerate(X):
            diff = seq.unsqueeze(0).expand(self.n_dims, -1, -1) - self.means.unsqueeze(-2)
            product = diff.unsqueeze(-1) @ diff.unsqueeze(-2)
            
            weighted_product = gamma[i, :, :seq.size(0)].unsqueeze(-1).unsqueeze(-1) * product
            new_covs += weighted_product.sum(dim=-3)

        new_covs /= gamma.sum(dim=0).sum(dim=-1, keepdim=True).unsqueeze(-1)
        new_covs += self.min_covar * torch.eye(self.n_features, device=self.device)

        return new_covs
    
    def update_emissions_params(self, X: Sequence[torch.Tensor], posterior: torch.Tensor):
        self._means.copy_(self.compute_means(X, posterior))
        self._covs.copy_(self.compute_covs(X, posterior))

class BernoulliEmissions: ...
class GammaEmissions: ...
class InverseGammaEmissions: ...
class InverseWishartEmissions: ...
class StudentTEmissions: ...
class WishartEmissions: ...
class MultinomialEmissions: ...
class ExponentialEmissions: ...
class weibullEmissions: ...
class BetaEmissions: ...
class NegativeBinomialEmissions: ...
class BinomialEmissions: ...
class PoissonEmissions: ...