# ghbin

Easily download and update github releases.

## Installation

```bash
git clone git@github.com:afriemann/ghbin
cd ghbin
pip install --user --upgrade .
```

## Usage

Currently only supports dumb installation

```bash
ghbin install
```

## Configure

```yaml
---
# ~/.config/ghbin/config.yaml

sources:
  - name: terragrunt
    repository: gruntwork-io/terragrunt
    asset: terragrunt_linux_amd64
  - name: kubesec
    repository: controlplaneio/kubesec
    asset: kubesec_linux_amd64.tar.gz
    extract:
      - kubesec
  - name: saml2aws
    repository: versent/saml2aws
    version: v2.22.0
    asset: saml2aws_2.22.0_linux_amd64.tar.gz
    extract:
      - saml2aws
  - name: ksniff
    repository: eldadru/ksniff
    asset: ksniff.zip
    extract:
      - kubectl-sniff
      - static-tcpdump
  - name: kubectx
    repository: aca/go-kubectx
    version: v0.1.0
    asset: go-kubectx_0.1.0_Linux_x86_64.tar.gz
    extract:
      - kubectx
      - kubens
  - name: kubectl-doctor
    repository: emirozer/kubectl-doctor
    asset: kubectl-doctor_linux_amd64.zip
    extract:
      - kubectl-doctor
  - name: kubectl-resources
    repository: howardjohn/kubectl-resources
    version: v0.1.0
    asset: kubectl-resources_0.1.0_Linux_x86_64.tar.gz
    extract:
      - kubectl-resources
```

## Issues

See [ISSUES.md](ISSUES.md)

