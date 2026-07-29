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

    def check_cidr_overlaps(self):
        overlap_findings = []
        all_vpcs = []

        clouds = self.discovery_report['clouds']
        for provider, cloud_data in clouds.items():
            for vpc in cloud_data.get('vpcs', []):
                all_vpcs.append({
                    'provider': provider,
                    'vpc_id': vpc['vpc_id'],
                    'cidr_block': vpc['cidr_block']
                })

        for i in range(len(all_vpcs)):
            for j in range(i + 1, len(all_vpcs)):
                if all_vpcs[i]['cidr_block'] == all_vpcs[j]['cidr_block']:
                    overlap_findings.append({
                        'severity': 'warning',
                        'message': f"CIDR overlap: {all_vpcs[i]['provider']} VPC {all_vpcs[i]['vpc_id']} and {all_vpcs[j]['provider']} VPC {all_vpcs[j]['vpc_id']} both use {all_vpcs[i]['cidr_block']}"
                    })

        if not overlap_findings:
            overlap_findings.append({
                'severity': 'info',
                'message': 'No CIDR overlaps detected across clouds'
            })

        return overlap_findings

    def check_security_group_exposure(self):
        exposure_findings = []
        clouds = self.discovery_report['clouds']

        for provider, cloud_data in clouds.items():
            for sg in cloud_data.get('security_groups', []):
                for rule in sg['inbound_rules']:
                    protocol = rule.get('protocol', '')
                    from_port = rule.get('from_port', '')
                    if protocol == '-1' or from_port == 'N/A':
                        exposure_findings.append({
                            'severity': 'warning',
                            'provider': provider,
                            'group_id': sg['group_id'],
                            'message': f"Security group {sg['group_name']} allows all protocols/ports - review for over-permissive access"
                        })

        if not exposure_findings:
            exposure_findings.append({
                'severity': 'info',
                'message': 'No overly permissive security group rules detected'
            })

        return exposure_findings