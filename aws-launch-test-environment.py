#!/usr/bin/python
import subprocess
import sys
import time
import os

print "Initializing environment variables"
icingagroup=os.environ['ICINGA_TEST_GROUP']
master_user=os.environ['ICINGA_MASTER_USER']
FNULL = open(os.devnull, 'w')

def testRemoteMachines(aws_group, username, command):
	complete=False
	hosts="retry"
	while hosts=="retry":
		try:
			hosts=subprocess.check_output("ansible -i inventory/aws-hosts --list "+aws_group+" | sed -n '1!p' | tr -d ' '", shell=True, stderr=FNULL)
		except:
			hosts="retry"
			
	while complete == False:
		complete=True
		for host in hosts.splitlines():
			rc=subprocess.call("ssh -n "+username+"@"+host+" -oStrictHostKeyChecking=no -i ~/.ssh/DerrickKeyPair.pem \""+command+"\"", shell=True, stdout=FNULL, stderr=FNULL)
			if rc != 0:
				print "\tFailed for "+host+", will retry in 5 seconds"
				complete=False
			else:
				print "\tSuccess for "+host
		if complete == False:
			time.sleep(5)	
	print ""

			
print "Creating instances to test"
rc=subprocess.call("ansible-playbook aws-icinga-create-test-instances.yml -i inventory/aws-hosts", shell=True, stdout=FNULL, stderr=FNULL)
if rc != 0:
	print "Creating instances failed with exit code "+str(rc)
	sys.exit(rc)
	
print "Waiting for Icinga 2 Test machines to register with AWS"
complete=False
while complete == False:
	complete=True
	try:
		rc=subprocess.call("ansible -i inventory/aws-hosts --list tag_Group_"+icingagroup+"*", shell=True, stdout=FNULL, stderr=FNULL)
		if rc!=0:
			complete=False
	except:
		pass
		
	if complete == False:
		print "\tNo hosts found yet, will retry in 10 seconds"
		time.sleep(10)
print ""
	
print "Trying to test connect to Ubuntu machines and install python"
testRemoteMachines("tag_Group_"+icingagroup+"_ubuntu","ubuntu","sudo apt-get update; sudo apt-get install -y python")

print "Trying to test connect to centos machines"
testRemoteMachines("tag_Group_"+icingagroup+"_centos","centos","echo hello")

print "Trying to test connect to master machines"
testRemoteMachines("tag_Group_"+icingagroup,master_user,"echo hello")
