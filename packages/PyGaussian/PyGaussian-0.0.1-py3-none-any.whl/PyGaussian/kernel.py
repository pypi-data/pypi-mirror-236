from typing import Any
from abc import ABC, abstractmethod
import numpy as np
import math


class Kernel(ABC):
    """ Abstract class representing a Kernel function for the Gaussian Process. """

    @abstractmethod
    def __call__(self, X1: np.ndarray, X2: np.ndarray) -> float:
        pass

    @staticmethod
    @abstractmethod
    def get_hps() -> dict[str, Any]:
        """
        Returns:
            dict[str, Any]: dictionary, where
                - key := name of hyperparameter
                - value := type of hyperparameter
        """
        pass


class GaussianKernel(Kernel):
    """ Class representing the quadratic exponential kernel (gaussian kernel) for the Gaussian Process. """

    def __init__(self, length: float):
        self.length_scale = length

    def __call__(self, X1: np.ndarray, X2: np.ndarray) -> float:
        """
        Calculates the covariance function K(X1, X2) between X1 and X2, after the gaussian kernel function:
            - K(X1, X2) = exp(-||X1 - X2||^2 / (2 * σ^2))

        Args:
            X1 (np.ndarray): first data point
            X2 (np.ndarray): second data point

        Returns:
            float: result of the covariance function K(X1, X2)
        """
        return np.exp(-(np.linalg.norm(X1 - X2) ** 2) / (2 * self.length_scale ** 2))

    @staticmethod
    def get_hps() -> dict[str, Any]:
        return {
            "length": float,
        }

# TODO: Implement more Kernel Functions: https://en.wikipedia.org/wiki/Gaussian_process
