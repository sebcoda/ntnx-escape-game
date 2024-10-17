## Setup 

- Create an alternative admin user / OK
- Connect with it / OK
- Create a project / OK
- Create a subnet / OK
- Add an image / OK
- Create a new VM with user / OK
- Check with prod user it is not viewable / OK
- Move the VM on another node / OK
- Create a category #OK
- Securize the VM
	- Encryption #OK
	- Microseg
	- Replication
- Create approval rule to prevent deletion of RP
- VM has been deleted, restore VM from recovery point

## Operational help

- Create report to send-it regularly to an email
- Add a node
- LCM ?
- Cluster Runaway (on Specialists HPOC ?)
	- Identify bad sized VM (on Specialists HPOC ?) with `Optimize resources`
- Create Playbook to call a webhook as soon as VM is restarted
- Clone prod into a VPC
	- do it once
	- Schedule a refresh 
- Change app in marketplace to add (spying) task

## Others (Not in 1rst release)
- Create file share
- Create DB
- Create bucket