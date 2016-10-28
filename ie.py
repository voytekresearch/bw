#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
"""Usage: ie.py NAME 
    [-t T] 
    [-p P]
    [-q Q]
    [-s S]
    [--dt DT]

Wilcon-Cowan EI model.

    Arguments
        NAME        name of the results file

    Options:
        -h help     show this screen
        -t T        simultation run time [default: 3.0]
        -p P        E drive  [default: 2]
        -q Q        I drive  [default: 1]
        -s S        std dev of drive variations [default: 0.1]
        --dt DT     time resolution [default: 1e-3]
"""
from __future__ import division, print_function

from docopt import docopt
import numpy as np
from pykdf.kdf import save_kdf

from brian2 import *


# P=1, Q=3
def ie(t, P, Q, c1=15.0, c2=15.0, c3=15.0, c4=3.0, dt=1e-3):
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

    P = P * (2**-0.03) 

    eqs = """
            dE/dt = -E/tau_e + ((1 - re * E) * (1 / (1 + exp(-(k * c1 * E - k * c2 * I+ k* P - 2))) - 1/(1 + exp(2*1.0)))) / tau_e : 1
            dI/dt = -I/tau_i + ((1 - ri * I) * (1 / (1 + exp(-2 * (kn * c3 * E - kn * c4 * I + kn * Q - 2.5))) - 1/(1 + exp(2*2.5)))) / tau_i : 1
            # P : 1 (constant)
            # Q : 1 (constant)
        """

    pops = NeuronGroup(1, model=eqs, namespace={'Q' : Q, 'P': P})
    pops.E = 0
    pops.I = 0

    # --
    # Record
    mon = StateMonitor(pops, ('E', 'I'), record=True)

    # --
    # Run
    defaultclock.dt = time_step
    run(time, report='text')

    return mon.I.flatten(), mon.E.flatten()



if __name__ == "__main__":
    args = docopt(__doc__, version='alpha')
   
    # -
    # Process params
    t = float(args['-t'])
    dt = float(args['--dt'])
   
    P = float(args['-p'])
    Q = float(args['-q'])

    # -
    I, E = ie(t, P, Q, dt=dt)

    lfp = E + I

    # -
    save_kdf(
            str(args['NAME']),
            E=E,
            I=I,
            lfp=lfp,
            t=t,
            dt=dt,
            P=P,
            Q=Q
        )
