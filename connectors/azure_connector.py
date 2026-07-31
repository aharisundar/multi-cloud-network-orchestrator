import os
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from connectors.base_connector import BaseConnector

class AzureConnector(BaseConnector):
    def __init__(self):
        super().__init__('Azure')
        self.credential = ClientSecretCredential(
            tenant_id=os.environ['AZURE_TENANT_ID'],
            client_id=os.environ['AZURE_CLIENT_ID'],
            client_secret=os.environ['AZURE_CLIENT_SECRET']
        )
        self.subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        self.client = NetworkManagementClient(self.credential, self.subscription_id)

    def discover_vpcs(self):
        vpcs = []
        for vnet in self.client.virtual_networks.list_all():
            vpcs.append({
                'vpc_id': vnet.id,
                'cidr_block': vnet.address_space.address_prefixes[0] if vnet.address_space.address_prefixes else 'N/A',
                'state': vnet.provisioning_state.value if hasattr(vnet.provisioning_state, 'value') else str(vnet.provisioning_state),
                'is_default': False
            })
        return vpcs

    def discover_subnets(self):
        subnets = []
        for vnet in self.client.virtual_networks.list_all():
            for subnet in vnet.subnets:
                subnets.append({
                    'subnet_id': subnet.id,
                    'vpc_id': vnet.id,
                    'cidr_block': subnet.address_prefix,
                    'availability_zone': 'N/A',
                    'state': subnet.provisioning_state
                })
        return subnets

    def discover_route_tables(self):
        route_tables = []
        for rt in self.client.route_tables.list_all():
            routes = []
            for route in (rt.routes or []):
                routes.append({
                    'destination': route.address_prefix,
                    'target': route.next_hop_type
                })
            route_tables.append({
                'route_table_id': rt.id,
                'vpc_id': 'N/A',
                'routes': routes
            })
        return route_tables

    def discover_security_groups(self):
        security_groups = []
        for nsg in self.client.network_security_groups.list_all():
            inbound_rules = []
            for rule in (nsg.security_rules or []):
                if rule.direction == 'Inbound':
                    inbound_rules.append({
                        'protocol': rule.protocol,
                        'from_port': rule.destination_port_range or 'N/A',
                        'to_port': rule.destination_port_range or 'N/A'
                    })
            security_groups.append({
                'group_id': nsg.id,
                'group_name': nsg.name,
                'vpc_id': 'N/A',
                'inbound_rules': inbound_rules
            })
        return security_groups

    def health_check(self):
        try:
            list(self.client.virtual_networks.list_all())
            return True
        except Exception:
            return False