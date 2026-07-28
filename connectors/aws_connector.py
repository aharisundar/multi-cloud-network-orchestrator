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
    def discover_route_tables(self):
        response = self.client.describe_route_tables()
        route_tables = []
        for rt in response['RouteTables']:
            routes = []
            for route in rt['Routes']:
                routes.append({
                    'destination': route.get('DestinationCidrBlock', 'N/A'),
                    'target': route.get('GatewayId', route.get('NatGatewayId', 'local'))
                })
            route_tables.append({
                'route_table_id': rt['RouteTableId'],
                'vpc_id': rt['VpcId'],
                'routes': routes
            })
        return route_tables
    
    def discover_security_groups(self):
        response = self.client.describe_security_groups()
        security_groups = []
        for sg in response['SecurityGroups']:
            inbound_rules = []
            for rule in sg['IpPermissions']:
                inbound_rules.append({
                    'protocol': rule.get('IpProtocol', 'N/A'),
                    'from_port': rule.get('FromPort', 'N/A'),
                    'to_port': rule.get('ToPort', 'N/A')
                })
            security_groups.append({
                'group_id': sg['GroupId'],
                'group_name': sg['GroupName'],
                'vpc_id': sg['VpcId'],
                'inbound_rules': inbound_rules
            })
        return security_groups
        
    def health_check(self):
        try:
            self.client.describe_vpcs()
            return True
        except Execption:
            return False
