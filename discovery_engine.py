class DiscoveryEngine:
    def __init__(self, connectors):
        self.connectors = connectors

    def run_discovery(self):
        report = {}
        for connector in self.connectors:
            provider = connector.provider_name
            if connector.health_check():
                vpcs = connector.discover_vpcs()
                report[provider] = {
                    'status': 'healthy',
                    'vpc_count': len(vpcs),
                    'vpcs': vpcs
                }
            else:
                report[provider] = {
                    'status': 'unhealthy',
                    'vpc_count': 0,
                    'vpcs': []
                }
        return report