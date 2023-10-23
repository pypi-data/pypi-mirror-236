from unittest import TestCase

from prometheus_client import Counter, REGISTRY

from app.wrapper_kafka.prometheus import declare_basic_kafka_consumer_metrics, create_custom_counters


def unregister_metrics():
    for collector, names in tuple(
            REGISTRY._collector_to_names.items()):
        REGISTRY.unregister(collector)


class TestWrappersPrometheus(TestCase):
    def setUp(self) -> None:
        self.test_counter_name = 'test_name'
        self.test_counter_description = 'test_description'
        self.counters_tuple = [(self.test_counter_name, self.test_counter_description)]
        self.default_metric_names = ['inspected_messages', 'consumer_exceptions', 'wrong_message']
        unregister_metrics()

    def tearDown(self) -> None:
        unregister_metrics()

    def test_create_custom_metrics(self):
        custom_counters = create_custom_counters(self.counters_tuple)

        for c in custom_counters:
            self.assertIsInstance(c, Counter)
            self.assertEqual(c._name, self.test_counter_name)
            self.assertEqual(c._documentation, self.test_counter_description)

    def test_basic_metrics_are_declared(self):
        self.counters = [c for c in declare_basic_kafka_consumer_metrics()]
        self.assertEqual(len(self.counters), 3)

        for c in self.counters:
            self.assertIsInstance(c, Counter)

        for c in self.counters:
            self.assertTrue(c._name in self.default_metric_names)
