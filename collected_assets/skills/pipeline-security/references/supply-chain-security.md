# Supply chain security patterns

Concrete CI/CD patterns for action pinning, keyless container signing, Software Bill of Materials
(SBOM) generation, and SLSA provenance generation.

## Contents

- Pin third-party actions by full commit SHA
- Keyless image signing with Sigstore Cosign via OIDC
- SBOM generation and vulnerability scanning (Syft + Grype)
- SLSA provenance generation

## Pin third-party actions by full commit SHA

Never reference mutable release tags (`@v4` or `@main`). Tags can be moved or compromised. Pin to
an exact immutable commit SHA with a comment indicating the tag version.

```yaml
steps:
  # Good: pinned by SHA with tag comment
  - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
  - uses: actions/setup-node@60edb5dd545a775178f5252478332d7967cb8615 # v4.0.2
    with:
      node-version: "20"
```

## Keyless image signing with Sigstore Cosign via OIDC

Use GitHub Actions OIDC identity token to sign container images without managing long-lived private
signing keys.

```yaml
jobs:
  build-and-sign:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write # Required for Sigstore OIDC keyless signing
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - uses: sigstore/cosign-installer@59acb6260d9c0ba8f4a2f9d9b4764742234e7440 # v3.5.0

      - name: Build container image
        run: |
          docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
          docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Sign container image
        run: |
          cosign sign --yes ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## SBOM generation and vulnerability scanning (Syft + Grype)

Generate a SPDX / CycloneDX SBOM during CI and fail the build if critical unpatched CVEs are
present.

```yaml
      - name: Generate SBOM with Syft
        uses: anchore/sbom-action@f325610c9f50a54015d37c8d535d74388689ab10 # v0.15.11
        with:
          image: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Scan SBOM with Grype
        uses: anchore/scan-action@3343887d815d7b07461f6fdcd195dbb63345007b # v3.6.4
        with:
          sbom: sbom.spdx.json
          fail-build: true
          severity-cutoff: high
```

## SLSA provenance generation

Attach non-forgeable SLSA Level 3 build provenance to verify the exact Git commit, builder, and
workflow that produced the artifact.

```yaml
  provenance:
    needs: [build-and-sign]
    permissions:
      actions: read
      id-token: write
      contents: write
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v2.0.0
    with:
      base64-subjects: "${{ needs.build-and-sign.outputs.digests }}"
      upload-assets: true
```

