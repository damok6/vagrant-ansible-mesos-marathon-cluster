

vagrant-ansible-mesos-marathon-cluster
====

A Mesos and Marathon cluster created with Vagrant, Virtualbox and Ansible that works on any host operating system.

Uses Ansible installed in the guest OS, so it does not require a host OS that supports Ansible. i.e. It can run on Windows without any software installed besides Vagrant and Virtualbox.

Most of this is based on the excellent [Mesosphere tutorials](https://open.mesosphere.com/advanced-course/recreating-the-cluster-using-ansible/), with some modifications to run on Ubuntu Virtual Machines instead of CentOS.


##Usage

This Vagrantfile uses Ansible to configure the Mesos master and Mesos agent Virtual Machines (VMs). It uses an Ansible installation in the guest OS so there is no need to install anything in the host OS besides Vagrant and VirtualBox.


### Prerequisites

This will work with most recent, mutually compatible, versions of Vagrant and VirtualBox. Most recently this configuration has been tested to work with the following components:
* VirtualBox 5.1.14
* Vagrant 1.9.1

Vagrant also requires the `guest_ansible` plugin, which if not already installed can be installed using:

```vagrant plugin install vagrant-guest_ansible```


### Running

TODO: Change all 'node' references to say 'agent'.

This script runs a single Mesos master and up to 4 Mesos agents. At present, it uses the Vagrant private network for cross-VM communication, so you will only be able to access the VMs from the host OS. The names of the guest VMs are `master`, `node1`, `node2`, `node3` and `node4`. Later we can bring all of the VMs up at once, but at first we should test a minimal cluster with one master and one agent node VM. 

You must first clone or download this repository to your computer and `cd` into the project's root directory. To bring up this minimal cluster you can tell the script to bring up only the Mesos master and the first Mesos agent by using the command. 

```vagrant up master node1```

This will take some time to provision the servers the first time it is run. When this completes, you can skip to the Testing section to test the minimal cluster or proceed to bring up the remaining Mesos agent VMs by using the command:

```vagrant up node2 node3 node4```

In the future, when you're sure everything works as expected, you can bring the entire cluster back up by using the command:

```vagrant up```

which will bring up all 5 VMs in the cluster at once.

When the cluster is successfully provisioned and running we can skip to testing the cluster as outlined in the next section.

### TODO: Public networking

Default should be private within-host networking, but show how public networking can be used.

### Testing

When the cluster is running we can use the web browser to view the Mesos-master page at the url:

<http://192.168.33.20:5050>

As you bring up applications they should appear here. To bring up applications, you can use the Marathon web interface available at:

<http://192.168.33.20:8080>

It should now be possible to run both Mesos and Docker containerized applications as described in the Mesosphere [Application Basics](https://mesosphere.github.io/marathon/docs/application-basics.html).


### Stopping or Destroying

If you wish to simply stop the cluster to start again later without needing to run the provisining process you can simply run:

```vagrant halt```

Or if you wish to stop a single VM to reduce memory consumption or to test cluster fail-over, you can run:

```vagrant halt node4```

to take down `node4` for example.

If you wish to permanently destroy all machines that make up the cluster you can run:

```vagrant destroy -f```

This will permanently remove all machines in the cluster and clear the hard drive space occupied by the VirtualBox images. If you take this option you will have to re-run the VM instanation process next time you run `vagrant up`, so make sure you are happy with this before destroying all VMs.

##Notes

###Marathon Load Balancer

TODO: Examples of how to use the load balancer.

###Guest Additions Issues

Occasionally when bringing back up a VM, you may encounter the error:

```
node1: /vagrant => C:/Users/Damian/Documents/Vagrant/ansible-mesos-vagrant-cluster
Vagrant was unable to mount VirtualBox shared folders. This is usually
because the filesystem "vboxsf" is not available. This filesystem is
made available via the VirtualBox Guest Additions and kernel module.
Please verify that these guest additions are properly installed in the
guest. This is not a bug in Vagrant and is usually caused by a faulty
Vagrant box. For context, the command attempted was:

mount -t vboxsf -o uid=1000,gid=1000 vagrant /vagrant

The error output from the command was:

: No such device
```

This can be due to the kernel being updated by the Docker installation to a version that is incompatible with the VBox Guest Additions.

This can be rectified by updating the Vagrant VM image using the command `vagrant box update`, then destroying and recreating the VMs again.

Alternatively you can install the [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) plugin which should ensure that up-to-date Guest Additions are built for the box when necessary.

##ToDos

Some items on the immediate horizon for this project are:

* [x] ~~Use vagrant hostmanager plugin to automatically update host OS list of hosts~~ Use only IP addresses for Mesos Agents rather than hostnames.
* [ ] Add Mesos-DNS (on master most likely)
* [x] Add Marathon Load Balancer
* [ ] Use Vagrant public IP address with optional switch
* [x] Change all nodes to be referred to as agents
