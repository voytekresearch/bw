# bw
Toy simulations to try and better interpret peak bandwidth in power spectra. 

# usage

See the `Makefile` for experiments to date, as well as the `ipynb` folder.

# dependencies

- fakespikes: [https://github.com/voytekresearch/fakespikes]()
- brian2: [https://brian2.readthedocs.io/en/stable/]()
- numpy, scipy, etc (i.e. install conda).

# results

- Changes to drive (input), and 
- changes to oscillatory burst length probably have identifiable bw effects in real data.
- But the more interesting variations, where oscillator number changes
- or phase entrianment chages, don't have strong (or any) BW effects.
