# NMEA_Data_Parsing
########################################################################################################################
# Coding Exercise – Techworks Marine
# @author ERDOGAN BERKE KOCAR

Introduction
GPS data is given in NMEA data output when read by a sensor system. This data needs to be parsed, verified and written to a file in a particular format. For this exercise you will be given some example GPS data (GPS.txt), your script should extract the relevant data and output to a file in csv format

In a csv file (comma separated) we should be able to see the following data:
1.	Date
2.	Time
3.	Latitude
4.	Longitude
5.	Number of Satellites 

Parsing methodology: The general logic of my algorithm is, firstly it reads the data between GPTXT's and store its values in to dictionary. At the end of the reading it merges the dictionary values by keys and writes in to CSV file. Data Structure Usage: Dictionary. The reason I used dictionary is it provides a easy access in to data with key-value relation.) A Python dictionary is an unordered collection of data values. Unlike other data types that hold only one value as an element, a Python dictionary holds a key: value pair. The Python dictionary is optimized in a manner that allows it to access values when the key is known.
