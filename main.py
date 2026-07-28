from connectors.aws_connector import AWSConnector
from connectors.azure_connector import AzureConnector
from connectors.gcp_connector import GCPConnector
from discovery_engine import DiscoveryEngine
import json
from datetime import datetime

connectors = [AWSConnector(), AzureConnector(), GCPConnector()]

engine = DiscoveryEngine(connectors)
report = engine.run_discovery()

print(json.dumps(report, indent=2))

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f'reports/discovery_report_{timestamp}.json'

with open(filename, 'w') as f:
    json.dump(report, f, indent=2)

print(f"\nReport saved to {filename}")