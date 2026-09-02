# OpenTelemetry Collector configuration

Production-ready OpenTelemetry Collector configuration template with tail sampling, batching,
memory limiting, and sensitive attribute redaction.

## Contents

- Complete collector pipeline configuration (YAML)
- Memory limiter and buffer sizing rules
- Tail-based sampling policies (errors, high latency, probabilistics)
- Sensitive attribute redaction and masking

## Complete collector pipeline configuration (YAML)

Save this configuration as `otel-collector-config.yaml` for an OpenTelemetry Collector gateway.

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  memory_limiter:
    check_interval: 1s
    limit_percentage: 75
    spike_limit_percentage: 20

  batch:
    send_batch_size: 8192
    timeout: 5s
    send_batch_max_size: 16384

  # Sensitive data redaction
  transform:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - replace_pattern(attributes["http.url"], "token=[^&]+", "token=REDACTED")
          - replace_pattern(attributes["http.url"], "api_key=[^&]+", "api_key=REDACTED")

  # Tail sampling: retain errors and slow requests, sample baseline traffic
  tail_sampling:
    decision_wait: 10s
    num_traces: 10000
    expected_new_traces_per_sec: 2000
    policies:
      # Always keep traces containing errors
      - name: sample-errors
        type: status_code
        status_code: { status_codes: [ERROR] }

      # Always keep high-latency traces (> 1.5s)
      - name: sample-slow-requests
        type: latency
        latency: { threshold_ms: 1500 }

      # Retain 5% of healthy baseline traffic
      - name: sample-probabilistic
        type: probabilistic
        probabilistic: { sampling_percentage: 5.0 }

exporters:
  otlp/traces:
    endpoint: tempo-distributor.monitoring.svc.cluster.local:4317
    tls:
      insecure: true

  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: otelcol

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, transform, tail_sampling, batch]
      exporters: [otlp/traces]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
  telemetry:
    logs:
      level: "info"
    metrics:
      address: "0.0.0.0:8888"
```

## Memory limiter and buffer sizing rules

The `memory_limiter` processor must always precede stateful processors like `tail_sampling` and
`batch` in the pipeline order.

- Set `limit_percentage: 75` of the container's hard memory limit to prevent `OOMKilled` events
  during traffic spikes.
- Set `decision_wait` in `tail_sampling` to be slightly larger than your longest expected trace
  duration (e.g. 10s–30s) so spans from slow services arrive before the sampling decision is made.
- Scale collector replicas using Horizontal Pod Autoscaling based on memory utilization and
  incoming span volume.

