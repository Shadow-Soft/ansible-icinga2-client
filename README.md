This series of ansible playbooks installs and configures an icinga client to a given icinga master. This playbook assumes that the client will be directly connecting to a singular master. To leverage these ansible playbooks the following must be changed.

1. The host template located under files/host_template.j2 must be updated to contain any variables that will associated the new client with a set of service/host checks
2. The host file under ./inventory/host must be updated to include the all the new clients as well as the current icinga master.  Examples are included
3. The icinga version number will be autodiscovered from the master.  There is no need to specify at this time.
4. The host file must include the new clients as a list under [new_icinga_clients]
5. The username associated with the client and master hosts must be equally specified
6. Ansible assumes the running instance has SSH access to the master and client.  Furthermore, sudoers permissions should be available as well


Note: This has only been tested on python 2.7, Ansible 2.4.2 and with pexpect 3.3.  For AWS related components, use the latest version of boto