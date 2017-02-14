"""Usage: kur.py NAME 
    [-t T] 
    [-n N]
    [-k K]
    [-o OMEGA]
    [-r OMEGA_RANGE]
    [-p PON]
    [--seed SEED]
    [--dt DT]
    [--sigma SIGMA]

Kuramoto model.

    Arguments
        NAME    name of results file

    Options:
        -h --help               show this screen
        -t T                    simultation run time [default: 3.0]
        -n N                    number of oscillators [default: 1000]
        -k K                    coupling (as fraction of N) [default: 6]
        -o OMEGA                center frequency [default: 10]
        -r OMEGA_RANGE          min/max of the center [default: 1]
        -p PON                  probability a ith oscillator is on [default: 1]
        --seed SEED             seed for creating the stimulus [default: 42]
        --dt DT                 time resolution [default: 1e-2]
        --sigma SIGMA  Population noise [default: 1e-2]
"""
from __future__ import division, print_function

from docopt import docopt
import numpy as np
from sdeint import itoint
from pykdf.kdf import save_kdf


# --
def kuramoto(theta, t, omega, K, N, sigma):
    # In classic kuramoto...

    # each oscillator gets the same wieght K
    # normalized by the number of oscillators
    c = K / N

    # and all oscillators are connected to all
    # oscillators
    theta = np.atleast_2d(theta)  # for broadcasting
    W = np.sum(np.sin(theta - theta.T), 1)

    # ep = np.random.normal(0, sigma, N)
    ep = np.random.normal(0, sigma, N)

    return omega + ep + (c * W)


def onoff(theta, t, omega, K, N, sigma, p):
    theta = kuramoto(theta, t, omega, K, N, sigma)

    return theta * np.random.binomial(1, p, size=N)


def simulate(theta0, T, omegas, K, N, sigma, p, dt):
    """Simulate a Kuramoto model."""

    times = np.linspace(0, T, int(T / dt))

    def G(_, t):
        return np.diag(np.ones(N) * sigma)

    if np.allclose(p, 1):

        def f(theta, t):
            return kuramoto(theta, t, omegas, K, N, sigma)
    else:

        def f(theta, t):
            return onoff(theta, t, omegas, K, N, sigma, p)

    thetas = itoint(f, G, theta0, times)
    thetas = np.mod(thetas, 2 * np.pi)
    thetas -= np.pi

    return thetas, times


if __name__ == "__main__":
    args = docopt(__doc__, version='alpha')

    try:
        seed = int(args['--seed'])
    except TypeError:
        seed = None
        pass
    np.random.seed(seed)

    # -
    # Network
    N = int(args['-n'])
    K = float(args['-k'])
    p = float(args['-p'])

    # Time
    T = float(args['-t'])
    dt = float(args['--dt'])

    # -
    # Init oscillators
    omega = float(args['-o'])

    # mean freq
    omega_range = float(args['-r'])

    a = omega - omega_range
    b = omega + omega_range
    if omega < 0:
        raise ValueError("The center frequency must be > 0.")
    if a < 0:
        raise ValueError("The center frequency must be > 0.")
    if b < 0:
        raise ValueError("The center frequency must be > 0.")

    sigma = float(args['--sigma'])

    # Init
    omegas = np.random.uniform(a, b, size=N)
    theta0 = np.random.uniform(-np.pi * 2, np.pi * 2, size=N)

    # -
    thetas, times = simulate(theta0, T, omegas, K, N, sigma, p, dt)

    # -
    # From the unit circle to sin waves, and the simulated lfp.
    waves = []
    for n in range(N):
        th = thetas[:, n]
        f = omegas[n]

        wave = np.sin(f * 2 * np.pi * times + th)
        waves.append(wave)

    waves = np.vstack(waves)
    lfp = waves.mean(0)

    # -
    save_kdf(
        str(args['NAME']),
        thetas=thetas,
        theta0=theta0,
        omegas=omegas,
        waves=waves,
        lfp=lfp,
        seed=seed,
        sigma=sigma,
        N=N,
        K=K,
        times=times,
        t=T,
        dt=dt)
