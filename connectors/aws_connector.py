import boto3
from connectors.base_connector import BaseConnector

class AWSConnector(BaseConnector):
    def __init__(self,region='us-east-1'):
        super().__init__('AWS')
        self.client = boto3.client('ec2',region_name=region)

    def discover_vpcs(self):
        response = self.client.describe_vpcs()
        vpcs = []
        for vpc in response['Vpcs']:
            vpcs.append({
                'vpc_id': vpc['VpcId'],
                'cidr_block': vpc['CidrBlock'],
                'state': vpc['State'],
                'is_default': vpc['IsDefault']
            })
            return vpcs

    def discover_subnets(self):
        response = self.client.describe_subnets()
        subnets = []
        for subnet in response['Subnets']:
            subnets.append({
                'subnet_id': subnet['SubnetId'],
                'vpc_id': subnet['VpcId'],
                'cidr_block': subnet['CidrBlock'],
                'availability_zone': subnet['AvailabilityZone'],
                'state': subnet['State']
            })
        return subnets
        
    def health_check(self):
        try:
            self.client.describe_vpcs()
            return True
        except Execption:
            return False
