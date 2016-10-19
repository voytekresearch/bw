#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
"""Usage: burstie.py NAME 
    [-t T] 
    [-n N]  
    [-p P]
    [-b B]
    [-w W]
    [-q Q]
    [-s S]
    [--dt DT]

Wilcon-Cowan EI model of oscillatory bursting.

    Arguments
        NAME        name of the results file

    Options:
        -h help     show this screen
        -t T        simultation run time [default: 3.0]
        -n N        number of populations [default: 1]
        -p P        E drive at burst [default: 2]
        -b B        burst onset time [default: 1]
        -w W        burst onset length [default: 0.1]
        -q Q        avg I drive  [default: 1]
        -s S        std dev of drive variations [default: 0.1]
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
    run(time, report='text')

    return mon.I, mon.E


if __name__ == "__main__":
    args = docopt(__doc__, version='alpha')
   
    # -
    # Process params
    N = int(args['-n'])

    t = float(args['-t'])
    dt = float(args['--dt'])
   
    P = float(args['-p'])

    t_burst = float(args['-b'])
    w = float(args['-w'])

    Q = float(args['-q'])
    Qs = np.repeat(Q, N)

    s = float(args['-s'])

    if np.allclose(s, 0):
        Ps = np.repeat(P, N)
        ws = np.repeat(w, N)
    else:
        Ps = np.random.normal(P, P * s, size=N)
        ws = np.random.normal(w, w * s, size=N)

    # Prevent negative time
    ws[ws < 0] = 0.0001

    # -
    # Run models
    E, I = [], []
    for n, (P, w) in enumerate(zip(Ps, ws)):

        i, e = ie(t, P, t_burst, w)

        E.append(e)
        I.append(i)

    E = np.vstack(E)
    I = np.vstack(I)

    lfp = (E + I).mean(0) 

    # -
    save_kdf(
            str(args['NAME']),
            N=N,
            E=E,
            I=I,
            lfp=lfp,
            t=t,
            dt=dt,
            Ps=Ps,
            Qs=Qs,
            ws=ws,
            s=s
        )
