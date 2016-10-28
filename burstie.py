#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
"""Usage: burstie.py NAME 
    [-t T] 
    [-p P]
    [-b B]
    [-w W]
    [-q Q]
    [-s S]
    [--seed SEED]
    [--dt DT]

Wilcon-Cowan EI model of oscillatory bursting.

    Arguments
        NAME        name of the results file

    Options:
        -h help     show this screen
        -t T        simultation run time [default: 3.0]
        -p P        E drive at burst [default: 2]
        -b B        burst onset time [default: 1]
        -w W        burst onset length [default: 0.1]
        -q Q        avg I drive  [default: 1]
        -s S        std dev of drive variations [default: 0.1]
        --seed SEED random seed
        --dt DT     time resolution [default: 1e-3]
"""
from __future__ import division, print_function

from docopt import docopt
import numpy as np
from pykdf.kdf import save_kdf

from brian2 import *
from fakespikes import rates


def ie(t, P, t_burst, w, c1=15.0, c2=15.0, c3=15.0, c4=3.0, Q=1, dt=1e-3, min_P=0):
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
    # Define the burst, as part of the drive to E, i.e, variable P.
    times = rates.create_times(t, dt)
    P = rates.square_pulse(times, P, t_burst, w, dt, min_a=min_P)

    # Scale it
    P = P * (2**-0.03) 

    # Format for Brian2
    P = TimedArray(P, dt=time_step)

    # -
    eqs = """
            dE/dt = -E/tau_e + ((1 - re * E) * (1 / (1 + exp(-(k * c1 * E - k * c2 * I+ k * P(t) - 2))) - 1/(1 + exp(2*1.0)))) / tau_e : 1
            dI/dt = -I/tau_i + ((1 - ri * I) * (1 / (1 + exp(-2 * (kn * c3 * E - kn * c4 * I + kn * Q - 2.5))) - 1/(1 + exp(2*2.5)))) / tau_i : 1
        """

    pops = NeuronGroup(1, model=eqs, namespace={'Q' : Q})
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
   

    t_burst = float(args['-b'])
    w = float(args['-w'])

    Q = float(args['-q'])
    P = float(args['-p'])
    s = float(args['-s'])

    # Only add noise to the window length
    if not np.allclose(s, 0):
        w = np.random.normal(w, w * s, size=1)
        # Prevent negative time
        if w < 0:
            w = 0.0001 

    # -
    # Run model
    I, E = ie(t, P, t_burst, w)
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
            w=w,
            s=s
        )
