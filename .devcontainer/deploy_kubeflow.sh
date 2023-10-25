#!/bin/sh

# if kind cluster doesn't exists, create it
if [ -z "$(kind get clusters | grep kind)" ]; then
    kind create cluster
fi

# explicitely export configuration and set kubectl context
kind export kubeconfig
kubectl cluster-info --context kind-kind

# install kubeflow. Use version 2.0.1 instead of 2.0.2 to overcome some installation challenges
export PIPELINE_VERSION=2.0.1
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"


# wait for the ui pod to be up and running. Once done, the devcontainer will forward it such that it can be viewed on port 8080
while [[ $(kubectl get pods -l=app=ml-pipeline-ui --namespace=kubeflow -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
    echo "Waiting for pod"
    sleep 5
done
