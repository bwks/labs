# labs
Repository for various labs based on the following topolgy.

[https://codingpackets.com/blog/network-lab-base/](https://codingpackets.com/blog/network-lab-base/)

#### Requirements
- python3.6+
- vagrant 2.1+
- vagrant-libvirt
- grifter
- nornir


### Build Base Lab

Create working directory and environment
``` 
mkdir path/to/some/dir && cd path/to/some/dir
python3.6 -m venv .venv
source .venv/bin/activate
```

Install required packages
```
pip install -r requirements.txt
pip install -U https://github.com/bobthebutcher/labs/archive/master.zip
```

Create Vagrantfile 
``` 
git clone git@github.com:bobthebutcher/labs.git
grifter create guests.yml
```

Build Vagrant guests. Below a regex is used to bring 
up only the guests in pod 1.
``` 
vagrant up /^p1/
```

Generate configuration and sshconfig files.
``` 
lab-config --device-config --ssh-config
```

Apply base configurations
```
lab-config --apply-config base
```

Save baseline configuration
```
lab-config --save-config
```

Apply feature configurations
```
lab-config --apply-config isis
```

Reload baseline config. 
``` 
# This will load the last saved configuration.
lab-base --reload-baseline
```