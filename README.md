# minikube-test

## Install

### Install Minikube

First, minikube had to be installed, below are the few steps required on a MAC desktop.

```
% brew install minikube

% minikube kubectl -- get po -A
```

### Install HyperKit in MAC

Then, the driver for minikube had to be installed.

I decide to use docker, but getting some issues when tried to connect to nginx below the error:

    `❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.`

Here a link with the error, and some folks there recommended to use HyperKit: 

    https://github.com/kubernetes/minikube/issues/9016

Then I move to install HyperKit, [here the documentation](https://minikube.sigs.k8s.io/docs/drivers/hyperkit/) 

### Start minikube using HyperKit driver

After the HyperKit install I started the minikube using that driver, previously deleted the previous minikube using docker.

```
% minikube start driver=hyperkit

😄  minikube v1.25.2 on Darwin 12.3.1
✨  Automatically selected the hyperkit driver
💾  Downloading driver docker-machine-driver-hyperkit:
    > docker-machine-driver-hyper...: 65 B / 65 B [----------] 100.00% ? p/s 0s
    > docker-machine-driver-hyper...: 8.35 MiB / 8.35 MiB  100.00% 5.37 MiB p/s
🔑  The 'hyperkit' driver requires elevated permissions. The following commands will be executed:

    $ sudo chown root:wheel /Users/vmax/.minikube/bin/docker-machine-driver-hyperkit 
    $ sudo chmod u+s /Users/vmax/.minikube/bin/docker-machine-driver-hyperkit 


Password:
💿  Downloading VM boot image ...
    > minikube-v1.25.2.iso.sha256: 65 B / 65 B [-------------] 100.00% ? p/s 0s
    > minikube-v1.25.2.iso: 237.06 MiB / 237.06 MiB [] 100.00% 6.20 MiB p/s 38s
👍  Starting control plane node minikube in cluster minikube
🔥  Creating hyperkit VM (CPUs=2, Memory=4000MB, Disk=20000MB) ...
🐳  Preparing Kubernetes v1.23.3 on Docker 20.10.12 ...
    ▪ kubelet.housekeeping-interval=5m
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

## Create the NGINX deployment

### Create

I used the below commmand to deploy nginx:

```
% kubectl run nginx --image=nginx:latest --port=80

pod/nginx created
```

Then, I exposed the port to connect from the localhost to test the nginx server:

```
% kubectl expose pod nginx  --type=NodePort

3service/nginx exposed
```

Lastly I get the url for connection, this step was the one failing when using docker driver:

```
% minikube service nginx --url

http://192.168.64.2:30239
```

## Get logs (`get-kubelogs.py`)

The script basically get the logs for any pod in kubernetes, it presents a menu with all the pods available not only for the namespace `default`, then select the pod and show the logs for that particular pod. Logs are shown like the `less` tool in linux, keys can be used to scroll the log text.

### Requirements

It was used a virtual environment with Python 3.8.8, and the required libraries are listed in the `requirements.txt` file inside the GitHub.

### Future features related to "show logs"

- Improves the menu
- Configure colors in logs to easily get information
- Configure regex to found errors and inform in the menu directly
- Filter pods with the most relevant