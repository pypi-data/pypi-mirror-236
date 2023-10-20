import asyncio
from typing import Iterable
import faust

from prometheus_client.core import GaugeMetricFamily
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import Collector


class AsyncioCollector(Collector):
    def collect(self) -> Iterable[Metric]:
        loop = asyncio.get_event_loop()

        yield GaugeMetricFamily('python_asycnio_loops', 'Count of active asyncio loops', 1)
        yield GaugeMetricFamily('python_asycnio_tasks', 'Count of active asyncio tasks', len(asyncio.all_tasks(loop)))


class FaustCollector(Collector):
    def __init__(self, faust_app: faust.App) -> None:
        self.faust_app = faust_app

    def collect(self) -> Iterable[Metric]:
        m = self.faust_app.monitor

        yield GaugeMetricFamily(
            'max_avg_history',
            'Max number of total run time values to keep to build average',
            m.max_avg_history,
        )
        yield GaugeMetricFamily(
            'max_commit_latency_history',
            'Max number of commit latency numbers to keep',
            m.max_commit_latency_history,
        )
        yield GaugeMetricFamily(
            'max_send_latency_history',
            'Max number of send latency numbers to keep',
            m.max_send_latency_history,
        )
        yield GaugeMetricFamily(
            'max_assignment_latency_history',
            'Max number of assignment latency numbers to keep',
            m.max_assignment_latency_history,
        )

        yield GaugeMetricFamily(
            'messages_active',
            'Number of messages currently being processed',
            m.messages_active,
        )

        yield GaugeMetricFamily(
            'messages_received',
            'Number of messages processed in total',
            m.messages_received_total,
        )

        yield GaugeMetricFamily(
            'messages_s',
            'Number of messages being processed this second',
            m.messages_s,
        )

        yield GaugeMetricFamily(
            'messages_sent',
            'Number of messages sent in total',
            m.messages_sent,
        )

        c = GaugeMetricFamily('messages_sent_by_topic', 'Number of messages sent in total by topic', labels=['topic'])

        for topic, value in m.messages_sent_by_topic.items():
            c.add_metric([topic], value)

        yield c

        c = GaugeMetricFamily('messages_received_BY_TOPIC', 'Number of messages processed in total', labels=['topic'])

        for topic, value in m.messages_received_by_topic.items():
            c.add_metric([topic], value)

        yield c
