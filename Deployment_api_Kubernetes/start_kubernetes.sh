#!/bin/bash
eval $(minikube -p minikube docker-env)
cd docker_container_api
docker image build . -t api_churn:latest
cd ..
minikube start
kubectl create -f my-deployment-project.yml
kubectl create -f my-secret-project.yml
kubectl create -f my-service-project.yml
kubectl create -f my-ingress-project.yml
minikube get pods
