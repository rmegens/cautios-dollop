#!/usr/bin/python2.7
# test_winrm.py
# version 1.0, d.d. 5 nov 2017 by RME
# simple python(2.7) script to test winrm connectivity

# import winrm module
import winrm

# declare variables
uname=Administrator
pword='-LSKJ?rrLh8'
managednode=ec2-54-171-94-237.eu-west-1.compute.amazonaws.com
remotecmd='hostname'

session = winrm.Session(managednode, auth=(uname,pword))

result = session.run_ps(remotecmd)

print(result.std_out)

# EOF
