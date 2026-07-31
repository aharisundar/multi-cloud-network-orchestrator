class CostAnalyzer:
    RATE_CARD = {
        'vpc': 0.0,
        'subnet': 0.0,
        'route_table': 0.0,
        'security_group': 0.0,
        'nat_gateway_estimate': 32.0,
        'elastic_ip_unused_estimate': 3.6
    }

    def __init__(self, discovery_report):
        self.discovery_report = discovery_report

    def estimate_costs(self):
        clouds = self.discovery_report['clouds']
        cost_summary = {}

        for provider, cloud_data in clouds.items():
            vpc_count = cloud_data.get('vpc_count', 0)
            subnet_count = cloud_data.get('subnet_count', 0)
            route_table_count = cloud_data.get('route_table_count', 0)
            security_group_count = cloud_data.get('security_group_count', 0)

            estimated_cost = (
                vpc_count * self.RATE_CARD['vpc'] +
                subnet_count * self.RATE_CARD['subnet'] +
                route_table_count * self.RATE_CARD['route_table'] +
                security_group_count * self.RATE_CARD['security_group']
            )

            cost_summary[provider] = {
                'estimated_monthly_cost_usd': round(estimated_cost, 2),
                'note': 'Estimate based on resource counts only - VPCs, subnets, route tables, and security groups themselves are free; actual cost depends on compute, storage, data transfer, and NAT/load balancer usage not yet discovered by this tool.',
                'resource_breakdown': {
                    'vpcs': vpc_count,
                    'subnets': subnet_count,
                    'route_tables': route_table_count,
                    'security_groups': security_group_count
                }
            }

        return cost_summary