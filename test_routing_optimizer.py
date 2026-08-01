from routing_optimizer import RoutingOptimizer

def test_detects_missing_default_route():
    fake_report = {
        'clouds': {
            'TestCloud': {
                'route_tables': [
                    {
                        'route_table_id': 'rt-test',
                        'vpc_id': 'vpc-test',
                        'routes': [
                            {'destination': '10.0.0.0/16', 'target': 'local'}
                        ]
                    }
                ]
            }
        }
    }
    optimizer = RoutingOptimizer(fake_report)
    findings = optimizer.analyze()
    assert findings['TestCloud'][0]['severity'] == 'warning'
    assert 'default route' in findings['TestCloud'][0]['message']

def test_healthy_route_table_passes():
    fake_report = {
        'clouds': {
            'TestCloud': {
                'route_tables': [
                    {
                        'route_table_id': 'rt-test',
                        'vpc_id': 'vpc-test',
                        'routes': [
                            {'destination': '0.0.0.0/0', 'target': 'igw-test'}
                        ]
                    }
                ]
            }
        }
    }
    optimizer = RoutingOptimizer(fake_report)
    findings = optimizer.analyze()
    assert findings['TestCloud'][0]['severity'] == 'info'