from datetime import datetime

class HealthMonitor:
    def __init__(self, connectors):
        self.connectors = connectors

    def check_health(self):
        results = {}
        checked_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for connector in self.connectors:
            provider = connector.provider_name
            is_healthy = connector.health_check()
            results[provider] = {
                'status': 'healthy' if is_healthy else 'unhealthy',
                'checked_at': checked_at
            }

        total = len(results)
        healthy_count = sum(1 for r in results.values() if r['status'] == 'healthy')

        summary = {
            'checked_at': checked_at,
            'total_clouds': total,
            'healthy_count': healthy_count,
            'unhealthy_count': total - healthy_count,
            'overall_status': 'healthy' if healthy_count == total else 'degraded'
        }

        return {'summary': summary, 'clouds': results}