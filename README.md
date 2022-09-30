This simple program computes traffic assignments using the FW method. BPR cost function is assigned as a major cost function method. 

Our code is tested for various networks available on [TransportationNetworks](https://github.com/bstabler/TransportationNetworks).

Our program has been tested for all the networks for which a solution is available on [TransportationNetworks](https://github.com/bstabler/TransportationNetworks) and has always obtained the correct solution.



# How to use

1) Download a Python file ("ComputeTrafficAssignment.py")

2) Insert Network_file (CSV format) & Demand_file (CSV format) in " import_network " function as inputs

3) Determine the file path for the total cost in the " reportTotalCost " function  

4) Determine file path for final flow in the " reportFlow " function

5) Run the program



# Importing networks

 Networks and demand files must be specified in the CSV data format.

 A thorough description of the CSV format and a wide range of real transportation networks to test the algorithm on is available at [TransportationNetworks](https://github.com/bstabler/TransportationNetworks).

 Several well-known networks’ CSV data format has been provided in the CSV_networks folder.


# Acknowledgments

All the networks I used to test the algorithm’s correctness are available at [TransportationNetworks](https://github.com/bstabler/TransportationNetworks).

The entire program is written by Ashkan Fouladi (fooladiashkang@gmail.com) & Vahid Noroozi (vahidnoroozi1994@yahoo.com).
