#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
"""Usage: driftie.py NAME 
    [-t T] 
    [-p P]
    [-d D]
    [-q Q]
    [--dt DT]
    [--seed SEED]
    [--min_P MP]
    [--sigma SIGMA]

Wilcon-Cowan EI model, where the oscillation frequency drifts
with time.

    Arguments
        NAME        name of the results file

    Options:
        -h help     show this screen
        -t T        simultation run time [default: 3.0]
        -p P        E drive at burst [default: 2]
        -d D        drive drift term [default: 0.1]
        -q Q        avg I drive  [default: 1]
        --dt DT     time resolution [default: 1e-3]
        --seed SEED random seed
        --min_P MP  smallest P possible [default: 1]
        --sigma SIGMA  Population noise [default: 1e-2]
"""
from __future__ import division, print_function

from docopt import docopt
import numpy as np
from pykdf.kdf import save_kdf

from brian2 import *
from fakespikes import rates


def ie(t,
       P,
       drift,
       c1=15.0,
       c2=15.0,
       c3=15.0,
       c4=3.0,
       Q=1,
       dt=1e-3,
       min_P=1,
       sigma=0.01):
    # --
    time = t * second
    time_step = dt * second

    # -
    # Fixed parameters.
    re = 1.0
    ri = 0.5

    kn = 1.0
    k = 1.0

    tau_e = 5 * msecond
    tau_i = 10 * msecond

    # -
    # Define the drifting drive
    times = rates.create_times(t, dt)
    P = rates.stim(times, P, drift)
    P[P < min_P] = min_P

    # Scale it
    P = P * (2** -0.03)

    # Format for Brian2
    P = TimedArray(P, dt=time_step)

    # -
    eqs = """
            dE/dt = -E/tau_e + ((1 - re * E) * (1 / (1 + exp(-(k * c1 * E - k * c2 * I+ k * P(t) - 2))) - 1/(1 + exp(2*1.0)))) / tau_e  + (sigma / tau_e**.5 * xi_e) : 1
            dI/dt = -I/tau_i + ((1 - ri * I) * (1 / (1 + exp(-2 * (kn * c3 * E - kn * c4 * I + kn * Q - 2.5))) - 1/(1 + exp(2*2.5)))) / tau_i + (sigma / tau_i**.5 * xi_i) : 1
        """

    pops = NeuronGroup(1, model=eqs, namespace={'Q': Q})
    pops.E = 0
    pops.I = 0

    # --
    # Record
    mon = StateMonitor(pops, ('E', 'I'), record=True)

    # --
    # Run
    defaultclock.dt = time_step
    run(time)

    return mon.I.flatten(), mon.E.flatten()


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
    t = float(args['-t'])
    dt = float(args['--dt'])

    P = float(args['-p'])
    d = float(args['-d'])
    if d < 0:
        raise ValueError("d must > 0.")

    Q = float(args['-q'])
    min_P = float(args['--min_P'])

    sigma = float(args['--sigma'])

    # -
    # Run model
    I, E = ie(t, P, d, min_P=min_P, sigma=sigma)
    lfp = (E + I)

    # -
    save_kdf(
        str(args['NAME']),
        E=E,
        I=I,
        lfp=lfp,
        t=t,
        dt=dt,
        P=P,
        Q=Q,
        d=d,
        sigma=sigma)
