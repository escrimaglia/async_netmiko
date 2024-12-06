# Async Netmiko Test

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

### Running as script

Note: To connect to the devices, I configured SSH Bastion Host on my Mac.

From your CLI execute the following:

- `python3 sync_serv.py` demonstrates synchronous operations.
- `python3 async_serv.py` demonstrates asynchronous operations.

#### SSH JumpHost configuration

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

### Running as an API endpoint

I configured a FastAPI project with two endpoints:

- `/api/v1/netmiko/async` demonstrates asynchronous operations.
- `/api/v1/netmiko/sync` demonstrates synchronous operations.

To launch the application, execute the following command in your CLI:

- `uvicorn controller:app --reload`
- `localhost:8000/docs`

This project demonstrates how to integrate asynchronous Netmiko operations within an HTTP server using FastAPI. The uvicorn server is utilized as it supports both synchronous and asynchronous programming, showcasing FastAPI’s flexibility for network automation tasks.

### Results

#### Test time for five devices and two commands per device

Output sync netmiko: {'result': 'Tiempo total: 0:00:30.678405'}  
Output async netmiko: {'result': 'Tiempo total: 0:00:07.157979'}  

Hope this helps in your automation journey  

Ed Scrimaglia
  