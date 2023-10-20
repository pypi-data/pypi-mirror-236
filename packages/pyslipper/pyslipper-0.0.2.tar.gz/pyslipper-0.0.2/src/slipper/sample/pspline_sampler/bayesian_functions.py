from collections import namedtuple
from typing import NamedTuple

import numpy as np
from bilby.core.prior import ConditionalPriorDict, Gamma

from slipper.splines.p_splines import PSplines

from ..utils import _xPx


class LnlArgs(NamedTuple):
    w: np.ndarray
    τ: float
    τα: float
    τβ: float
    φ: float
    φα: float
    φβ: float
    δ: float
    δα: float
    δβ: float
    data: np.ndarray
    spline_model: PSplines


def lprior(args: LnlArgs):
    φα, φβ, δα, δβ, τα, τβ = (
        args.φα,
        args.φβ,
        args.δα,
        args.δβ,
        args.τα,
        args.τβ,
    )
    φ, δ, τ = (args.φ, args.δ, args.τ)
    v = args.w
    k = args.spline_model.n_basis
    vTPv = _xPx(v, args.spline_model.penalty_matrix)
    logφ = np.log(φ)
    logδ = np.log(δ)
    logτ = np.log(τ)

    lnpri_weights = (k - 1) * logφ * 0.5 - φ * vTPv * 0.5
    lnpri_φ = φα * logδ + (φα - 1) * logφ - φβ * δ * φ
    lnpri_δ = (δα - 1) * logδ - δβ * δ
    lnpri_τ = -(τα + 1) * logτ - τβ / τ
    log_prior = lnpri_weights + lnpri_φ + lnpri_δ + lnpri_τ
    return log_prior


def __conditional_phi(k, v, P, φα, φβ, δ):
    vTPv = np.dot(np.dot(v.T, P), v)
    shape = (k - 1) / 2 + φα
    rate = φβ * δ + vTPv / 2
    return Gamma(k=shape, theta=1 / rate)


def __conditional_delta(φ, φα, φβ, δα, δβ):
    """Gamma prior for pi(δ|φ)"""
    shape = φα + δα
    rate = φβ * φ + δβ
    return Gamma(k=shape, theta=1 / rate)


def __conditional_tau(v, data, spline_model, τα, τβ):
    """Inverse(?) prior for tau -- tau = 1/inv_tau_sample"""

    n = len(data)
    _spline = spline_model(v=v, n=n)
    is_even = n % 2 == 0
    if is_even:
        spline_normed_data = data[1:-1] / _spline[1:-1]
    else:
        spline_normed_data = data[1:] / _spline[1:]

    n = len(spline_normed_data)

    shape = τα + n / 2
    rate = τβ + np.sum(spline_normed_data) / (2 * np.pi) / 2
    return Gamma(k=shape, theta=1 / rate)


def sample_φδτ(args: LnlArgs):
    v, φα, φβ, δα, δβ, τα, τβ, δ = (
        args.w,
        args.φα,
        args.φβ,
        args.δα,
        args.δβ,
        args.τα,
        args.τβ,
        args.δ,
    )
    spline_model = args.spline_model
    k = spline_model.n_basis
    data = args.data

    φ = (
        __conditional_phi(k, v, spline_model.penalty_matrix, φα, φβ, δ)
        .sample()
        .flat[0]
    )
    δ = __conditional_delta(φ, φα, φβ, δα, δβ).sample().flat[0]
    τ = 1 / __conditional_tau(v, data, spline_model, τα, τβ).sample()
    return φ, δ, τ


def lpost(args: LnlArgs):
    v, τ, data, spline_model = (
        args.w,
        args.τ,
        args.data,
        args.spline_model,
    )
    logprior = lprior(args)
    loglike = spline_model.lnlikelihood(data=data, v=v, τ=τ)
    logpost = logprior + loglike
    if not np.isfinite(logpost):
        raise ValueError(
            f"logpost is not finite: lnpri{logprior}, lnlike{loglike}, lnpost{logpost}"
        )

    return logpost
