VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.ssh.forward_agent = true

    config.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--memory", 4096]
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end

    config.vm.define "ubuntu" do |ubuntu|
        ubuntu.vm.hostname = "tisac"
        ubuntu.vm.box = "ubuntu/trusty64"
        ubuntu.vm.network :forwarded_port, guest: 9200, host: 9200
        ubuntu.vm.network :forwarded_port, guest: 5601, host: 5601
	ubuntu.vm.network :forwarded_port, guest: 5000, host: 5000
        ubuntu.vm.provision :shell, :path => "ubuntubootstrap.sh"
        ubuntu.vm.provision :shell, :path => "plugins.sh"
        ubuntu.vm.provider :virtualbox do |v|
            v.name = "T-ISAC"
        end
    end

   end
