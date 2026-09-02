# Kyverno and Rego policy patterns

Concrete policy definitions for Kubernetes admission control and Terraform plan validation using
Kyverno and Open Policy Agent (OPA) / Gatekeeper Rego.

## Contents

- Kyverno: Disallow privileged containers
- Kyverno: Enforce required resource limits and requests
- OPA Gatekeeper: Disallow privileged containers (ConstraintTemplate & Constraint)
- OPA / Conftest: Terraform plan validation for S3 bucket public access

## Kyverno: Disallow privileged containers

Blocks any pod where `securityContext.privileged` is set to `true`.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
  annotations:
    policies.kyverno.io/title: Disallow Privileged Containers
    policies.kyverno.io/category: Pod Security Standards (Baseline)
    policies.kyverno.io/severity: medium
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: check-privileged
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Privileged mode is prohibited on all containers."
        pattern:
          spec:
            =(ephemeralContainers):
              - =(securityContext):
                  =(privileged): "false"
            =(initContainers):
              - =(securityContext):
                  =(privileged): "false"
            containers:
              - =(securityContext):
                  =(privileged): "false"
```

## Kyverno: Enforce required resource limits and requests

Ensures every container specifies CPU and memory requests and limits.

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-requests-limits
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-resources
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "CPU and memory requests and limits are mandatory for all containers."
        pattern:
          spec:
            containers:
              - resources:
                  requests:
                    memory: "?*"
                    cpu: "?*"
                  limits:
                    memory: "?*"
                    cpu: "?*"
```

## OPA Gatekeeper: Disallow privileged containers (ConstraintTemplate & Constraint)

Gatekeeper uses a parameterized `ConstraintTemplate` holding Rego logic and a `Constraint` applying it.

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sdisallowprivileged
spec:
  crd:
    spec:
      names:
        kind: K8sDisallowPrivileged
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sdisallowprivileged

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          container.securityContext.privileged == true
          msg := sprintf("Container '%v' in pod '%v' cannot run in privileged mode", [container.name, input.review.object.metadata.name])
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sDisallowPrivileged
metadata:
  name: disallow-privileged
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces:
      - "production"
      - "staging"
```

## OPA / Conftest: Terraform plan validation for S3 bucket public access

Evaluates a `terraform show -json tfplan.binary` JSON output in CI before `terraform apply`.

```rego
package terraform.security

import future.keywords.in

default allow = false

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    resource.change.after.acl == "public-read"
    msg := sprintf("Resource '%v' has public-read ACL. All S3 buckets must be private.", [resource.address])
}

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    resource.change.after.block_public_acls == false
    msg := sprintf("Resource '%v' does not enforce block_public_acls = true.", [resource.address])
}
```

