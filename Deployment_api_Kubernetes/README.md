
Contains all files necessary to deploy api with Kubernetes within 3 pods.

k8_settings_windows.sh is a script that:

1) build the docker image containing api_churn
2) made it available locally to kubernets
3) create the deployment,service,ingress and secrets after starting minikube
