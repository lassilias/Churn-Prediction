#!/bin/bash
# https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d
# To point your shell to minikube’s docker-daemon, run: 
eval $(minikube -p minikube docker-env)
# with this command we run locally built images in Kubernetes, without publishing them to a global registry.
cd docker_container_api
docker image build . -t api_churn:latest
cd ..
minikube start
kubectl create -f my-deployment-project.yml
kubectl create -f my-secret-project.yml
kubectl create -f my-service-project.yml
kubectl create -f my-ingress-project.yml
minikube get pods
minikube dashboard --url=True
