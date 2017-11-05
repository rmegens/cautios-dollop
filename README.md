# cautios-dollop
Ansible playbook for installing IIS on a Windows 2012R2 server.

# About this guide
This guide describes the steps to setup an Ansible control node and a Windows 2012R2 managed node to run Ansible playbooks on a Windows 2012R2
managed node by using winrm. 

# Ansible and Windows
Ansible can be used to manage Windows managed hosts. However, the ansible control node still needs to be Linux.
WinRM is used to connect to the Windows managed host. On Linux this support is implemented with a python module pywinrm.
This allowes a Linux computer to interact with the WinRM system on ports 5985(http) and 5986(https). For authentication, 
there are 5 distinct options available:

| Option      | Local Accounts | Active Directory Accounts | Credentials Delegation |
|-------------|:--------------:|:-------------------------:|:----------------------:|
| Basic       | Yes            | No                        | No                     |
| Certificate | Yes            | No                        | No                     |
| Kerberos    | No             | Yes                       | Yes                    |
| NTLM        | Yes            | Yes                       | No                     |
| CredSSP     | Yes            | Yes                       | Yes                    |

This guide aims to show the concepts of working with Ansible on Windows and therefor will use basic authentication to make contact with winrm. Also, we will allow for unencrypted authentication traffic.

# Setup the control node
## Install pywinrm module
As mentioned, winrm support is implemented via a python(2) module called pywinrm. This module has to be installed by pip.
```
pip install pywinrm
```

# Setup WinRM on the Windows 2012 R2
WinRM is already installed on a stock Windows 2012R2 installation. We need to setup a user account for ansible to work with. This account needs to have administrator privileges since it needs to perform administrative tasks. Also we need to configure winrm authentication to set to basic and loosen security even more by allowing for unencrypted authentication traffic on the http port 5985.

Steps to be taken:
1. create a ansible account called 'remoteuser' with a password on the Windows 2012R2 server
2. make this user member of the local administrators group so it can perform admin tasks
3. setup 

