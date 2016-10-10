# -*- mode: ruby -*-
#
# Vagrantfile - One development machine to rule them all.
#


# This is the minimum customization necessary but, to tailor this configuration
# to a specific project, you should also edit the "vagrant/provision.sh" script...
vm_name = "CTF Ubuntu 16.04"
vm_hostname = "vagrant-ctf"


# The box is assumed to be readily usable by default, but all available
# system updates can be installed during provisioning, if necessary...
install_system_updates = false


# Location of the external files used by this script...
vagrant_assets = File.dirname(__FILE__) + "/vagrant"


Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/xenial64"
    config.vm.hostname = vm_hostname

    # The Debian box defaults to using an rsynced folder...
    config.vm.synced_folder ".", "/vagrant", disabled: true

    # Because Ubuntu manages to produce broken builds that persist for days...
    config.vm.provision "shell", inline: "sudo ln -nsf ../run/resolvconf/resolv.conf /etc/resolv.conf",
                                 privileged: false, name: "fix resolv.conf symlink"

    # Support git operations inside the VM. The file provisioner requires files to exist,
    # which in this case is a good thing as it prevents commits attributed to wrong users...
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"

    # Perform base-system customizations and install project-specific dependencies...
    config.vm.provision "shell", path: "#{vagrant_assets}/provision.sh",
                                 env: {"INSTALL_SYSTEM_UPDATES" => install_system_updates.to_s},
                                 privileged: false  # ...run as the "ubuntu" user.

    # Immediately apply system updates, if possible...
    if install_system_updates and Vagrant.has_plugin?("vagrant-reload")
        config.vm.provision "reload"
    end

    #config.ssh.forward_agent = true
    config.ssh.keep_alive = true


    config.vm.provider "virtualbox" do |vm, override|
        vm.name = vm_name
        vm.gui = false

        vm.memory = 1024
        vm.cpus = 1

        # Prevent guest time from drifting uncontrollably on older hosts, even with
        # time synchronization running in the guest VM. If you have a fairly recent
        # machine this probably won't affect you and can be safely commented-out...
        vm.customize ["modifyvm", :id, "--paravirtprovider", "legacy"]

        # Override the console log location set by the base box...
        vm.customize ["modifyvm", :id, "--uart1", "0x3F8", "4" ]
        vm.customize ["modifyvm", :id, "--uartmode1", "file", File.join(vagrant_assets, "console.log")]

        # Expose the VM to the host instead of forwarding many ports individually
        # for complex projects. The provisioning script will setup Avahi/mDNS to
        # make the guest VM easily accessible through a "*.local" domain...
        override.vm.network "private_network", type: "dhcp"

        # Make the current directory visible (and editable) inside the VM...
        override.vm.synced_folder ".", "/home/ubuntu/shared"
    end
end


# vim: set expandtab ts=4 sw=4 ft=ruby:
