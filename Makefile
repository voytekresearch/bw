SHELL=/bin/bash -O expand_aliases

# =========================================================================
ie: mixie_n mixie_s driftie_d burstie1 drivie1


# =========================================================================
# Explore increasing drive of E in a single population

drivie1:
	-mkdir data/drivie1
	-rm data/drivie1/*
	parallel -j 10 \
		--joblog 'data/drivie1/log' \
		--nice 19 \
		'python ie.py data/drivie1/d_{} -p {} -q 1 -t 3' ::: 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.5


# =========================================================================
# Explore population number, leaving drive std dev constant
# mixie_n: mixie5 mixie10 mixie20 mixie40 mixie80 mixie160 mixie320

mixie_n:
	-mkdir data/mixie_n
	-rm data/mixie_n/*
	parallel -j 10 -v \
		--joblog 'data/mixie_n/log' \
		--nice 19 \
		'python mixie.py data/mixie_n/n{1}_run{2} -n {1} -p 1 -q 2 -s .5 -t 3 --seed {2}' ::: 3 5 7 9 10 12 14 16 18 20 ::: {1..100}

# -
# Explore std dev in drive, leavning n constant
mixie_s:
	-mkdir data/mixie_s
	-rm data/mixie_s/*
	parallel -j 10 -v \
		--joblog 'data/mixie_s/log' \
		--nice 19 \
		'python mixie.py data/mixie_s/s{1}_run{2} -n 10 -p1 -q 2 -s {1} -t 3 --seed {2}' ::: 0.5 0.7 0.9 1.1 1.3 1.5 1.7 1.9 2.0 ::: {1..100} 

# =========================================================================
# Burstie
# Explore burst length
burstie1:
	-mkdir data/burstie1
	-rm data/burstie1/*
	parallel -j 10 -v \
		--joblog 'data/burstie1/log' \
		--nice 19 \
		'python burstie.py data/burstie1/{} -t 3 -b 0.8 -w 0.5 -s 1 --seed {1}' ::: {1..100}


# =========================================================================
# Explore drift
# try a few drift parameters, repeating each a 100 random interations
driftie_d:
	-mkdir data/driftie_d
	-rm data/driftie_d/*
	parallel -j 10 -v \
		--joblog 'data/driftie_d/log' \
		--nice 19 \
		'python driftie.py data/driftie_d/d{1}_run{2} -d {1} --min_P 0.5 -t 3 --seed {2}' ::: 0.01 0.03 0.05 0.07 .1 .2 .3 ::: {1..100}


# =========================================================================
#
kur: kur_k kur_r


kur_k: 
	-mkdir data/kur_k
	-rm data/kur_k/*
	parallel -j 10 -v \
		--joblog 'data/kur_k/log' \
		--nice 19 \
		'python kur.py data/kur_k/k{1}_run{2} -t 3 -n 10 -k {1} -o 25 -r 5 --seed {2}' ::: 1 3 6 9 12 ::: {1..100}

kur_r:
	-mkdir data/kur_r
	-rm data/kur_r/*
	parallel -j 10 -v \
		--joblog 'data/kur_r/log' \
		--nice 19 \
		'python kur.py data/kur_r/r{1}_run{2} -t 3 -n 50 -k 6 -o 25 -r {1} --seed {2}' ::: 1 3 5 7 9 ::: {1..100}

