"""
Collection of physical constants and conversion factors.

Most constants are in SI units, so you can do
print '10 mile per minute is', 10*mile/minute, 'm/s or', 10*mile/(minute*knot), 'knots'

The list is not meant to be comprehensive, but just a convenient list for everyday use.
"""
from __future__ import division, print_function, absolute_import

"""
BasSw 2006
physical constants: imported from CODATA
unit conversion: see e.g. NIST special publication 811
Use at own risk: double-check values before calculating your Mars orbit-insertion burn.
Some constants exist in a few variants, which are marked with suffixes.
The ones without any suffix should be the most common one.
"""

import math as _math
from .codata import value as _cd
import numpy as _np

# mathematical constants
pi = _math.pi
golden = golden_ratio = (1 + _math.sqrt(5)) / 2

# SI prefixes
yotta = 1e24
zetta = 1e21
exa = 1e18
peta = 1e15
tera = 1e12
giga = 1e9
mega = 1e6
kilo = 1e3
hecto = 1e2
deka = 1e1
deci = 1e-1
centi = 1e-2
milli = 1e-3
micro = 1e-6
nano = 1e-9
pico = 1e-12
femto = 1e-15
atto = 1e-18
zepto = 1e-21

# binary prefixes
kibi = 2**10
mebi = 2**20
gibi = 2**30
tebi = 2**40
pebi = 2**50
exbi = 2**60
zebi = 2**70
yobi = 2**80

# physical constants
c = speed_of_light = _cd('speed of light in vacuum')
mu_0 = 4e-7*pi
epsilon_0 = 1 / (mu_0*c*c)
h = Planck = _cd('Planck constant')
hbar = h / (2 * pi)
G = gravitational_constant = _cd('Newtonian constant of gravitation')
g = _cd('standard acceleration of gravity')
e = elementary_charge = _cd('elementary charge')
R = gas_constant = _cd('molar gas constant')
alpha = fine_structure = _cd('fine-structure constant')
N_A = Avogadro = _cd('Avogadro constant')
k = Boltzmann = _cd('Boltzmann constant')
sigma = Stefan_Boltzmann = _cd('Stefan-Boltzmann constant')
Wien = _cd('Wien wavelength displacement law constant')
Rydberg = _cd('Rydberg constant')

# weight in kg
gram = 1e-3
metric_ton = 1e3
grain = 64.79891e-6
lb = pound = 7000 * grain  # avoirdupois
oz = ounce = pound / 16
stone = 14 * pound
long_ton = 2240 * pound
short_ton = 2000 * pound

troy_ounce = 480 * grain  # only for metals / gems
troy_pound = 12 * troy_ounce
carat = 200e-6

m_e = electron_mass = _cd('electron mass')
m_p = proton_mass = _cd('proton mass')
m_n = neutron_mass = _cd('neutron mass')
m_u = u = atomic_mass = _cd('atomic mass constant')

# angle in rad
degree = pi / 180
arcmin = arcminute = degree / 60
arcsec = arcsecond = arcmin / 60

# time in second
minute = 60.0
hour = 60 * minute
day = 24 * hour
week = 7 * day
year = 365 * day
Julian_year = 365.25 * day

# length in meter
inch = 0.0254
foot = 12 * inch
yard = 3 * foot
mile = 1760 * yard
mil = inch / 1000
pt = point = inch / 72  # typography
survey_foot = 1200.0 / 3937
survey_mile = 5280 * survey_foot
nautical_mile = 1852.0
fermi = 1e-15
angstrom = 1e-10
micron = 1e-6
au = astronomical_unit = 149597870691.0
light_year = Julian_year * c
parsec = au / arcsec

# pressure in pascal
atm = atmosphere = _cd('standard atmosphere')
bar = 1e5
torr = mmHg = atm / 760
psi = pound * g / (inch * inch)

# area in meter**2
hectare = 1e4
acre = 43560 * foot**2

# volume in meter**3
litre = liter = 1e-3
gallon = gallon_US = 231 * inch**3  # US
# pint = gallon_US / 8
fluid_ounce = fluid_ounce_US = gallon_US / 128
bbl = barrel = 42 * gallon_US  # for oil

gallon_imp = 4.54609e-3  # uk
fluid_ounce_imp = gallon_imp / 160

# speed in meter per second
kmh = 1e3 / hour
mph = mile / hour
mach = speed_of_sound = 340.5  # approx value at 15 degrees in 1 atm. is this a common value?
knot = nautical_mile / hour

# temperature in kelvin
zero_Celsius = 273.15
degree_Fahrenheit = 1/1.8  # only for differences

# energy in joule
eV = electron_volt = elementary_charge  # * 1 Volt
calorie = calorie_th = 4.184
calorie_IT = 4.1868
erg = 1e-7
Btu_th = pound * degree_Fahrenheit * calorie_th / gram
Btu = Btu_IT = pound * degree_Fahrenheit * calorie_IT / gram
ton_TNT = 1e9 * calorie_th
# Wh = watt_hour

# power in watt
hp = horsepower = 550 * foot * pound * g

# force in newton
dyn = dyne = 1e-5
lbf = pound_force = pound * g
kgf = kilogram_force = g  # * 1 kg

# functions for conversions that are not linear


def C2K(C):
    """
    Convert Celsius to Kelvin

    Parameters
    ----------
    C : array_like
        Celsius temperature(s) to be converted.

    Returns
    -------
    K : float or array of floats
        Equivalent Kelvin temperature(s).

    Notes
    -----
    Computes ``K = C + zero_Celsius`` where `zero_Celsius` = 273.15, i.e.,
    (the absolute value of) temperature "absolute zero" as measured in Celsius.

    Examples
    --------
    >>> from scipy.constants.constants import C2K
    >>> C2K(_np.array([-40, 40.0]))
    array([ 233.15,  313.15])

    """
    return _np.asanyarray(C) + zero_Celsius


def K2C(K):
    """
    Convert Kelvin to Celsius

    Parameters
    ----------
    K : array_like
        Kelvin temperature(s) to be converted.

    Returns
    -------
    C : float or array of floats
        Equivalent Celsius temperature(s).

    Notes
    -----
    Computes ``C = K - zero_Celsius`` where `zero_Celsius` = 273.15, i.e.,
    (the absolute value of) temperature "absolute zero" as measured in Celsius.

    Examples
    --------
    >>> from scipy.constants.constants import K2C
    >>> K2C(_np.array([233.15, 313.15]))
    array([-40.,  40.])

    """
    return _np.asanyarray(K) - zero_Celsius


def F2C(F):
    """
    Convert Fahrenheit to Celsius

    Parameters
    ----------
    F : array_like
        Fahrenheit temperature(s) to be converted.

    Returns
    -------
    C : float or array of floats
        Equivalent Celsius temperature(s).

    Notes
    -----
    Computes ``C = (F - 32) / 1.8``.

    Examples
    --------
    >>> from scipy.constants.constants import F2C
    >>> F2C(_np.array([-40, 40.0]))
    array([-40.        ,   4.44444444])

    """
    return (_np.asanyarray(F) - 32) / 1.8


def C2F(C):
    """
    Convert Celsius to Fahrenheit

    Parameters
    ----------
    C : array_like
        Celsius temperature(s) to be converted.

    Returns
    -------
    F : float or array of floats
        Equivalent Fahrenheit temperature(s).

    Notes
    -----
    Computes ``F = 1.8 * C + 32``.

    Examples
    --------
    >>> from scipy.constants.constants import C2F
    >>> C2F(_np.array([-40, 40.0]))
    array([ -40.,  104.])

    """
    return 1.8 * _np.asanyarray(C) + 32


def F2K(F):
    """
    Convert Fahrenheit to Kelvin

    Parameters
    ----------
    F : array_like
        Fahrenheit temperature(s) to be converted.

    Returns
    -------
    K : float or array of floats
        Equivalent Kelvin temperature(s).

    Notes
    -----
    Computes ``K = (F - 32)/1.8 + zero_Celsius`` where `zero_Celsius` =
    273.15, i.e., (the absolute value of) temperature "absolute zero" as
    measured in Celsius.

    Examples
    --------
    >>> from scipy.constants.constants import F2K
    >>> F2K(_np.array([-40, 104]))
    array([ 233.15,  313.15])

    """
    return C2K(F2C(_np.asanyarray(F)))


def K2F(K):
    """
    Convert Kelvin to Fahrenheit

    Parameters
    ----------
    K : array_like
        Kelvin temperature(s) to be converted.

    Returns
    -------
    F : float or array of floats
        Equivalent Fahrenheit temperature(s).

    Notes
    -----
    Computes ``F = 1.8 * (K - zero_Celsius) + 32`` where `zero_Celsius` =
    273.15, i.e., (the absolute value of) temperature "absolute zero" as
    measured in Celsius.

    Examples
    --------
    >>> from scipy.constants.constants import K2F
    >>> K2F(_np.array([233.15,  313.15]))
    array([ -40.,  104.])

    """
    return C2F(K2C(_np.asanyarray(K)))

# optics


def lambda2nu(lambda_):
    """
    Convert wavelength to optical frequency

    Parameters
    ----------
    lambda : array_like
        Wavelength(s) to be converted.

    Returns
    -------
    nu : float or array of floats
        Equivalent optical frequency.

    Notes
    -----
    Computes ``nu = c / lambda`` where c = 299792458.0, i.e., the
    (vacuum) speed of light in meters/second.

    Examples
    --------
    >>> from scipy.constants.constants import lambda2nu
    >>> lambda2nu(_np.array((1, speed_of_light)))
    array([  2.99792458e+08,   1.00000000e+00])

    """
    return _np.asanyarray(c) / lambda_


def nu2lambda(nu):
    """
    Convert optical frequency to wavelength.

    Parameters
    ----------
    nu : array_like
        Optical frequency to be converted.

    Returns
    -------
    lambda : float or array of floats
        Equivalent wavelength(s).

    Notes
    -----
    Computes ``lambda = c / nu`` where c = 299792458.0, i.e., the
    (vacuum) speed of light in meters/second.

    Examples
    --------
    >>> from scipy.constants.constants import nu2lambda
    >>> nu2lambda(_np.array((1, speed_of_light)))
    array([  2.99792458e+08,   1.00000000e+00])

    """
    return c / _np.asanyarray(nu)