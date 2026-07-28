from connectors.base_connector import BaseConnector

class GCPConnector(BaseConnector):
    def __init__(self):
        super().__init__('GCP')

    def discover_vpcs(self):
        return [
            {
                'vpc_id': 'projects/mock-project/global/networks/mock-vpc-1',
                'cidr_block': '10.128.0.0/20',
                'state': 'READY',
                'is_default': False
            }
        ]
    def discover_subnets(self):
        return [
            {
                'subnet_id': 'projects/mock-project/regions/us-central1/subnetworks/mock-subnet-1',
                'vpc_id': 'projects/mock-project/global/networks/mock-vpc-1',
                'cidr_block': '10.128.1.0/24',
                'availability_zone': 'us-central1',
                'state': 'READY'
            }
        ]
    def discover_route_tables(self):
        return [
            {
                'route_table_id': 'projects/mock-project/global/routes/mock-route-1',
                'vpc_id': 'projects/mock-project/global/networks/mock-vpc-1',
                'routes': [
                    {
                        'destination': '0.0.0.0/0',
                        'target': 'default-internet-gateway'
                    }
                ]
            }
        ]
    def discover_security_groups(self):
        return [
            {
                'group_id': 'projects/mock-project/global/firewalls/mock-fw-1',
                'group_name': 'mock-fw-1',
                'vpc_id': 'projects/mock-project/global/networks/mock-vpc-1',
                'inbound_rules': [
                    {
                        'protocol': 'tcp',
                        'from_port': 443,
                        'to_port': 443
                    }
                ]
            }
        ]
              
    def health_check(self):
        return True