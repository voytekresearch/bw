"""Usage: kur.py NAME 
    [-t T] 
    [-n N]
    [-k K]
    [-o OMEGA]
    [-r OMEGA_RANGE]
    [--seed SEED]
    [--dt DT]

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

        --seed SEED             seed for creating the stimulus [default: 42]
        --dt DT                 time resolution [default: 1e-2]
"""
from __future__ import division, print_function

from docopt import docopt
import numpy as np
from scipy.integrate import odeint
from pykdf.kdf import save_kdf


# --
def kuramoto(theta, t, omega, K, N):
    # In classic kuramoto...

    # each oscillator gets the same wieght K
    # normalized by the number of oscillators
    c = K / N

    # and all oscillators are connected to all
    # oscillators
    theta = np.atleast_2d(theta)  # for broadcasting
    W = np.sum(
            np.sin(theta - theta.T), 1
        )

    return omega + c * W


def simulate(theta0, times, omegas, K, N):
    """Simulate a Kuramoto model."""

    thetas = odeint(kuramoto, theta0, times, args=(omegas, K, N))
    thetas = np.mod(thetas, 2 * np.pi)
    thetas -= np.pi

    return thetas


if __name__ == "__main__":
    args = docopt(__doc__, version='alpha')

    seed = int(args['--seed'])
    np.random.seed(seed)

    # -
    # Network
    N = int(args['-n'])
    K = float(args['-k'])

    # Time
    T = float(args['-t'])
    dt = float(args['--dt'])
    times = np.linspace(0, T, int(T / dt))

    # -
    # Init oscillators
    omega = float(args['-o']); # mean freq
    omega_range = float(args['-r'])

    a = omega - omega_range
    b = omega + omega_range
    if omega < 0:
        raise ValueError("The center frequency must be > 0.")
    if a < 0:
        raise ValueError("The center frequency must be > 0.")
    if b < 0:
        raise ValueError("The center frequency must be > 0.")

    # Init
    omegas = np.random.uniform(a, b, size=N)
    theta0 = np.random.uniform(-np.pi * 2, np.pi * 2, size=N)  

    # -
    thetas = simulate(theta0, times, omegas, K, N)

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
            N=N, 
            K=K, 
            times=times
        )
