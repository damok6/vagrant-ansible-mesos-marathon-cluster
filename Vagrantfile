# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

ANSIBLE_GROUPS = {
              "master" => ["node1"],
              "nodes" => ["node2", "node3", "node4"],
              "all_groups:children" => ["master", "nodes"]
            }

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/xenial64"
#	config.vm.synced_folder ".", "/vagrant", disabled: true
	
	# DK: to allow ansible to use a version in the guest os instead of needing one in the host OS, which does not work in Windows
	provisioner = Vagrant::Util::Platform.windows? ? :guest_ansible : :ansible
	# DK: actually do this manually below by using "guest_ansible" instead of "ansible" for the provisioner

	config.vm.provider "virtualbox" do |vb|
		vb.memory = "2048"
		vb.cpus = 2
		vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]		
	end
	
    config.vm.define "node1" do |node1|
        node1.vm.network "private_network", ip: "192.168.33.20"
        node1.vm.hostname = "node1"
        node1.vm.provision "guest_ansible", run: "always" do |ansible|
            ansible.playbook = "playbook.yml"
            ansible.groups = ANSIBLE_GROUPS
        end
    end

    config.vm.define "node2" do |node2|
        node2.vm.network "private_network", ip: "192.168.33.21"
        node2.vm.hostname = "node2"
        node2.vm.provision "guest_ansible", run: "always" do |ansible|
            ansible.playbook = "playbook.yml"
            ansible.groups = ANSIBLE_GROUPS
        end
    end

end
