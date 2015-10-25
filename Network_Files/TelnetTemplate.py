#!/usr/bin/env python

import telnetlib
import time

# Open telnet connection to devices, takes a single arg, the ip address of the device
def open_telnet_conn(ip):
    try:
        # Define telnet parameters
        username = 'teopy'
        password = 'python'

        # User input for Config File that we will send to device
        cmd_file = raw_input("Enter config filename and extension, include full path if not in this dir: ")

        # Specify the Telnet Port
        port = 23

        # Specify the connection timeout in seconds for blocking operations, like connection attempts
        connection_timeout = 5

        # Specify a timeout in seconds.  Read until a string is found or the timeout period has passed
        reading_timeout = 5

        # Connect and Log into the device
        connection = telnetlib.Telnet(ip, port, connection_timeout)

        # Wait for Router to Ask for Username
        router_output = connection.read_until("Username:", reading_timeout)
        # Enter the username when prompted and a "\n" for Enter
        connection.write(username + "\n")

        # Wait until we are prompted for a password
        router_output = connection.read_until("Password:", reading_timeout)
        # Enter the password when prompted and use "\n" for Enter
        connection.write(password + "\n")
        time.sleep(1)

        # Set Terminal Length to get entire output - disabling pagination
        connection.write('terminal length 0\n')
        time.sleep(1)

        #Enter "Conf T" Mode
        connection.write("\n")
        connection.write("conf t\n")
        time.sleep(1)

        # Open user specified file
        selected_cmd_file = open(cmd_file, 'r')

        # Start from beginning of file
        selected_cmd_file.seek(0)

        # Write each line of the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.write(each_line + '\n')
            time.sleep(1)

        # Close the file
        selected_cmd_file.close()

        #Read command output
        router_output = connection.read_very_eager()
        print router_output

        # Close the Connection
        connection.close()

    except IOError:
        print "Input parameter Error, BIAAATCH!!"

# Call telnet function
if __name__ == '__main__':
    ip = raw_input("Please Enter the ip address of the device")
    open_telnet_conn(ip)









