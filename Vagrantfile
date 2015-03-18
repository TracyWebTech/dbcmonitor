# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = ENV.fetch("VAGRANT_BOX", 'trusty64')
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  ips = YAML.load_file('config/development/ips.yaml')

  config.vm.define 'monitor' do |monitor|
    monitor.vm.hostname = 'vagrant-monitor'
    monitor.vm.network 'private_network', ip: ips['monitor']
	monitor.vm.network :forwarded_port, guest: 8000, host: 8000 # (runserver)
    monitor.vm.provider "virtualbox" do |v|
      v.memory = 512
    end
  end

  config.vm.define 'replica1' do |replica1|
    replica1.vm.hostname = 'vagrant-replica1'
    replica1.vm.network 'private_network', ip: ips['replica1']
    replica1.vm.provider "virtualbox" do |v|
      v.memory = 512
    end
  end

  config.vm.define 'replica2' do |replica2|
    replica2.vm.hostname = 'vagrant-replica2'
    replica2.vm.network 'private_network', ip: ips['replica2']
    replica2.vm.provider "virtualbox" do |v|
      v.memory = 512
    end
  end
end

