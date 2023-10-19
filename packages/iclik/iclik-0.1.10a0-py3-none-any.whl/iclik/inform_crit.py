import numpy as np
from iclik.matrices import jacobian, hessian
import warnings


def _make_matrices(f, estimates, step, step_factor):
     jac = jacobian(f, estimates, step, step_factor)
     hess = hessian(f, estimates, step, step_factor)

     return jac, hess


def _cl_akaike(likelihood, jacobian_mat, hessian_mat):
    """Compute CLAIC from matrices."""
    return (-2 * likelihood 
            + 2 * np.trace(jacobian_mat @ np.linalg.inv(hessian_mat)))


def _cl_bayes(likelihood, jacobian_mat, hessian_mat, n_samples):
    """Compute CLBIC from matrices."""
    return (-2 * likelihood
            + np.log(n_samples)
            * np.trace(jacobian_mat @ np.linalg.inv(hessian_mat)))


def _detect_zeros(estimates, response="warn"):
    """Detect whether array of parameter estimates contains zeros."""
    if (estimates <= 0).any():
        if response=="error":
            raise ValueError("Zero or negative values detected")
        elif response=="warn":
            warnings.warn("Zeros or negative values detected in input - information criterion cannot be calculated", UserWarning)
        else:
             raise ValueError("Invalid setting {response} for response parameter, must be one of {'warn', 'error'}")


def _detect_nan_inf(estimates, response="warn"):
    """Detect whether array of parameter estimates contains NaN/inf."""
    if not (np.isfinite(estimates)).all():
        if response=="error":
            raise ValueError("Zero or negative values detected")
        elif response=="warn":
            warnings.warn("NaNs or Infs detected in input - information criterion cannot be calculated", UserWarning)
        else:
             raise ValueError("Invalid setting {response} for response parameter, must be one of {'warn', 'error'}")


def claic(f, estimates, step=1e-2, step_factor=0.5, zeros="allow", nan_infs="error"):
    """Compute composite likelihood Akaike information criterion (CLAIC).

    Args:
        f (function): Composite log-likelihood function.
        estimates (ndarray): Parameter estimates at which to evaluate CLAIC.
        step (float): Step size for finding Hessian and Jacobian matrices. Defaults to 1e-2.
        step_factor (float): Factor by which to multiply the step size in each attempt. Defaults to 0.5.
        zeros (str, optional): What to do with zeros in input, one of {"allow", "warn", "error"}. Defaults to "allow".
        nan_infs (str, optional): What to do with NaNs and infs in input, one of {"allow", "warn", "error"}. Defaults to "error".

    Returns:
        float: Composite likelihood AIC estimate.
    """
    if nan_infs != "allow":
        _detect_nan_inf(estimates, response=nan_infs)
    if zeros != "allow":
        _detect_zeros(estimates, response=zeros)

    likelihood = f(estimates)
    jacobian_mat, hessian_mat = _make_matrices(f, estimates, step, step_factor)
    return _cl_akaike(likelihood, jacobian_mat, hessian_mat)


def clbic(f, estimates, n_samples, step=1e-2, step_factor=0.5, zeros="allow", nan_infs="error"):
    """Compute composite likelihood Bayesian information criterion (CLBIC).

    Args:
        f (function): Composite log-likelihood function.
        estimates (ndarray): Parameter estimates at which to evaluate CLBIC.
        n_samples (int): Number of samples in data.
        step (float): Step size for finding Hessian and Jacobian matrices. Defaults to 1e-2.
        step_factor (float): Factor by which to multiply the step size in each attempt. Defaults to 0.5.
        zeros (str, optional): What to do with zeros in input, one of {"allow", "warn", "error"}. Defaults to "allow".
        nan_infs (str, optional): What to do with NaNs and infs in input, one of {"allow", "warn", "error"}. Defaults to "error".

    Returns:
        float: Composite likelihood BIC estimate.
    """
    if nan_infs != "allow":
        _detect_nan_inf(estimates, response=nan_infs)
    if zeros != "allow":
        _detect_zeros(estimates, response=zeros)

    likelihood = f(estimates)
    jacobian_mat, hessian_mat = _make_matrices(f, estimates, step, step_factor)
    return _cl_bayes(likelihood, jacobian_mat, hessian_mat, n_samples)














