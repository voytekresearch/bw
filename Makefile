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
		'python ie.py data/drivie1/d_{} -p {} -q 1' ::: 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.5

# =========================================================================
# Explore population number, leaving drive std dev constant
# mixie_n: mixie5 mixie10 mixie20 mixie40 mixie80 mixie160 mixie320

mixie_n:
	-mkdir data/mixie_n
	-rm data/mixie_n/*
	parallel -j 10 -v \
		--joblog 'data/mixie_n/log' \
		--nice 19 \
		'python mixie.py data/mixie_n/n{1}_run{2} -n {1} -p 1 -q 2 -s .5' ::: 3 5 7 9 10 12 14 16 18 20 ::: {1..100}

# mixie5:
# 	-mkdir data/mixie5
# 	-rm data/mixie5/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie5/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie5/run_{} -n 5 -p 1 -q 2 -s .5' ::: {1..100}
#
# mixie10:
# 	-mkdir data/mixie10
# 	-rm data/mixie10/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie10/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie10/run_{} -n 10 -p 1 -q 2 -s .5' ::: {1..100} 
#
# mixie20:
# 	-mkdir data/mixie20
# 	-rm data/mixie20/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie20/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie20/run_{} -n 20 -p 1 -q 2 -s .5' ::: {1..100}  
#
# mixie40:
# 	-mkdir data/mixie40
# 	-rm data/mixie40/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie40/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie40/run_{} -n 40 -p 1 -q 2 -s .1' ::: {1..100}  
#
# mixie80:
# 	-mkdir data/mixie80
# 	-rm data/mixie80/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie80/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie80/run_{} -n 80 -p 1 -q 2 -s .5' ::: {1..100}  
#
# mixie160:
# 	-mkdir data/mixie160
# 	-rm data/mixie160/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie160/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie160/run_{} -n 160 -p 1 -q 2 -s .5' ::: {1..100}  
#
# mixie320:
# 	-mkdir data/mixie320
# 	-rm data/mixie320/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie320/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie320/run_{} -n 320 -p 1 -q 2 -s .5' ::: {1..100}  
#
# -
# Explore std dev in drive, leavning n constant
mixie_s:
	-mkdir data/mixie_s
	-rm data/mixie_s/*
	parallel -j 10 -v \
		--joblog 'data/mixie_s/log' \
		--nice 19 \
		'python mixie.py data/mixie_s/s{1}_run{2} -n 10 -p1 -q 2 -s {1}' ::: 0.5 1 1.5 2.0 ::: {1..100} 

# mixie_s: mixie_s3 mixie_s5 mixie_s7
#
#
# mixie_s3:
# 	-mkdir data/mixie_s3
# 	-rm data/mixie_s3/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie_s3/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie_s3/run_{} -n 20 -p1 -q 2 -s .3' ::: {1..100} 
#
# mixie_s5:
# 	-mkdir data/mixie_s5
# 	-rm data/mixie_s5/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie_s5/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie_s5/run_{} -n 20 -p1 -q 2 -s .5' ::: {1..100} 
#
# mixie_s7:
# 	-mkdir data/mixie_s7
# 	-rm data/mixie_s7/*
# 	parallel -j 10 -v \
# 		--joblog 'data/mixie_s7/log' \
# 		--nice 19 \
# 		'python mixie.py data/mixie_s7/run_{} -n 20 -p1 -q 2 -s .7' ::: {1..100} 
#
# =========================================================================
# Burstie
# Explore burst length
burstie1:
	-mkdir data/burstie1
	-rm data/burstie1/*
	parallel -j 10 -v \
		--joblog 'data/burstie1/log' \
		--nice 19 \
		'python burstie.py data/burstie1/{} -t 2 -b 0.8 -w 0.5 -s 1' ::: {1..100}


# =========================================================================
# Explore drift
# try a few drift parameters, repeating each a 100 random interations
driftie_d: driftie_d05 driftie_d1 driftie_d2 driftie_d3


driftie_d05:
	-mkdir data/driftie_d05
	-rm data/driftie_d05/*
	parallel -j 10 -v \
		--joblog 'data/driftie_d05/log' \
		--nice 19 \
		'python driftie.py data/driftie_d05/{} -d .05 --min_P 0.5' ::: {1..100}

driftie_d1:
	-mkdir data/driftie_d1
	-rm data/driftie_d1/*
	parallel -j 10 -v \
		--joblog 'data/driftie_d1/log' \
		--nice 19 \
		'python driftie.py data/driftie_d1/{} -d .1 --min_P 0.5' ::: {1..100}

driftie_d2:
	-mkdir data/driftie_d2
	-rm data/driftie_d2/*
	parallel -j 10 -v \
		--joblog 'data/driftie_d2/log' \
		--nice 19 \
		'python driftie.py data/driftie_d2/{} -d .2 --min_P 0.5' ::: {1..100}

driftie_d3:
	-mkdir data/driftie_d3
	-rm data/driftie_d3/*
	parallel -j 10 -v \
		--joblog 'data/driftie_d3/log' \
		--nice 19 \
		'python driftie.py data/driftie_d3/{} -d .3 --min_P 0.5' ::: {1..100}

# =========================================================================
kur: kur_k1 kur_k6 kur_k12 kur_r1 kur_r2 kur_r4


# Explore kuramoto K, at fixed N and fixed freq (20, same as mixie_s)
kur_k1:
	-mkdir data/kur_k1
	-rm data/kur_k1/*
	parallel -j 10 -v \
		--joblog 'data/kur_k1/log' \
		--nice 19 \
		'python kur.py data/kur_k1/{} -n 20 -k 1 -o 10 -r 0' ::: {1..100}

kur_k6:
	-mkdir data/kur_k6
	-rm data/kur_k6/*
	parallel -j 10 -v \
		--joblog 'data/kur_k6/log' \
		--nice 19 \
		'python kur.py data/kur_k6/{} -n 20 -k 6 -o 10 -r 0' ::: {1..100}

kur_k12:
	-mkdir data/kur_k12
	-rm data/kur_k12/*
	parallel -j 10 -v \
		--joblog 'data/kur_k12/log' \
		--nice 19 \
		'python kur.py data/kur_k12/{} -n 20 -k 12 -o 10 -r 0' ::: {1..100}

# Explore kuramoto range at an intermediate K
kur_r1:
	-mkdir data/kur_r1
	-rm data/kur_r1/*
	parallel -j 10 -v \
		--joblog 'data/kur_r1/log' \
		--nice 19 \
		'python kur.py data/kur_r1/{} -n 20 -k 6 -o 10 -r 1' ::: {1..100}

kur_r2:
	-mkdir data/kur_r2
	-rm data/kur_r2/*
	parallel -j 10 -v \
		--joblog 'data/kur_r2/log' \
		--nice 19 \
		'python kur.py data/kur_r2/{} -n 20 -k 6 -o 10 -r 2' ::: {1..100}

kur_r4:
	-mkdir data/kur_r4
	-rm data/kur_r4/*
	parallel -j 10 -v \
		--joblog 'data/kur_r4/log' \
		--nice 19 \
		'python kur.py data/kur_r4/{} -n 20 -k 6 -o 10 -r 4' ::: {1..100}
