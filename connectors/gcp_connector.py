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

    def health_check(self):
        return True