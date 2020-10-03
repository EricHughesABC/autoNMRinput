# autoNMRinput

This software is designed to work in a University chemistry department environment or similar, where the users belong to research groups and have walk-on access to the NMR spectrometers. The solution is specific to Bruker NMr spectrometers using iconnmr as the frontend interface between the users and the spectrometer. 

Submission of experiments to the spectometers is a two step process using first an excel spread sheet and then a python script.

The excel sheet resides on the  user's own computer. The excel sheet saves the input to a csv file in a directory that is accessible by the different spectrometers.
A single python script converts the csv file into a text file that can be read by the NMR spectrometers which starts the automation process on the spectrometer.

All the NMR spectrometers are manufactured by Bruker, the computers controlling the spectrometers are running a Linux operating system and are not hooked up to the outside internet. The python script has been written to use the python version that comes with the operating system which is typically below 2.7.

In order to use this software it will need adapting by the user to their specific environment. I have posted the software on github for two reasons, one to keep a working copy in a known place and second, for others who may need to implement a similar solution an example to look at, adapt and improve.
