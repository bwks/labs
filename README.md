# labs
Repository for various labs based on the following topolgy.

[https://codingpackets.com/blog/network-lab-base/](https://codingpackets.com/blog/network-lab-base/)

#### Requirements
- python3.6+
- vagrant 2.1+
- vagrant-libvirt
- grifter
- napalm


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

Generate and apply config
``` 
lab-base --device-config --ssh-config --apply-config p1r1 p1r2 p1r3 p1r4 p1r5 p1r6 p1r7 p1r8 p1sw1
```

Reload baseline config
``` 
lab-base --reload-baseline p1r1 p1r2 p1r3 p1r4 p1r5 p1r6 p1r7 p1r8 p1sw1
```