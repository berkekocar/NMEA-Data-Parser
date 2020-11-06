########################################################################################################################
# Coding Exercise – Techworks Marine
# @author ERDOGAN BERKE KOCAR


# Parsing methodology: The general logic of my algorithm is, firstly it reads the data between GPTXT's and store its
# values in to dictionary. At the end of the reading it merges the dictionary values by keys and writes in to CSV file.
# Data Structure Usage: Dictionary. The reason I used dictionary is it provides a easy access in to data with
# key-value relation.) A Python dictionary is an unordered collection of data values.
# Unlike other data types that hold only one value as an element,
# a Python dictionary holds a key: value pair.
# The Python dictionary is optimized in a manner that allows it to access values when the key is known.

# Importing the csv library and regex
import csv
import re


# This method has the main functionality and does reading operation
def main():
    print("Program started...")
    # Create two dictionaries one for GPGGA other for GPRMC values
    GPGGA_dict = dict()
    GPRMC_dict = dict()
    reading_id = 0
    # Reading the file
    with open('GPS.txt', 'r') as in_file:
        for line in in_file:
            # Control the checksum if data valid or not
            try:
                control = checksum(line.strip())
            except:
                control = False
            # If the control true calla the parser method
            if control:
                # Split the line by six and assign a variable called code
                code = line[1:6]
                # Call the parser method which parse the file
                parser(GPGGA_dict, GPRMC_dict, code, line, reading_id)
    # Fill the dictionaries with the return of the parser method
    alldata_dict = filldict(GPGGA_dict, GPRMC_dict)
    # Write the dictionaries in to Csv file
    print("CSV Conversion Initialized...")
    writetocsv(alldata_dict)
    # Buffer close
    in_file.close()
    print("***********************************CSV file ready***********************************")


# Checksum method denotes to verification of our with the CRC error detection
def checksum(line):
    # String to hex conversion
    cksum = line[len(line) - 2:]
    # Slice the strings and grap the characters between the data within the flags($,*)
    chksumdata = re.sub("(\n|\r\n)", "", line[line.find("$") + 1:line.find("*")])
    # Initialize the initial XOR value
    csum = 0
    # Compare the each char in checksum data, comparing to previous XOR.
    # Last XOR will be the final checksum. For the verification we slice off the NMEA data.
    for c in chksumdata:
        # XOR'ing value of csum against the next char in line
        # and storing the new XOR value in csum
        csum ^= ord(c)
    # Check the valid line
    if hex(csum) == hex(int(cksum, 16)):
        return True
    return False


# Parser method parse the data. It has two extended methods for GPGGA and GPRMC
def parser(GPGGA_dict, GPRMC_dict, code, line, reading_id):
    # First we need to check the starting notation of the line
    if code == 'GPTXT':
        # Increment the reading
        reading_id += 1
    # Filtering the necessary data types
    if code in ['GPRMC', 'GPGGA']:
        # Split the lines from commas
        line = line.split(',')
        # Calling the sub-parsers
        gpggaParser(GPGGA_dict, code, line, reading_id)
        gprmcParser(GPRMC_dict, code, line, reading_id)


# This is the parser method for GPRMC Parser
def gprmcParser(GPRMC_dict, code, line, reading_id):
    # Checking the type of data(GPRMC)
    try:
        if code == 'GPRMC':
            # Controlling the validity and corrapted data's
            if line[2] == 'A' and (line[1] != '' and line[9] != ''):
                # Calling the formating methods for date and time values
                date_formatted, time_formatted = datetimeformat(line)
                # The key of the dictionary. The structure is 'timestamp':'reading_id'
                key = str(line[1]).strip() + ':' + str(reading_id)
                # Insert the key and values in to dicionary
                GPRMC_dict[key] = [date_formatted, time_formatted]
    except:
        pass


# This is the parser method for GPGGA Parser
def gpggaParser(GPGGA_dict, code, line, reading_id):
    # Checking the type of data(GPGGA)
    try:
        if code == 'GPGGA':
            # Check the gps quality indicator
            if line[6] in ['1', '2']:
                # The key of the dictionary. The structure is 'timestamp':'reading_id'
                key = str(line[1]).strip() + ':' + str(reading_id)
                # Calling the latitude and longitude formatting methods
                latitude_formated, longitude_formatted = latlonformat(line)
                # Insert the key and values in to dictionary
                GPGGA_dict[key] = [latitude_formated, longitude_formatted, line[7]]
    except:
        pass


# This method is used for writing the values in to csv format
def writetocsv(alldata_dict):
    # Open and writing to csv file
    with open("GPS_output.csv", "w") as outfile:
        # Creating a csv writer object
        writer = csv.writer(outfile)
        # Writing the fields
        writer.writerow(alldata_dict.keys())
        # Writing the data rows
        writer.writerows(zip(*alldata_dict.values()))
        # Buffer close
        outfile.close()


# This method is used for filling the dictionaries created for GPGGA other for GPRMC values
def filldict(GPGGA_dict, GPRMC_dict):
    # Insert the data column titles in to dictionary
    alldata_dict = {'Date': [], 'Time': [], 'Latitude': [], 'Longitude': [], 'Number of Satellites': []}
    # Pace between the dictionary items
    for key, GPGGA_value in GPGGA_dict.items():
        # Append the values in to keys
        try:
            GPRMC_value = GPRMC_dict[str(key)]
            alldata_dict['Date'].append(GPRMC_value[0])
            alldata_dict['Time'].append(GPRMC_value[1])
            alldata_dict['Latitude'].append(GPGGA_value[0])
            alldata_dict['Longitude'].append(GPGGA_value[1])
            alldata_dict['Number of Satellites'].append(GPGGA_value[2])
        except:
            continue
    return alldata_dict


# This method is used for formatting the date and time data
def datetimeformat(line):
    # Assign the related data in to variable for date
    date_formatted = line[9]
    # Format the date data by the slashes
    date_formatted = date_formatted[0:2] + "/" + date_formatted[2:4] + "/" + date_formatted[4:6]
    # Assign the related data in to variable fo time
    time_formatted = line[1]
    # Format the time data by the colon
    time_formatted = time_formatted[0:2] + ":" + time_formatted[2:4] + ":" + time_formatted[4:6]
    # Return the formatted date and time values
    return date_formatted, time_formatted


# This method is used for formatting the latitude and longitude data
def latlonformat(line):
    # Assign the related data in to variable for latitude
    latitude_formated = line[2]
    # Format the latitude data by the the formula:
    # Decimal Degrees = Degrees + (Minutes divided by 60) + (Seconds divided by 3600)
    latitude_formated = latitude_formated[:2].lstrip('0') + "." + "%.7s" % str(float(latitude_formated[2:]) * 1.0 / 60.0).lstrip("0.")
    # Assign the related data in to variable for longitude
    longitude_formatted = line[4]
    # Format the longitude data by the the formula:
    # Decimal Degrees = Degrees + (Minutes divided by 60) + (Seconds divided by 3600)
    longitude_formatted = longitude_formatted[:3].lstrip('0') + "." + "%.7s" % str(float(longitude_formatted[3:]) * 1.0 / 60.0).lstrip("0.")
    # Return the formatted latitude and longitude data
    return latitude_formated, longitude_formatted


# Defining the main function
if __name__ == "__main__":
    main()
