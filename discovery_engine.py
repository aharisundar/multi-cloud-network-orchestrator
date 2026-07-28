class DiscoveryEngine:
    def __init__(self, connectors):
        self.connectors = connectors

    def run_discovery(self):
        report = {}
        for connector in self.connectors:
            provider = connector.provider_name
            if connector.health_check():
                vpcs = connector.discover_vpcs()
                subnets = connector.discover_subnets()
                route_tables = connector.discover_route_tables()
                report[provider] = {
                    'status': 'healthy',
                    'vpc_count': len(vpcs),
                    'subnet_count': len(subnets),
                    'route_table_count': len(route_tables),
                    'vpcs': vpcs,
                    'subnets': subnets,
                    'route_tables': route_tables
                }
            else:
                report[provider] = {
                    'status': 'unhealthy',
                    'vpc_count': 0,
                    'subnet_count': 0,
                    'route_table_count': 0,
                    'vpcs': [],
                    'subnets': [],
                    'route_tables': []
                }

        total_vpcs = sum(cloud['vpc_count'] for cloud in report.values())
        total_subnets = sum(cloud['subnet_count'] for cloud in report.values())
        total_route_tables = sum(cloud['route_table_count'] for cloud in report.values())
        healthy_clouds = [name for name, cloud in report.items() if cloud['status'] == 'healthy']
        unhealthy_clouds = [name for name, cloud in report.items() if cloud['status'] == 'unhealthy']

        summary = {
            'total_vpcs': total_vpcs,
            'total_subnets': total_subnets,
            'total_route_tables': total_route_tables,
            'healthy_clouds': healthy_clouds,
            'unhealthy_clouds': unhealthy_clouds
        }

        return {'summary': summary, 'clouds': report}