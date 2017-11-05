# test_winrm.py
# version 1.0, d.d. 5 nov 2017 by RME
# simple python(2.7) script to test winrm connectivity

# import winrm module
import winrm

# declare variables
uname=[your-ansible-username-here]
pword=[your-ansible-password-here]
managednode=[ip-of-windows-2012r2-managed-node-here]
remotecmd='hostname'

session = winrm.Session(managednode, auth=(uname,pword))

result = session.run_ps(remotecmd)

print(result.std_out)

# EOF
