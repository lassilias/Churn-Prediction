#!/bin/bash
minikube start
# https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d
# To point your shell to minikube’s docker-daemon, run: 
eval $(minikube -p minikube docker-env)
# with this command we run locally built images in Kubernetes, without publishing them to a global registry.
cd docker_container_api
docker image build . -t api_churn:latest
cd ..
#kubectl delete namespaces ingress-nginx
export DOCKER_HOST=tcp://127.0.0.1:2375
myNamespace="ingress-nginx"
kubectl get namespace | grep -q "^$myNamespace " || kubectl apply -f config-ingress.yaml
kubectl config set-context --current --namespace=ingress-nginx
kubectl create -f my-deployment-project.yml
kubectl create -f my-secret-project.yml
kubectl create -f my-service-project.yml
kubectl create -f my-ingress-project.yml
#kubectl expose deployment my-api-project-churn-deployement --type=ClusterIP --port=8080
#kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
minikube service  my-api-project-churn-service -n ingress-nginx
#minikube service my-api-project-churn-deployement --url -n ingress-nginx
#minikube dashboard --url=True
