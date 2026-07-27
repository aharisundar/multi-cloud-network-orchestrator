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
                report[provider] = {
                    'status': 'healthy',
                    'vpc_count': len(vpcs),
                    'subnet_count': len(subnets),
                    'vpcs': vpcs,
                    'subnets': subnets
                }
            else:
                report[provider] = {
                    'status': 'unhealthy',
                    'vpc_count': 0,
                    'subnet_count': 0,
                    'vpcs': [],
                    'subnets': []
                }

        total_vpcs = sum(cloud['vpc_count'] for cloud in report.values())
        total_subnets = sum(cloud['subnet_count'] for cloud in report.values())
        healthy_clouds = [name for name, cloud in report.items() if cloud['status'] == 'healthy']
        unhealthy_clouds = [name for name, cloud in report.items() if cloud['status'] == 'unhealthy']

        summary = {
            'total_vpcs': total_vpcs,
            'total_subnets': total_subnets,
            'healthy_clouds': healthy_clouds,
            'unhealthy_clouds': unhealthy_clouds
        }

        return {'summary': summary, 'clouds': report}