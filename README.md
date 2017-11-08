# About cautios-dollop
This guide describes the steps to setup an Ansible control node and a Windows 2012R2 managed node to run Ansible playbooks on a Windows 2012R2 managed node by using winrm.

# Security considerations
This guide has a focus on how to connect and interoperate an Ansible Control Node to a Windows managed host. Therefore security is set to basic to avoid fighting to many battles at once.

# Ansible and Windows
Ansible can be used to manage Windows managed hosts. However, the ansible control node still needs to be Linux. WinRM is used to connect to the Windows managed host. On Linux this support is implemented with a python module pywinrm. This allowes a Linux computer to interact with the WinRM system on ports 5985(http) and 5986(https).

For authentication there are 5 distinct options available:

| Option      | Local Accounts | Active Directory Accounts | Credentials Delegation |
| ----------- | :------------: | :-----------------------: | :--------------------: |
| Basic       |      Yes       |            No             |           No           |
| Certificate |      Yes       |            No             |           No           |
| Kerberos    |       No       |            Yes            |          Yes           |
| NTLM        |      Yes       |            Yes            |           No           |
| CredSSP     |      Yes       |            Yes            |          Yes           |

This guide aims to show the concepts of working with Ansible on Windows and therefor will use basic authentication to make contact with winrm. Also, we will allow for unencrypted authentication traffic.

# Setup the control node
## Install pywinrm module
As mentioned, winrm support is implemented via a python(2) module called pywinrm. This module has to be installed by pip.
```
pip install pywinrm
```

# Setup WinRM on the Windows 2012 R2
WinRM is already installed on a stock Windows 2012R2 installation. We need to setup a user account for ansible to work with. This account needs to have administrator privileges since it needs to perform administrative tasks. Also we need to configure winrm authentication to set to basic and loosen security even more by allowing for unencrypted authentication traffic on the http port 5985.

## Required software
On the Windows 2012R2 server, we need:
* .NET Framework 4.6 or higher
* Windows Management Framework 5.0 or higher

## Command execution
Different from Ansible on Linux, on Windows execution is by use of PowerShell and the .NET framework. For this a user with elevated privileges is needed to execute. Tasks will be executed in form of batches.

> This guide assumes the user has the skills necesarry to operate Windows 2012R2 with PowerShell and is able to create a local user with administrative privileges.

## Steps
1. create a ansible account called 'remoteuser' with a password on the Windows 2012R2 server
2. add this user to the local administrators group so it can perform admin tasks
3. setup winrm with Powershell(PS) (3 options to choose from, this guide preferes the first one)
```
# enable winrm on this server
winrm quickconfig
# or use
Configure-SMremoting.exe --enable
# or use
Enable-PSRemoting --Force
# this enables powershell remoting, set's up the winrm listener and enables the windows firewall # rule for winrm. 
```
4. configure WinRM for basic security and enable unencrypted traffic (using PS)
```
# allow for unencrypted traffic
winrm set winrm/config/service @{AllowUnEncrypted="true"}

# set authentication type to basic
winrm set winrm/config/service/auth @{basic="true"}
```
5. open the firewall for winrm with the graphical firewall tool



# Test WinRM with python on control node
Now we can test if winrm is working, without using Ansible by using a simple python script on the control node. If our Ansible test fails later on we at least know where to look when troubleshooting.

Cut and paste the script below into test_winrm.py
```
# test_winrm.py
# version 1.0, d.d. 5 nov 2017 by rikmegens@work-smarter.nl
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
```

Run this script on the Linux control node from the command line by using python27 or by making this file executable. If the output is a hostname, connectivity is established. If the script throws an error, there is something not working correct and this means Ansible will probably not function properly either.

# Ansible ad-hoc to Windows managed node
## Setting up the inventory
The Windows 2012R2 managed host in this example is a stock installed server on a KVM/QEMU hypervisor. To connect to this node, we need to add some variables to the inventory file.
| Variable               | Value         |
| ---------------------- | ------------- |
| SrvName                | win2012r2srv  |
| IPv4                   | 192.168.1.199 |
| Ansible remote account | remoteuser    |
| Ansible user passwd    | secret123     |
| winrm port (http)      | 5985/tcp      |

The inventory file (inventory) looks like this:
```
[winsrvs]
win2012r2srv

[winsrvs:vars]
ansible_user=remoteuser
ansible_password=secret123
ansible_connection=winrm
ansible_port=5985
```

## run the ad-hoc command
As is the case for 'normal' linux controlnodes with the ping module, we can use win_ping to check the connection.
```
ansible win2012r2srv -i inventory -m win_ping
```
If everything is configured as described, the module should return 'pong'.



# Ansible playbook to Windows managed node
## Setting up the playbook

For a playbook a directory structure is created for the different components like tasks, inventory and variables. The configuration for this playbook is managed by ansible.cfg in the working directory of this playbook. Files can be cloned with git from this repository (git clone https://github.com/rmegens/cautios-dollop.git ). Below the more interesting files are listed.

```
/playbooks/cautios-dollop
						/ansible.cfg				# ansible config file
						/go_webapp_remove.yaml		 # remove IIS from managed node
						/go_webapp_install.yaml		 # install IIS on managed node
						/test_winaws.yaml			 # test winrm connectivity with ansible
						/test_winkvm.yaml			 # test winrm connectivity with ansible
						/files/index.html			 # custom index page for IIS
						/group_vars/winsrvs.yaml	  # server group variables
						/inventory/inventory 		 # inventory file
						/logs/ansible-windows.log	 # created by running the playbook
						/tasks/						# tasks of the playbook

```

Example ansible.cfg

```
[defaults]
log_path        = ./logs/ansible-windows.log
inventory       = inventory

[privilege_escalation]
[paramiko_connection]
[ssh_connection]
[accelerate]
[selinux]
[colors]
```

Example files/index.html

```
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Managing a Windows managed node with Ansible</title>
  <meta name="description" content="Windows managed node with Ansible">
  <meta name="author" content="Work-smarter.nl">
</head>

<body>
  <h1>Welcome on this Ansible managed server</h1>
  <p>Have a nice day</p>
</body>
</html>
```



Example inventory/inventory

```
[winsrvs]
win2012r2srv

[winsrvs:vars]
ansible_user=remoteuser
ansible_password=secret123
ansible_connection=winrm
ansible_port=5985
```





## Run the playbook

To test connectivity to the Windows 2012R2 managed node on the local KVM/QEMU hypervisor run: 

```
ansible-playbook test_win_kvm.yaml
```



To test connectivity to the Windows 2012R2 managed node on AWS run:

```
ansible-playbook test_aws.yaml
```



To install the webserver feature on the Windows 2012R2 managed node run:

```
ansible-playbook go_webapp_install.yaml
```
Test if the installation has been succesful by using a brower or curl to http:/win2012r2srv



To remove the webserver feature on the Windows 2012R2 managed node run:

```
ansible-playbook go_webapp_remove.yaml
```