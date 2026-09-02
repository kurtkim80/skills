# NetworkPolicy and Gateway API patterns

Concrete manifests for default-deny network policies and modern Kubernetes Gateway API routing.
Copy and adapt these patterns.

## Contents

- Default-deny all traffic (Ingress and Egress)
- Fine-grained Service-to-Service allow policy
- Allow DNS egress and scoped external CIDR
- Gateway API: GatewayClass and Gateway
- Gateway API: HTTPRoute with path and header routing

## Default-deny all traffic (Ingress and Egress)

Apply this to every namespace to enforce a zero-trust baseline. All unlisted ingress and egress
traffic will be dropped by compliant CNIs (Cilium, Calico).

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

## Fine-grained Service-to-Service allow policy

Explicitly permits traffic to the `backend` service only from pods labeled `app: frontend` in
the same namespace, on TCP port 8080.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

## Allow DNS egress and scoped external CIDR

Permits pods to perform CoreDNS queries over UDP/TCP port 53 and reach external payment gateway
IPs without opening unrestricted egress to the internet.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-and-payment-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: checkout
  policyTypes:
    - Egress
  egress:
    # Allow DNS resolution within kube-system
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
    # Allow egress to external payment provider CIDR
    - to:
        - ipBlock:
            cidr: 198.51.100.0/24
      ports:
        - protocol: TCP
          port: 443
```

## Gateway API: GatewayClass and Gateway

The cluster operator defines the `Gateway` infrastructure entrypoint, decoupled from application
routing rules.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-gateway
  namespace: infra
spec:
  gatewayClassName: envoy-gateway
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: wildcard-tls-cert
      allowedRoutes:
        namespaces:
          from: Selector
          selector:
            matchLabels:
              env: production
```

## Gateway API: HTTPRoute with path and header routing

Application teams attach `HTTPRoute` objects to the shared Gateway without needing cluster-admin
privileges, supporting clean prefix matching and header injection.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-service-route
  namespace: production
spec:
  parentRefs:
    - name: production-gateway
      namespace: infra
  hostnames:
    - "api.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /v2/orders
          headers:
            - name: X-Client-Version
              value: "2"
      backendRefs:
        - name: orders-v2-svc
          port: 8080
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: core-api-svc
          port: 8080
```

