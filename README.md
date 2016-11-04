# bw
Toy simulations to try and better interpret peak bandwidth in power spectra. 

# usage

See the `Makefile` for experiments to date, as well as the `ipynb` folder.

# dependencies

- fakespikes: [https://github.com/voytekresearch/fakespikes]()
- brian2: [https://brian2.readthedocs.io/en/stable/]()
- numpy, scipy, etc (i.e. install conda).
- to run the experiments in the `Makefile` you'll also need gnu parallel: [https://www.gnu.org/software/parallel/]()

# results

- Changes to drive (input), and 
- changes to oscillatory burst length probably have identifiable bw effects in real data.
- But the more interesting variations, where oscillator number changes
- or phase entrianment chages, don't have strong (or any) BW effects.
- Also worth noting that adding any noise to WC models leads to very sharp noisy peaks in the power spectra. It's a far stronger effect than I'd have predicted.
