
Contains all files necessary to deploy api with Kubernetes within 3 pods.

start_kubernetes.sh is a script that:

1) build the docker image containing api_churn; 
2) Made it available locally to kubernets
3) create the deployment,service,ingress dnd secrets after starting minikube
