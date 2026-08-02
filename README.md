# Multi-Cloud Network Orchestrator

A network discovery, routing analysis, cost estimation, and health monitoring tool built for AWS, Azure, and GCP — designed around a single, unified interface so the rest of the system doesn't need to know or care which cloud it's talking to.

Built as a hands-on project to demonstrate real-world cloud networking, Python software design, and DevOps practices: live API integration, defensive multi-cloud architecture, automated testing, containerization, and CI/CD.

## What it does

- **Discovery** — finds VPCs/VNets, subnets, route tables, and security groups/NSGs across all three clouds, and normalizes the results into one consistent format
- **Routing Optimization** — audits discovered route tables for missing default routes, duplicate CIDR entries, cross-cloud CIDR overlaps, and overly permissive security group rules
- **Cost Analysis** — estimates monthly cost per cloud using a transparent rate-card model, with an honest breakdown of what is and isn't actually billable
- **Health Monitoring** — checks connectivity/auth health across all three clouds and reports an overall system status
- **Reporting** — every run is saved as a timestamped JSON snapshot combining discovery, routing findings, cost estimate, and health status in one file

## Architecture

Every cloud connector (`AWSConnector`, `AzureConnector`, `GCPConnector`) inherits from a common `BaseConnector` interface, implementing the same four methods: `discover_vpcs()`, `discover_subnets()`, `discover_route_tables()`, `discover_security_groups()`, and `health_check()`. The `DiscoveryEngine`, `RoutingOptimizer`, `CostAnalyzer`, and `HealthMonitor` modules operate purely on this normalized data — none of them contain any cloud-specific logic. Adding a fourth cloud, or swapping a mock connector for a real one, requires no changes anywhere else in the system.

## Cloud connectivity status

| Cloud | Status | Notes |
|---|---|---|
| AWS | Live | Real boto3 integration against a free-tier account, using a least-privilege IAM user (describe-only permissions) |
| Azure | Live | Real Azure SDK integration via a service principal with Reader role, authenticated through `azure-identity` |
| GCP | Mocked | See note below |

### Why GCP is mocked

Google Cloud's "Secure by Default" organization policy blocks service account key creation on personal free-tier projects, and this project's account does not have Organization Policy Administrator access to override it — confirmed via both the console and `gcloud` CLI, both returning permission-denied on the same underlying IAM check. The alternative (Workload Identity Federation, or service account impersonation via an interactive OAuth device-code flow) is technically possible but was judged out of scope for this project's timeline. The `GCPConnector` returns realistic, correctly-shaped mock data so the rest of the system — discovery, routing checks, cost estimation — works identically whether the underlying data is real or mocked.

## Getting started

**Requirements:** Python 3.12, pip

```
pip install -r requirements.txt
```

**Environment variables** (for live AWS/Azure connectivity):

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

**Run it:**

```
python3 main.py
```

This runs discovery, routing analysis, cost estimation, and health checks across all three clouds, prints a full report to the console, and saves a timestamped JSON snapshot to `reports/`.

## Running with Docker

```
docker build -t multi-cloud-orchestrator .
docker run --env-file <(env | grep -E 'AWS_|AZURE_') multi-cloud-orchestrator
```

## Running tests

```
pytest test_routing_optimizer.py -v
```

Unit tests validate the routing optimizer's logic (missing default route detection, healthy route table validation) against self-contained fake data — no cloud credentials required. `test_connectors.py` is a separate manual integration script for validating live cloud connectivity and is not run as part of the automated test suite.

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on every push: installs dependencies, runs the unit test suite, and confirms the Docker image builds successfully.

## Project structure

```
connectors/
  base_connector.py       — abstract interface all connectors implement
  aws_connector.py        — real AWS integration (boto3)
  azure_connector.py      — real Azure integration (azure-identity, azure-mgmt-network)
  gcp_connector.py        — mocked GCP connector (see note above)
discovery_engine.py        — orchestrates discovery across all connectors
routing_optimizer.py       — analyzes route tables and security groups for issues
cost_analyzer.py           — estimates monthly cost per cloud
health_monitor.py          — checks connectivity health across all clouds
main.py                    — entry point, runs a full orchestrator cycle
test_routing_optimizer.py  — automated unit tests
test_connectors.py         — manual integration test script (requires live credentials)
Dockerfile
requirements.txt
reports/                   — timestamped JSON snapshots from each run
```

## Author

Built by Hari Sundar A, a Senior Network Engineer with 18+ years of experience in network security and infrastructure, as a hands-on project demonstrating the transition from traditional network engineering into cloud and DevOps engineering.


