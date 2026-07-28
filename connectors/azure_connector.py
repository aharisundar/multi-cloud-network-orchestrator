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
    def discover_route_tables(self):
        return [
            {
                'route_table_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/routeTables/mock-rt-1',
                'vpc_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/virtualNetworks/mock-vnet-1',
                'routes': [
                    {
                        'destination': '0.0.0.0/0',
                        'target': 'Internet'
                    }
                ]
            }
        ]
    def discover_security_groups(self):
        return [
            {
                'group_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/networkSecurityGroups/mock-nsg-1',
                'group_name': 'mock-nsg-1',
                'vpc_id': '/subscriptions/mock-sub-id/resourceGroups/mock-rg/providers/Microsoft.Network/virtualNetworks/mock-vnet-1',
                'inbound_rules': [
                    {
                        'protocol': 'TCP',
                        'from_port': 443,
                        'to_port': 443
                    }
                ]
            }
        ]
             
    def health_check(self):
        return True