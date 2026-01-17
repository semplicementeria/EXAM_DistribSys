# K0s installation


Follow the first steps from [official guide](https://k0sproject.io/)
```bash
curl -sSf https://get.k0s.sh | sudo sh
sudo k0s install controller --single
sudo k0s start
```

and wait for all the containers to become ready

If you want you can enable also the autocompletion of commands (guide [here](https://docs.k0sproject.io/v1.23.6+k0s.2/shell-completion/))
---
# Deploy your first pod! #

```bash
k0s kubectl apply -f nginx-pod.yaml
```
the complete API documentation on Pods can be found [here](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/)

---

# Pods are hard to manage, let's use a deployment instead #

```bash
k0s kubectl apply -f nginx-dep.yaml
```
the complete API documentation on Deployments can be found [here](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/)

___

# Let's expose our deployment #

```bash
k0s kubectl apply -f nginx-svc.yaml
```
the complete API documentation on Services can be found [here](https://kubernetes.io/docs/reference/kubernetes-api/service-resources/service-v1/)

___

# Hint

You can use other pods to check the cluster's internal connectivity

```bash
k0s kubectl apply -f nettools-pod.yaml
```

___

# What if we want to pass some configurations to the pods?

```bash
k0s kubectl apply -f nginx-config-map
```






