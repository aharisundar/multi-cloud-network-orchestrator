from cost_analyzer import CostAnalyzer
from connectors.aws_connector import AWSConnector
from connectors.azure_connector import AzureConnector
from connectors.gcp_connector import GCPConnector
from discovery_engine import DiscoveryEngine
from routing_optimizer import RoutingOptimizer
import json
from datetime import datetime

connectors = [AWSConnector(), AzureConnector(), GCPConnector()]

engine = DiscoveryEngine(connectors)
report = engine.run_discovery()

print("=== DISCOVERY REPORT ===")
print(json.dumps(report, indent=2))

optimizer = RoutingOptimizer(report)
routing_findings = optimizer.analyze()

print("\n=== ROUTING OPTIMIZATION FINDINGS ===")
print(json.dumps(routing_findings, indent=2))

cidr_overlap_findings = optimizer.check_cidr_overlaps()

print("\n=== CIDR OVERLAP FINDINGS ===")
print(json.dumps(cidr_overlap_findings, indent=2))

sg_exposure_findings = optimizer.check_security_group_exposure()

print("\n=== SECURITY GROUP EXPOSURE FINDINGS ===")
print(json.dumps(sg_exposure_findings, indent=2))

cost_analyzer = CostAnalyzer(report)
cost_findings = cost_analyzer.estimate_costs()

print("\n=== COST ANALYSIS ===")
print(json.dumps(cost_findings, indent=2))

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f'reports/discovery_report_{timestamp}.json'

with open(filename, 'w') as f:
    json.dump(report, f, indent=2)

print(f"\nReport saved to {filename}")