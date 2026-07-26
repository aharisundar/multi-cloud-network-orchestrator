from connectors.aws_connector import AWSConnector
from connectors.azure_connector import AzureConnector
from connectors.gcp_connector import GCPConnector
from discovery_engine import DiscoveryEngine
import json

connectors = [AWSConnector(), AzureConnector(), GCPConnector()]

engine = DiscoveryEngine(connectors)
report = engine.run_discovery()

print(json.dumps(report, indent=2))