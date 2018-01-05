#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
DOCUMENTATION = '''
---
author: "Derrick Sutherland"
module: apt_install_ver
short_description: Use apt-get to install an older version of a package
version_added: "2.0"
description:
     - Use apt-get to install an older version of a particular software and all its associated dependencies
options:
  package:
    description:
      - The name of the package to install
	required: true
  version:
    description:
      - The version for the package to install
    required: true
'''

EXAMPLES = '''
# Install an old version of icinga on Debian
- name: Install an old version of icinga on Debian
  hosts: 127.0.0.1
  connection: local
  tasks:
    - name: Install icinga
      apt_install_ver:
        package: icinga2
        version: 2.7.2-1.xenial
'''

import subprocess
from ansible.module_utils.basic import *

argument_spec = dict(
	package=dict(required=True),
	version=dict(required=True),
)
module = AnsibleModule(
	argument_spec=argument_spec
)
fh = open("/tmp/log.txt","w")

def install(pkg,ver,tab):
	pkg_ver=pkg+"="+ver
	fh.write(tab+"Checking "+pkg_ver+"\n")
	res = subprocess.check_output("sudo apt-get -s install "+pkg_ver+" 2>1 | grep Depends | sed -e \"s/.*"+pkg+" ://p\" | awk {' print $2 \"=\" $4 '} | tr -d ')' | tail -n +2", shell=True)
	for dependency in res.splitlines():
		dep_name=dependency.split("=")[0]
		dep_ver=dependency.split("=")[1]
		install(dep_name,dep_ver,tab+"\t")
	fh.write(tab+"installing "+pkg_ver+"\n")
	subprocess.Popen("sudo apt-get install -y "+pkg_ver, shell=True, stdin=subprocess.PIPE ).communicate()
	
def main():
	package=module.params.get('package')
	version=module.params.get('version')

	try:
		install(package,version,"")
		data = dict(changed=True, status='installed')
		module.exit_json(**data)
	except Exception, e:
		module.fail_json(msg='Failed to install '+package+': '+ str(e))
	finally:
		fh.close()

if __name__ == '__main__':
    main()
