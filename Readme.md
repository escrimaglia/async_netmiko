# Async Netmico Test

![plot](imagen/netmiko.png)

## IaC - Infraestructure as Code

It refers to the practice of managing and provisioning computing infrastructure (such as servers, networks, and databases) through code and automation rather than through manual processes. This allows infrastructure to be treated the same way as application code, enabling it to be versioned, tested, and deployed using software development practices.

### Network Automation

As part of IaC, Network Automation refers to the use of software to automatically manage, configure, test, deploy, and operate network devices and services. It replaces manual tasks with programmatic workflows and scripts, reducing human intervention, minimizing errors, and increasing efficiency in network management.

This approach is increasingly important in modern networking, especially in large-scale environments such as cloud infrastructures, data centers, and enterprise networks.

### Async Netmiko

Async Netmiko is a repository that contains tests I have conducted to differentiate the performance between running Netmiko synchronously versus asynchronously.

The outputs directory contains the results of each test, and as can be observed, the results are notably different.

To run the test, I used the EVE Pro simulator deployed on Google Cloud, a lab with five Cisco IOS devices and each host connection runs in a different thread.

To connect to the devices, I configured SSH Bastion Host on my Mac.

### SSH JumpHost configuration

SSH Configuration file for netmiko & bastion host

host jumphost  
  IdentityFile ~/.ssh/id_rsa  
  IdentitiesOnly yes  
  user xxxx  
  hostname xxxx.octupus.com  

host 10.2.0.* !jumphost  
  ProxyCommand ssh -F ~/.ssh/config -W %h:%p jumphost  

host 10.2.0.*  
  KexAlgorithms +diffie-hellman-group1-sha1  
  Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc  
  HostKeyAlgorithms=+ssh-dss  

### Results

#### Test time for five devices and two commands per device

Test time sync netmiko: 0:00:30.881254  
Test time async netmiko: 0:00:06.516488  

Hope this helps in your automation journey  

#### Ed Scrimaglia
  