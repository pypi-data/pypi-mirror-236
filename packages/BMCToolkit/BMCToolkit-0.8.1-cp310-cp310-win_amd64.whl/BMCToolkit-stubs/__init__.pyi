"""
Pybind11 version of the BMCToolkit C++ library.
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['ClusterSortingMethod', 'KL_divergence_rate_difference_between_models', 'OrderOfBMC', 'PreferredHardware', 'SingularValueCalculationMethod', 'SpectralClusteringMethod', 'compute_bmcs_parameters', 'compute_cluster_difference', 'compute_cluster_improvement', 'compute_clusters_from_trajectory', 'compute_equilibrium_distribution_lift', 'compute_frequency_matrix_lift', 'compute_k_means', 'compute_spectral_clustering', 'compute_spectral_norm', 'compute_transition_matrix_lift', 'generate_sample_path', 'generate_trimmed_matrix', 'get_equilibrium_distribution_proj', 'get_frequency_matrix_proj', 'get_limiting_singular_value_distribution_of_frequency_matrix', 'get_transition_matrix_proj', 'label_clusters', 'label_clusters_by_decr_equilibrium_distribution', 'label_clusters_by_decr_size', 'label_clusters_by_incr_equilibrium_distribution', 'label_clusters_by_incr_size', 'order_selection_by_minimizing_information_criteria', 'project_sample_path', 'trim_frequency_matrix']
class ClusterSortingMethod:
    """
    Members:
    
      DECR_EQUILIBRIUM_DISTRIBUTION
    
      DECR_SIZE
    
      INCR_EQUILIBRIUM_DISTRIBUTION
    
      INCR_SIZE
    """
    DECR_EQUILIBRIUM_DISTRIBUTION: typing.ClassVar[ClusterSortingMethod]  # value = <ClusterSortingMethod.DECR_EQUILIBRIUM_DISTRIBUTION: 0>
    DECR_SIZE: typing.ClassVar[ClusterSortingMethod]  # value = <ClusterSortingMethod.DECR_SIZE: 1>
    INCR_EQUILIBRIUM_DISTRIBUTION: typing.ClassVar[ClusterSortingMethod]  # value = <ClusterSortingMethod.INCR_EQUILIBRIUM_DISTRIBUTION: 2>
    INCR_SIZE: typing.ClassVar[ClusterSortingMethod]  # value = <ClusterSortingMethod.INCR_SIZE: 3>
    __members__: typing.ClassVar[dict[str, ClusterSortingMethod]]  # value = {'DECR_EQUILIBRIUM_DISTRIBUTION': <ClusterSortingMethod.DECR_EQUILIBRIUM_DISTRIBUTION: 0>, 'DECR_SIZE': <ClusterSortingMethod.DECR_SIZE: 1>, 'INCR_EQUILIBRIUM_DISTRIBUTION': <ClusterSortingMethod.INCR_EQUILIBRIUM_DISTRIBUTION: 2>, 'INCR_SIZE': <ClusterSortingMethod.INCR_SIZE: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OrderOfBMC:
    """
    Members:
    
      ZEROTH_ORDER_BMC
    
      FIRST_ORDER_BMC
    """
    FIRST_ORDER_BMC: typing.ClassVar[OrderOfBMC]  # value = <OrderOfBMC.FIRST_ORDER_BMC: 1>
    ZEROTH_ORDER_BMC: typing.ClassVar[OrderOfBMC]  # value = <OrderOfBMC.ZEROTH_ORDER_BMC: 0>
    __members__: typing.ClassVar[dict[str, OrderOfBMC]]  # value = {'ZEROTH_ORDER_BMC': <OrderOfBMC.ZEROTH_ORDER_BMC: 0>, 'FIRST_ORDER_BMC': <OrderOfBMC.FIRST_ORDER_BMC: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PreferredHardware:
    """
    Members:
    
      CPU
    
      GPU
    """
    CPU: typing.ClassVar[PreferredHardware]  # value = <PreferredHardware.CPU: 0>
    GPU: typing.ClassVar[PreferredHardware]  # value = <PreferredHardware.GPU: 1>
    __members__: typing.ClassVar[dict[str, PreferredHardware]]  # value = {'CPU': <PreferredHardware.CPU: 0>, 'GPU': <PreferredHardware.GPU: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SingularValueCalculationMethod:
    """
    Members:
    
      VIA_MATRIX_PRODUCT
    
      VIA_HERMITIZATION
    
      VIA_BDCSVD
    """
    VIA_BDCSVD: typing.ClassVar[SingularValueCalculationMethod]  # value = <SingularValueCalculationMethod.VIA_BDCSVD: 2>
    VIA_HERMITIZATION: typing.ClassVar[SingularValueCalculationMethod]  # value = <SingularValueCalculationMethod.VIA_HERMITIZATION: 1>
    VIA_MATRIX_PRODUCT: typing.ClassVar[SingularValueCalculationMethod]  # value = <SingularValueCalculationMethod.VIA_MATRIX_PRODUCT: 0>
    __members__: typing.ClassVar[dict[str, SingularValueCalculationMethod]]  # value = {'VIA_MATRIX_PRODUCT': <SingularValueCalculationMethod.VIA_MATRIX_PRODUCT: 0>, 'VIA_HERMITIZATION': <SingularValueCalculationMethod.VIA_HERMITIZATION: 1>, 'VIA_BDCSVD': <SingularValueCalculationMethod.VIA_BDCSVD: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SpectralClusteringMethod:
    """
    Members:
    
      SVD_FULL
    
      SVD_PARTIAL
    """
    SVD_FULL: typing.ClassVar[SpectralClusteringMethod]  # value = <SpectralClusteringMethod.SVD_FULL: 0>
    SVD_PARTIAL: typing.ClassVar[SpectralClusteringMethod]  # value = <SpectralClusteringMethod.SVD_PARTIAL: 1>
    __members__: typing.ClassVar[dict[str, SpectralClusteringMethod]]  # value = {'SVD_FULL': <SpectralClusteringMethod.SVD_FULL: 0>, 'SVD_PARTIAL': <SpectralClusteringMethod.SVD_PARTIAL: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def KL_divergence_rate_difference_between_models(transition_matrix_P: numpy.ndarray[numpy.float64[m, n]], transition_matrix_Q: numpy.ndarray[numpy.float64[m, n]], sample_path_from_R: numpy.ndarray[numpy.uint32[m, 1]], mixing_time_of_R_estimate_as_a_percentage_of_time_horizon: float = 0.1, confidence_level: float = 0.95, time_horizon: int = -1) -> dict[int, tuple[float, float]]:
    """
    If R is the ground truth (which generated the sample path) and P and Q are your models, then this calculates ( KL(R;Q) - KL(R;P) ) / window for various window sizes.
    """
def compute_bmcs_parameters(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]], order_of_bmc: int = 1, verbose: bool = False) -> tuple[numpy.ndarray[numpy.float64[m, 1]], numpy.ndarray[numpy.float64[m, 1]], numpy.ndarray[numpy.float64[m, n]]]:
    """
    Estimates the parameters of a Block Markov Chain.
    """
def compute_cluster_difference(assignment_a: numpy.ndarray[numpy.uint32[m, 1]], assignment_b: numpy.ndarray[numpy.uint32[m, 1]]) -> int:
    """
    Computes the difference between two clusters.
    """
def compute_cluster_improvement(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]], max_iterations: int, order_of_bmc: int = 1, verbose: bool = False) -> numpy.ndarray[numpy.uint32[m, 1]]:
    """
    Executes the cluster improvement algorithm.
    """
def compute_clusters_from_trajectory(trajectory: numpy.ndarray[numpy.uint32[m, 1]], num_states: int, num_clusters: int, seed: int = 1987, max_trials: int = 10000, max_iterations: int = 1000, num_largest_singular_values_to_ignore: int = 0, num_extra_singular_values_to_use: int = 0, order_of_bmc: int = 1, preferred_hardware: PreferredHardware, verbose: bool = False) -> numpy.ndarray[numpy.uint32[m, 1]]:
    """
    Compute the clusters from a trajectory. This function does the spectral clustering algorithm as well as the cluster improvement algorithm.
    """
def compute_equilibrium_distribution_lift(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int) -> numpy.ndarray[numpy.float64[m, 1]]:
    """
    Returns the lifted equilibrium distribution of a Block Markov Chain.
    """
def compute_frequency_matrix_lift(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int) -> numpy.ndarray[numpy.float64[m, n]]:
    """
    Returns a BMCs lifted frequency matrix.
    """
def compute_k_means(matrix: numpy.ndarray[numpy.float64[m, n]], num_clusters: int, seed: int = 1987, max_trials: int = 10000, max_iterations: int = 1000, preferred_hardware: PreferredHardware, verbose: bool = False) -> numpy.ndarray[numpy.uint32[m, 1]]:
    """
    A C++ implementation to compute a K-means assignment.
    """
def compute_spectral_clustering(matrix: numpy.ndarray[numpy.float64[m, n]], num_clusters: int, seed: int = 1987, max_trials: int = 10000, max_iterations: int = 1000, num_largest_singular_values_to_ignore: int = 0, num_extra_singular_values_to_use: int = 0, verbose: bool = False) -> numpy.ndarray[numpy.uint32[m, 1]]:
    """
    Execute the spectral clustering algorithm.
    """
def compute_spectral_norm(matrix: numpy.ndarray[numpy.float64[m, n]], method: SingularValueCalculationMethod) -> float:
    """
    Compute a spectral norm.
    """
def compute_transition_matrix_lift(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int) -> numpy.ndarray[numpy.float64[m, n]]:
    """
    Returns the lifted transition matrix of a Block Markov Chain.
    """
def generate_sample_path(transition_matrix: numpy.ndarray[numpy.float64[m, n]], rel_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int, trajectory_length: int, seed: int) -> numpy.ndarray[numpy.uint32[1, n]]:
    """
    Generate a random sample path of a Block Markov Chain.
    """
def generate_trimmed_matrix(transition_matrix: numpy.ndarray[numpy.float64[m, n]], rel_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int, trajectory_length: int, num_states_to_trim: int, seed: int) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Generate a random trimmed frequency matrix of a Block Markov Chain.
    """
def get_equilibrium_distribution_proj(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int) -> numpy.ndarray[numpy.float64[m, 1]]:
    """
    Returns the projected equilibrium distribution of a Block Markov Chain.
    """
def get_frequency_matrix_proj(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int) -> numpy.ndarray[numpy.float64[m, n]]:
    """
    Returns the projected frequency matrix of a Block Markov Chain.
    """
def get_limiting_singular_value_distribution_of_frequency_matrix(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int, x_values: list[float], trajectory_length: int, num_iterations: int = 50, epsilon: float = 1e-08) -> dict[float, float]:
    """
    Returns the limiting singular value distribution of the frequency matrix of a Block Markov Chain.
    """
def get_transition_matrix_proj(transition_matrix: numpy.ndarray[numpy.float64[m, n]], relative_sizes: numpy.ndarray[numpy.float64[m, 1]], abs_size: int) -> numpy.ndarray[numpy.float64[m, n]]:
    """
    Returns the projected transition matrix of a Block Markov Chain.
    """
def label_clusters(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]], method: ClusterSortingMethod) -> numpy.ndarray[numpy.uint32[m, 1]]:
    """
    Relabels a cluster assignment.
    """
def label_clusters_by_decr_equilibrium_distribution(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]]) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Relabels a cluster assignment by increasing equilibrium distribution.
    """
def label_clusters_by_decr_size(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]]) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Relabels a cluster assignment by increasing cluster size.
    """
def label_clusters_by_incr_equilibrium_distribution(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]]) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Relabels a cluster assignment by increasing equilibrium distribution.
    """
def label_clusters_by_incr_size(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]]) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Relabels a cluster assignment by increasing cluster size.
    """
def order_selection_by_minimizing_information_criteria(low_dim_sample_path: numpy.ndarray[numpy.uint32[m, 1]], max_order: int = 3, verbose: bool = False) -> None:
    """
    Returns log-likelihoods, AICs, BICs, and CAICs for Markov chains of different orders.
    """
def project_sample_path(sample_path_proj: numpy.ndarray[numpy.uint32[m, 1]], cluster_assignment: numpy.ndarray[numpy.uint32[m, 1]]) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Project a sample path based on a cluster assignment
    """
def trim_frequency_matrix(frequency_matrix: numpy.ndarray[numpy.uint32[m, n]], num_states_to_trim: int) -> numpy.ndarray[numpy.uint32[m, n]]:
    """
    Zeroes out a desired number of rows and columns corresponding to the most-visited states.
    """
__version__: str = 'dev'
