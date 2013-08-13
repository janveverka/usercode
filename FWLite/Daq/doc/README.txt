FWLite/Daq/doc/README.txt - The README file of Jan's DAQ-related code pieces
============================================================================

ISILON TESTS - AUGUST 2013
--------------------------
The goal is to measure the performance of a small NAS cluster from the company
EMC(?).

The intersting quantities are the reading (outbound) and writing (inbound)
cluster filesystem throughputs. The number of reading and writing processes
and file sizes mimic the DAQ2 specifications.

The test cluster has an effective volume of ~ 40 TB.  This represents about
1/6-th of the SM2 design capacity. We assume that the cluster throughput
would scale linearly with the cluster size.

Related files:
data/rates_6x6_test1.dat
python/plot_rates.py

Results of the first test:
http://www.hep.caltech.edu/~veverka/plots/2013/13-08-13/
