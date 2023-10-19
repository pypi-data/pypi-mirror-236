import numpy as np
import numdifftools as nd


def hessian(f, estimates, step, step_factor):
    """Calculate Hessian by iteratively changing step size until all elements are finite.

    Args:
        f (function): Composite log likelihood function.
        estimates (ndarray): Parameter estimates at which to evaluate.
        initial_step (float): Initial step size for calculations.
        step_factor (float): Factor to multiply step size by at each iteration.

    Returns:
        ndarray: Hessian matrix.
    """
    hess_f = nd.core.Hessian(f, step=step)
    hess_mat = hess_f(np.array(estimates))
    if not (np.isfinite(hess_mat)).all():
            step = step * step_factor
            hess_mat = hessian(f, estimates, step=step, step_factor=step_factor)

    return hess_mat


def jacobian(f, estimates, step, step_factor):
    """Calculate Jacobian by iteratively changing step size until all elements are finite.

    Args:
        f (function): Composite log likelihood function.
        estimates (ndarray): Parameter estimates at which to evaluate.
        initial_step (float): Initial step size for calculations.
        step_factor (float): Factor to multiply step size by at each iteration.

    Returns:
        ndarray: Jacobian matrix.
    """
    jac_f = nd.core.Jacobian(f, step=step)
    jac_mat = jac_f(np.array(estimates))
    if not (np.isfinite(jac_mat)).all():
            step = step * step_factor
            jac_mat = jacobian(f, estimates, step=step, step_factor=step_factor)

    return jac_mat