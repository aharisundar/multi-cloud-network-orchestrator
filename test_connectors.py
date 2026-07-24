from connectors.aws_connector import AWSConnector
from connectors.azure_connector import AzureConnector
from connectors.gcp_connector import GCPConnector

aws = AWSConnector()
print("AWS VPCs:", aws.discover_vpcs())
print("AWS health:", aws.health_check())

azure = AzureConnector()
print("Azure VPCs:", azure.discover_vpcs())
print("Azure health:", azure.health_check())

gcp = GCPConnector()
print("GCP VPCs:", gcp.discover_vpcs())
print("GCP health:", gcp.health_check())