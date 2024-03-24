helm upgrade --install blogchart .
helm upgrade --install blogchart . --set postgresql.auth.postgresPassword=qwerty123

helm uninstall blogchart
kubectl get pods

kubectl logs -f blogchart-0 blogchart-celery
kubectl exec -it blogchart-0 sh
kubectl describe pods blogchart-0

kubectl delete pvc data-blogchart-postgresql-0
