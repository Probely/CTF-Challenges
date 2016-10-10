#!/bin/bash -e
#
# Provision Ubuntu VMs (vagrant shell provisioner).
#


if [ "$(id -u)" != "$(id -u ubuntu)" ]; then
    echo "The provisioning script must be run as the \"ubuntu\" user!" >&2
    exit 1
fi


echo "provision.sh: Customizing the base system..."

sudo DEBIAN_FRONTEND=noninteractive apt-get -qq update

#
# Updating the system requires a restart. If the "vagrant-vbguest" plugin is
# installed and the updates included the kernel package, this will trigger a
# reinstallation of the VirtualBox Guest Tools for the new kernel.
#
# Also, the "vagrant-reload" plugin may be used to ensure the VM is restarted
# immediately after provisioning, but it fails sometimes and I don't know why.
#
if [ "$SYSTEM_UPDATES" == "true" ]; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y install upgrade
    sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y autoremove
    echo "*** Updates have been installed. The guest VM should be restarted ASAP. ***" >&2
fi

sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
    avahi-daemon mlocate rsync lsof iotop htop \
    ntpdate pv tree vim screen tmux ltrace strace

# This is just a matter of preference...
sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y install netcat-openbsd
sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y purge netcat-traditional


# Set a local timezone (the default for Ubuntu boxes is GMT)...
sudo timedatectl set-timezone "Europe/Lisbon"

sudo systemctl -q enable systemd-timesyncd
sudo systemctl start systemd-timesyncd

# This gives us an easly reachable ".local" name for the VM...
sudo systemctl -q enable avahi-daemon 2>/dev/null
sudo systemctl start avahi-daemon

# Prevent locale from being forwarded from the host, causing issues...
if sudo grep -q '^AcceptEnv\s.*LC_' /etc/ssh/sshd_config; then
    sudo sed -i 's/^\(AcceptEnv\s.*LC_\)/#\1/' /etc/ssh/sshd_config
    sudo systemctl restart ssh
fi

# Generate the initial "locate" DB...
if sudo test -x /etc/cron.daily/mlocate; then
    sudo /etc/cron.daily/mlocate
fi

# Remove the spurious "you have mail" message on login...
if [ -s "/var/spool/mail/$USER" ]; then
    > "/var/spool/mail/$USER"
fi

# Make "vagrant ssh" sessions more comfortable by tweaking the
# configuration of some system utilities (eg. bash, vim, tmux)...
rsync -a --exclude=.DS_Store ~/shared/vagrant/skel/ ~/


echo "provision.sh: Running project-specific actions..."

# Install extra packages needed for the project...
sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
    git build-essential \
    python-dev virtualenv


# Install Docker for challenges that require sandboxing...
sudo apt-key adv --keyserver "hkp://p80.pool.sks-keyservers.net:80" --recv-keys "58118E89F3A912897C070ADBF76221572C52609D"
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

sudo DEBIAN_FRONTEND=noninteractive apt-get -qq update
sudo DEBIAN_FRONTEND=noninteractive apt-get -qq -y install docker-engine


echo "provision.sh: Done!"


# vim: set expandtab ts=4 sw=4:
