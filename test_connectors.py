from connectors.aws_connector import AWSConnector
aws = AWSConnector()
print("AWS VPCs:", aws.discover_vpcs())
