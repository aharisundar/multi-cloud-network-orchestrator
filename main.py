from health_monitor import HealthMonitor
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
cost_summary = cost_analyzer.get_cost_summary()

print("\n=== COST ANALYSIS ===")
print(json.dumps(cost_summary, indent=2))

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f'reports/discovery_report_{timestamp}.json'

health_monitor = HealthMonitor(connectors)
health_status = health_monitor.check_health()

print("\n=== HEALTH STATUS ===")
print(json.dumps(health_status, indent=2))

full_report = {
    'discovery': report,
    'routing_findings': routing_findings,
    'cidr_overlap_findings': cidr_overlap_findings,
    'security_group_exposure_findings': sg_exposure_findings,
    'cost_summary': cost_summary,
    'health_status': health_status
}

with open(filename, 'w') as f:
    json.dump(full_report, f, indent=2)

print(f"\nReport saved to {filename}")