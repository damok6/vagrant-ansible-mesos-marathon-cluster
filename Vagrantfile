# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

mesos_master_ip = "192.168.33.20"

ANSIBLE_GROUPS = {
              "master" => ["master"],
              "nodes" => ["node1", "node2", "node3", "node4"],
              "all_groups:children" => ["master", "nodes"]
            }

Vagrant.configure(2) do |config|
#    config.vm.box = "ubuntu/xenial64"
    config.vm.box = "ubuntu/trusty64"
#	config.vm.synced_folder ".", "/vagrant", disabled: true
	
	# DK: to allow ansible to use a version in the guest os instead of needing one in the host OS, which does not work in Windows
	provisioner = Vagrant::Util::Platform.windows? ? :guest_ansible : :ansible
	# DK: actually do this manually below by using "guest_ansible" instead of "ansible" for the provisioner

	config.vm.provider "virtualbox" do |vb|
		vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]		
	end
	
	config.vm.provision "shell", path: "install_ansible.sh"
	
    config.vm.define "master" do |master|
        master.vm.network "private_network", ip: mesos_master_ip
        master.vm.hostname = "master"
		master.vm.provider "virtualbox" do |vb|
			vb.cpus = 1
			vb.memory = "1024"
		end
        master.vm.provision "guest_ansible", run: "always" do |ansible|
            ansible.playbook = "playbook.yml"
            ansible.groups = ANSIBLE_GROUPS
			ansible.extra_vars = {
				master_ip: mesos_master_ip
			}
        end
    end

	(1..4).each do |i|
		config.vm.define "node#{i}" do |node|
			node.vm.network "private_network", ip: "192.168.33.2#{i}"
			node.vm.hostname = "node#{i}"
			node.vm.provider "virtualbox" do |vb|
				vb.cpus = 2
				vb.memory = "3072"
			end
			node.vm.provision "guest_ansible", run: "always" do |ansible|
				ansible.playbook = "playbook.yml"
				ansible.groups = ANSIBLE_GROUPS
				ansible.extra_vars = {
					master_ip: mesos_master_ip
				}
			end
		end
	end

end
