class RoutingOptimizer:
    def __init__(self, discovery_report):
        self.discovery_report = discovery_report

    def analyze(self):
        findings = {}
        clouds = self.discovery_report['clouds']

        for provider, cloud_data in clouds.items():
            provider_findings = []
            route_tables = cloud_data.get('route_tables', [])

            for rt in route_tables:
                rt_id = rt['route_table_id']
                vpc_id = rt['vpc_id']
                routes = rt['routes']

                has_default_route = any(r['destination'] == '0.0.0.0/0' for r in routes)
                if not has_default_route:
                    provider_findings.append({
                        'severity': 'warning',
                        'route_table_id': rt_id,
                        'vpc_id': vpc_id,
                        'message': 'No default route (0.0.0.0/0) found - this VPC may have no internet path'
                    })

                destinations = [r['destination'] for r in routes]
                duplicates = set([d for d in destinations if destinations.count(d) > 1])
                if duplicates:
                    provider_findings.append({
                        'severity': 'warning',
                        'route_table_id': rt_id,
                        'vpc_id': vpc_id,
                        'message': f'Duplicate destination CIDR(s) found: {duplicates}'
                    })

                if not provider_findings:
                    provider_findings.append({
                        'severity': 'info',
                        'route_table_id': rt_id,
                        'vpc_id': vpc_id,
                        'message': 'No issues found - route table looks healthy'
                    })

            findings[provider] = provider_findings

        return findings