from typing import Optional, Dict, Literal, Sequence, Tuple
from abc import ABC, abstractproperty, abstractmethod

import torch
from torch.distributions import Distribution, MixtureSameFamily # type: ignore
from sklearn.cluster import KMeans # type: ignore
from stochastic_matrix import WeightsMatrix # type: ignore
from utils import validate_means, validate_covars, fill_covars # type: ignore


class MixtureEmissions(ABC):
    """
    Mixture model for HMM emissions. This class is an abstract base class for Gaussian, Poisson and other mixture models.
    """

    def __init__(self, 
                 n_dims: int,
                 n_components: int,
                 n_features: int,
                 init_weights: bool = True,
                 alpha: float = 1.0,
                 seed: Optional[int] = None,
                 device: Optional[torch.device] = None):
        
        self.n_components = n_components
        self.n_dims = n_dims
        self.n_features = n_features
        self.device = device
        
        if init_weights:
            self._weights = self.sample_weights(alpha, seed)

    @property
    def weights(self) -> WeightsMatrix:
        try:
            return self._weights
        except AttributeError:
            raise AttributeError('Weights are not initialized')

    @weights.setter
    def weights(self, vector):
        assert (self.n_dims, self.n_components) == vector.shape, 'Matrix dimensions differ from HMM model'
        if isinstance(vector, WeightsMatrix):
            self._weights = vector
        elif isinstance(vector, torch.Tensor):
            self._weights = WeightsMatrix(n_states=self.n_dims, 
                                          n_components=self.n_components,
                                          matrix=vector,
                                          device=self.device)
        else:
            raise NotImplementedError(f'Expected torch Tensor or WeightsMatrix object, got {type(vector)}')
        
    @property
    def mixture_pdf(self) -> MixtureSameFamily:
        """Return the emission distribution for Gaussian Mixture Distribution."""
        return MixtureSameFamily(mixture_distribution = self.weights._matrix,
                                 component_distribution = self.pdf)

    @abstractproperty
    def pdf(self) -> Distribution:
        """Return the emission distribution of Mixture."""
        pass

    @abstractproperty
    def params(self) -> Dict[str, torch.Tensor]:
        """Return the parameters of the Mixture."""
        pass

    @abstractmethod
    def update_emissions_params(self, X: Sequence[torch.Tensor], posterior: torch.Tensor) -> None:
        """Update the parameters of the Mixture."""
        pass 
    
    def sample_weights(self, 
                       alpha: float, 
                       seed: Optional[int]) -> WeightsMatrix:
        """Sample the weights for the mixture."""
        return WeightsMatrix(n_states=self.n_dims,
                            n_components=self.n_components,
                            rand_seed=seed,
                            alpha=alpha,
                            device=self.device)

    def map_emission(self, 
                     emission: torch.Tensor) -> torch.Tensor:
        return torch.logsumexp(self.weights + self.pdf.log_prob(emission), dim=1)
    
    def compute_weights(self, gamma: torch.Tensor) -> torch.Tensor:    
        gamma_reduced = gamma.sum(0).sum(-1)
        weights_exp = gamma_reduced / gamma_reduced.sum(dim=1, keepdim=True)
        return weights_exp.log()
    
    def compute_responsibilities(self, 
                                 X: torch.Tensor) -> torch.Tensor:
        """Compute the responsibilities for each component."""
        n_observations = X.size(dim=0)
        log_responsibilities = torch.zeros(size=(self.n_dims,self.n_components,n_observations), 
                                           dtype=torch.float64, 
                                           device=self.device)

        for t in range(n_observations):
            comps_resp = self.weights.matrix + self.pdf.log_prob(X[t])
            log_responsibilities[:,:,t].add_(comps_resp - comps_resp.logsumexp(dim=1, keepdim=True))
        
        return log_responsibilities
    

class GaussianMixtureEmissions(MixtureEmissions):
    """
    Gaussian Mixture Model for HMM emissions.    
    
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
                 n_components: int,
                 n_features: int,
                 params_init: bool = True,
                 alpha: float = 1.0,
                 covariance_type: COVAR_TYPES_HINT = 'full',
                 min_covar: float = 1e-3,
                 seed: Optional[int] = None,
                 device: Optional[torch.device] = None):
        
        self.min_covar = min_covar
        self.covariance_type = covariance_type
        
        MixtureEmissions.__init__(self,n_dims,n_components,n_features,params_init,alpha,seed,device)
        
        if params_init:
            self._means, self._covs = self.sample_emissions_params(seed)
            
    @property
    def means(self) -> torch.Tensor:
        return self._means
    
    @means.setter
    def means(self, means: torch.Tensor):
        valid_means = validate_means(means, self.n_dims, self.n_features, self.n_components)
        self._means = valid_means.to(self.device)

    @property
    def covs(self) -> torch.Tensor:
        return self._covs

    @covs.setter
    def covs(self, new_covars: torch.Tensor):
        """Setter function for the covariance matrices."""
        valid_covars = validate_covars(new_covars, self.covariance_type, self.n_dims, self.n_features, self.n_components)
        self._covs = fill_covars(valid_covars, self.covariance_type, self.n_dims, self.n_features, self.n_components).to(self.device)

    @property
    def pdf(self):
        return torch.distributions.MultivariateNormal(loc=self.means, 
                                                      covariance_matrix=self.covs)
    
    @property
    def params(self):
        return {'weights': self.weights.matrix,
                'means': self.means, 
                'covs': self.covs}
    
    def sample_emissions_params(self,
                                seed: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        
        means = torch.zeros(size=(self.n_dims, self.n_components, self.n_features), 
                                  dtype=torch.float64, 
                                  device=self.device)
        
        covs = torch.eye(n=self.n_features, 
                               dtype=torch.float64,
                               device=self.device).expand((self.n_dims, self.n_components, self.n_features, self.n_features)).clone()
        # self._k_means = KMeans(n_clusters=(self.n_dims), 
        #                        random_state=seed, 
        #                        n_init="auto").fit(X)
        # torch.from_numpy(self._k_means.cluster_centers_).reshape(self.means.shape)
        return means, covs
    
    def compute_means(self, 
                      X: Sequence[torch.Tensor], 
                      responsibilities: torch.Tensor) -> torch.Tensor:
        """Compute the means for each component."""
        new_mean = torch.zeros(size=(self.n_dims,self.n_components,self.n_features), 
                                dtype=torch.float64, 
                                device=self.device)
        
        for i, seq in enumerate(X):
            gamma_seq = responsibilities[i,:,:seq.size(dim=0)].unsqueeze(dim=-1)
            weighted_seq = gamma_seq.expand((-1,self.n_components,-1,self.n_features)) * seq
            new_mean += weighted_seq.sum(dim=-2)
            
        new_mean /= responsibilities.sum(dim=0).sum(dim=-1, keepdim=True)

        return new_mean
    
    def compute_covs(self, 
                     X: Sequence[torch.Tensor],
                     responsibilities: torch.Tensor) -> torch.Tensor:
        """Compute the covariances for each component."""
        new_covs = torch.zeros(size=(self.n_dims,self.n_components,self.n_features,self.n_features), 
                           dtype=torch.float64, 
                           device=self.device)

        for i, seq in enumerate(X):
            diff = seq.expand(self.n_dims,self.n_components,-1, -1) - self.means.unsqueeze(-2)
            product = diff.unsqueeze(-1) @ diff.unsqueeze(-2)
            weighted_product = responsibilities[i,:,:seq.size(0)].unsqueeze(-1).unsqueeze(-1) * product
            new_covs += weighted_product.sum(dim=-3)

        new_covs /= responsibilities.sum(dim=0).sum(dim=-1, keepdim=True).unsqueeze(-1)
        new_covs += self.min_covar * torch.eye(self.n_features, device=self.device)
        
        return new_covs
    
    def update_emissions_params(self, X, posterior):
        self.weights.matrix.copy_(self.compute_weights(posterior))
        self._means.copy_(self.compute_means(X, posterior)) 
        self._covs.copy_(self.compute_covs(X, posterior))