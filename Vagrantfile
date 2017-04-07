# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

######################################################################
# Select whether to use a private or public network and choose the
# IP addresses to use for the master and agents.
#
# Set the 'public', 'mesos_master_ip' and 'agent_ips' variables
# to suit your needs:
######################################################################
public = false
#public = true

use_kubernetes = false
use_kubernetes = true

if public == true
	puts 'Using public network, with static IP addresses.'
	mesos_master_ip = "192.168.1.190"
	agent_ips = {
		'agent1' => '192.168.1.191',
		'agent2' => '192.168.1.192',
		'agent3' => '192.168.1.193',
		'agent4' => '192.168.1.194'
	}
	kube_ip = "192.168.1.189"
else
	puts 'Using private network.'
	mesos_master_ip = "192.168.33.20"
	agent_ips = {
		'agent1' => '192.168.33.21',
		'agent2' => '192.168.33.22',
		'agent3' => '192.168.33.23',
		'agent4' => '192.168.33.24',
	}
	kube_ip = "192.168.33.19"
end
puts agent_ips
######################################################################

ANSIBLE_GROUPS = {
              "master" => ["master"],
              "nodes" => agent_ips.keys,
			  "kube" => ["kube"],
              "all_groups:children" => ["master", "nodes", "kube"]
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
		if public == true
			master.vm.network "public_network", ip: mesos_master_ip
		else
			master.vm.network "private_network", ip: mesos_master_ip
		end
        master.vm.hostname = "master"
		master.vm.provider "virtualbox" do |vb|
			vb.cpus = 1
			vb.memory = "1024"
		end
		master.vm.provision "base", type: "guest_ansible" do |ansible|
			ansible.playbook = "playbook_base.yml"
			ansible.groups = ANSIBLE_GROUPS
			ansible.extra_vars = {
				master_ip: mesos_master_ip,
				agent_ips: agent_ips,
				kube_ip: kube_ip
			}
		end
		# vagrant provision master --provision-with initial
		master.vm.provision "initial", type: "guest_ansible" do |ansible|
			ansible.playbook = "playbook_initial.yml"
			ansible.groups = ANSIBLE_GROUPS
			ansible.extra_vars = {
				master_ip: mesos_master_ip,
				agent_ips: agent_ips,
				kube_ip: kube_ip
			}
		end
        master.vm.provision "guest_ansible", run: "always" do |ansible|
            ansible.playbook = "playbook.yml"
            ansible.groups = ANSIBLE_GROUPS
			ansible.extra_vars = {
				master_ip: mesos_master_ip,
				agent_ips: agent_ips
			}
        end
    end

	agent_ips.each do |host, ip|
		config.vm.define "#{host}" do |node|
			if public == true
				node.vm.network "public_network", ip: "#{ip}"
			else
				node.vm.network "private_network", ip: "#{ip}"
			end
			node.vm.hostname = "#{host}"
			node.vm.provider "virtualbox" do |vb|
				vb.cpus = 2
				vb.memory = "2042"
			end
			node.vm.provision "base", type: "guest_ansible" do |ansible|
				ansible.playbook = "playbook_base.yml"
				ansible.groups = ANSIBLE_GROUPS
				ansible.extra_vars = {
					master_ip: mesos_master_ip,
					agent_ips: agent_ips,
					kube_ip: kube_ip
				}
			end
			node.vm.provision "guest_ansible", run: "always" do |ansible|
				ansible.playbook = "playbook.yml"
				ansible.groups = ANSIBLE_GROUPS
				ansible.extra_vars = {
					master_ip: mesos_master_ip,
					agent_ips: agent_ips
				}
			end
		end
	end
	
	if use_kubernetes == true
		config.vm.define "kube" do |kube|
			if public == true
				kube.vm.network "public_network", ip: kube_ip
			else
				kube.vm.network "private_network", ip: kube_ip
			end
			kube.vm.hostname = "kube"
			kube.vm.provider "virtualbox" do |vb|
				vb.cpus = 1
				vb.memory = "1024"
			end
			kube.vm.provision "base", type: "guest_ansible" do |ansible|
			#kube.vm.provision "base", type: "guest_ansible", run: "always" do |ansible|
				ansible.playbook = "playbook_base.yml"
				ansible.groups = ANSIBLE_GROUPS
				ansible.extra_vars = {
					master_ip: mesos_master_ip,
					agent_ips: agent_ips,
					kube_ip: kube_ip
				}
			end
			# vagrant provision kube --provision-with initial
			kube.vm.provision "initial", type: "guest_ansible" do |ansible|
			#kube.vm.provision "initial", type: "guest_ansible", run: "always" do |ansible|
				ansible.playbook = "playbook_initial.yml"
				ansible.groups = ANSIBLE_GROUPS
				ansible.extra_vars = {
					master_ip: mesos_master_ip,
					agent_ips: agent_ips,
					kube_ip: kube_ip
				}
			end
			# playbook_always
			kube.vm.provision "guest_ansible", run: "always" do |ansible|
				ansible.playbook = "playbook.yml"
				ansible.groups = ANSIBLE_GROUPS
				ansible.extra_vars = {
					master_ip: mesos_master_ip,
					agent_ips: agent_ips
				}
			end
		end
	end
end
