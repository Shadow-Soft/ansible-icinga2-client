This series of ansible playbooks installs and configures an icinga client to a given icinga master. 
Note: This has only been tested on python 2.7, Ansible 2.4.2 and with pexpect 3.3.  For AWS related components, use the latest version of boto

For all below scripts, ensure the private_key used to connect to hosts has been set under group_vars/all.yml

icinga-client-config.yml - playbook assumes that the client will be directly connecting to a singular master. To leverage these ansible playbooks the following must be changed.

1. The host template located under files/host_template.j2 must be updated to contain any variables that will associated the new client with a set of service/host checks
2. The host file under ./inventory/host must be updated to include the all the new clients as well as the current icinga master.  Examples are included
3. The icinga version number will be autodiscovered from the master.  There is no need to specify at this time.
4. The host file must include the new clients as a list under [new_icinga_clients]
5. The username associated with the client and master hosts must be equally specified
6. Ansible assumes the running instance has SSH access to the master and client.  Furthermore, sudoers permissions should be available as well

aws-icinga-client-config.yml - playbook is an example modification to the above playbook for aws specific deployment.  Instead of leveraging a static hosts file, this builds off of the AWS dynamic inventory (inventory/aws-hosts)

1. AWS Key and Secret must be set as environment variables as described in inventory/aws-hosts
2. This script assumes a number of tags have been set on instances.  To best leverage this use the playbook aws-icinga-create-test-instances.yml and make the appropriate modifications to tasks/test-vars.yml
3. The host template located under files/host_template.j2 must be updated to contain any variables that will associated the new client with a set of service/host checks

aws-icinga-create-test-instances.yml - Playbook creates instances used for testing purposes (icinga master, centos 6/7 instances and ubuntu 14.04/16.04 instances).

1. To properly leverage this playbook, modifications must be made to tasks/test-vars.yml
2. For our example, we leverage environment variables to fill in many of the requires variables as these will be populated by Jenkins.

aws-icinga-destroy-test-instances.yml - Playbook destroys existing instances that were created using the above playbook.
1. Ensure tasks/test-vars.yml hasn't changed since instances were created

aws-launch-test-environment.py - Python script which launches test instances using the above playbooks, ensures they deploy properly and installs python on Ubuntu based hosts (since it's not included OOTB). 
1. To properly leverage this playbook, modifications must be made to tasks/test-vars.yml
2. For our example, we leverage environment variables to fill in many of the requires variables as these will be populated by Jenkins.

aws-master-hostname-recon.yml - Playbook which will regenerate the public masters certificate based on the AWS Public DNS entry.  Use this only with an elastic ip in AWS otherwise the dns/ip will change on each instance reboot.  Also, the clients will need elastic ips as well for the exact same reason.  A smarter route would be to leverage your own registered domain name in route53 so when the box reboots the domain name always points to the same machine in AWS.
1. Change variables in the aws-config playbook to match the ec2 public dns entries:
    fqdn: "{{ ec2_public_dns_name  }}"
    fqdn_attr: "{{ ec2_public_dns_name }}"
  Note: There is a reference to these variables in the first two plays.
