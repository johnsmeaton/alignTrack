# alignTrack

Welcome to this collaborative repo for UCL g-2 team!  

The file mp2tst.bin [default binary file] is produced by mptest2.f90 [lines 98, 354- 381]. 

Here are the instructions to get the code on working on DAQ1: 

0. `scl enable devtoolset-3 python27 bash`
1.  `git clone https://github.com/glukicov/alignTrack.git`
to get the latest code from our repository 
2. `cd alignTrack/mpIIDESY`
3. `make`
to build the pede executable 
4. test that it works by `pede -t`
(should give a terminal output [last 2 lines]:
 Millepede II-P ending   ... Mon Dec 12 12:31:15 2016 
 Peak dynamic memory allocation:    0.100512 GB
5. `make -f handler.mk`
This build my handler code from MilleHandler.cpp (requires C++11) 
It has root capabilities for future testing/integration 
6. `Run the above with  ./MilleHandler`
This produces test.bin and test.root
7. To check the binary file do `python readMilleBinary.py "FILENAME" "N of line"`
e.g. `python readMilleBinary.py test.bin -1` [reads our binary for all lines] 
e.g. `python readMilleBinary.py mp2tst.bin 2` [reads default binary for 2 lines] 


###### Running C++ Port of Test 1 ######
1. Compile code with `make -f MakeMpTest1.mk`
2. Generate data by running `./MpTest1`. This generates:
   * `mp2test1_true_params_c.txt`: A plaintext file containing true values of parameters, with their labels, for comparison with fitted values.
   * `mp2tst1_c.bin`: A binary file containing fitting data.
   * `mp2test1con_c.txt`: A plaintext file containing parameter constraints.
   * `mp2test1str_c.txt`: A plaintext file containing steering information for `pede`. (Note - it is important to use the steering file generated here, rather than that generated by `./pede -t`, as this steering file flags the data binary as being generated by C, rather than Fortran.)
3. Fit data by running `./pede mp2test1str_c.txt`. 

###### Comparing True, Fitted Parameter Values ######
1. Ensure `python` use is enabled.
2. Generate test data, using either Fortran or C++ programme. This will generate a file containing true parameter values, for example `mp2test1_true_params_c.txt`.
3. Fit data using `./pede str.txt`. This will generate a results file `millepede.res`.
4. Run python script to compare parameter values, using `python compareParams.py -f <pede results file> -t <true parameter values file>`

###### Running C++ version of mptest2.f90: ######
1. Compile code with `make -f MakeMp2test.mk`
2. Generate data by running `./Mptest2`. This generates:
   * `Mp2tst.bin`, `Mp2con.txt`, `Mp2str.txt`
3. Fit data by running `./pede Mp2str.txt`.

### To run PEDE algorithm in general ###
1.  ` ./pede str.txt` [where e.g. str.txt is a steering file, which specifies both - a data.bin file and a constraint file (e.g. con.txt)]


### To run PEDE algorithm for Fortran version of Mptest2 ###
1. ` ./pede -t=track-model`
where track-model = SL0, SLE, BP, BRLF, BRLC [see p. 154 of refman.pdf] 

e.g. ./pede -t=SL0 [check the correct parameters, aslo option for flag -ip] 

### Generating Random Numbers ###
` python randomGenerator.py -g True`  [Gaussian (mean=0, std=1)]
` python randomGenerator.py -g True` [Uniform (0,1)]

### Reading Pede Histograms ###
` root -l `
` root [0] .L readPedeHists.C+`
` gStyle->SetOptStat(1111111)` [to see Under/Overflows and Integrals]
` root [1] readPedeHists()` [possible options inisde () "write" "nodraw" "print"] 