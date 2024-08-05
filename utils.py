from typing import Literal

import numpy as np
from astropy import constants as const  # type: ignore
from astropy import units as u  # type: ignore

ENERGY_LOSS_NORM = (8 * np.pi * const.e.gauss**4) / (3 * const.m_e**2 * const.c**3)
ENERGY_LOSS_SCALE_IC = 4 * np.pi / 3


def energy_loss_rate(
    proc: Literal["synch", "ic"],
    U: u.Quantity[u.eV / u.cm**3],
    E: u.Quantity[u.eV],
    ultrarel_approx: bool = False,
) -> u.Quantity:
    """See ex.3 for details"""
    scale = 1 if proc == "synch" else ENERGY_LOSS_SCALE_IC
    subtract = 0 if ultrarel_approx else 1
    return (
        ENERGY_LOSS_NORM * scale * U * ((E / (const.m_e * const.c**2)) ** 2 - subtract)
    )


def black_body_energy_density(T: u.Quantity[u.K]) -> u.Quantity[u.eV / u.cm**3]:
    return (const.sigma_sb * (T**4) / const.c).to(u.eV / u.cm**3)


# Gaussian units magnetic field, defined not as 10^-4 T, but in true CGS
gauss_cgs = u.def_unit(
    ["gauss_cgs", "G_cgs"],
    u.cm ** (-1 / 2) * u.g ** (1 / 2) * u.s ** (-1),
    format={"latex": r"G"},
    prefixes=True,
)


def bohm_diffusion_coeff(
    E: u.Quantity[u.eV], B: u.Quantity[gauss_cgs]
) -> u.Quantity[u.pc**2 / u.Gyr]:
    return (
        const.c
        * (1 / 3)
        * np.sqrt(E**2 - (const.m_e * const.c**2) ** 2)
        / (const.e.gauss * B)
    ).to(u.pc**2 / u.Gyr)


T_CMB = 2.725 * u.K


def clamp_mod(
    v: np.ndarray, min: float, period: float
) -> tuple[np.ndarray, np.ndarray]:
    v_shifted = v - min
    return (min + (v_shifted) % period, v_shifted // period)
