#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
"""Usage: mixie.py NAME 
    [-t T] 
    [-n N]  
    [-p P]
    [-q Q]
    [-s S]
    [--seed SEED]
    [--dt DT]
    [--sigma SIGMA]

Wilcon-Cowan EI model.

    Arguments
        NAME        name of the results file

    Options:
        -h help     show this screen
        -t T        simultation run time [default: 3.0]
        -n N        number of populations [default: 10]
        -p P        Avg E drive  [default: 2]
        -q Q        Avg I drive  [default: 1]
        -s S        Std dev of drive variations [default: 0.1]
        --seed SEED random seed 
        --dt DT     time resolution [default: 1e-3]
        --sigma SIGMA  Population noise [default: 1e-2]
"""
from __future__ import division, print_function

from docopt import docopt
import numpy as np
from pykdf.kdf import save_kdf

from brian2 import *


# P=1, Q=3
def _ie(t, P, Q, c1, c2, c3, c4, dt=1e-3, sigma=0.01):
    # --
    time = t * second
    time_step = dt * second

    # Fixed parameters.
    re = 1.0
    ri = 0.5

    kn = 1.0
    k = 1.0

    tau_e = 5 * msecond
    tau_i = 10 * msecond

    P = P * (2** -0.03)

    eqs = """
    dE/dt = -E/tau_e + ((1 - re * E) * (1 / (1 + exp(-(k * c1 * E - k * c2 * I+ k* P - 2))) - 1/(1 + exp(2*1.0)))) / tau_e + (sigma / tau_e**.5 * xi_e) : 1
    dI/dt = -I/tau_i + ((1 - ri * I) * (1 / (1 + exp(-2 * (kn * c3 * E - kn * c4 * I + kn * Q - 2.5))) - 1/(1 + exp(2*2.5)))) / tau_i + (sigma / tau_i**.5 * xi_i) : 1
    # P : 1 (constant)
    # Q : 1 (constant)
    """

    pops = NeuronGroup(1, model=eqs, namespace={'Q': Q, 'P': P})
    pops.E = 0
    pops.I = 0

    # --
    # Record
    mon = StateMonitor(pops, ('E', 'I'), record=True)

    # --
    # Run
    defaultclock.dt = time_step
    run(time)

    return mon.I, mon.E


def ie(t, Ps, Qs, N, c1=15.0, c2=15.0, c3=15.0, c4=3.0, dt=1e-3, sigma=0.01):
    if len(Ps) != N:
        raise ValueError("Ps must have a len of {}".format(N))
    if len(Qs) != N:
        raise ValueError("Qs must have a len of {}".format(N))

    E, I = [], []
    for n, (p, q) in enumerate(zip(Ps, Qs)):
        i, e = _ie(t, p, q, c1, c2, c3, c4, dt, sigma)
        E.append(e)
        I.append(i)

    E = np.vstack(E).mean(0)
    I = np.vstack(I).mean(0)

    return I, E


if __name__ == "__main__":
    args = docopt(__doc__, version='alpha')

    try:
        seed = int(args['--seed'])
    except TypeError:
        seed = None
        pass
    np.random.seed(seed)

    # -
    # Process params
    N = int(args['-n'])
    if N < 2:
        raise ValueError("N must be > 2.")

    t = float(args['-t'])
    dt = float(args['--dt'])

    P = float(args['-p'])
    Q = float(args['-q'])
    s = float(args['-s'])

    if np.allclose(s, 0):
        Ps = np.repeat(P, N)
        Qs = np.repeat(Q, N)
    else:
        Ps = np.random.normal(P, P * s, size=N)
        Qs = np.random.normal(Q, Q * s, size=N)

    sigma = float(args['--sigma'])

    # -
    I, E = ie(t, Ps, Qs, N, dt=dt, sigma=sigma)
    lfp = (E + I)

    # -
    save_kdf(
        str(args['NAME']),
        N=N,
        E=E,
        I=I,
        lfp=lfp,
        t=t,
        dt=dt,
        sigma=sigma,
        Ps=Ps,
        Qs=Qs)
