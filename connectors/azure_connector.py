from connectors.base_connector import BaseConnector

class AzureConnector(BaseConnector):
    def __init__(self):
        super().__init__('Azure')

    def discover_vpcs(self):
        return [
            {
                'vpc_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/virtualNetworks/mock-vnet-1',
                'cidr_block': '10.0.0.0/16',
                'state': 'Succeeded',
                'is_default': False
            }
        ]
    def discover_subnets(self):
        return [
            {
                'subnet_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/virtualNetworks/mock-vnet-1/subnets/mock-subnet-1',
                'vpc_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/virtualNetworks/mock-vnet-1',
                'cidr_block': '10.0.1.0/24',
                'availability_zone': 'eastus-1',
                'state': 'Succeeded'
            }
        ]
        
    def health_check(self):
        return True