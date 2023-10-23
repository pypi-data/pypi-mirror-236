import unittest

from pygutils.event.event_listener import EventListener


class EventListenerTest(unittest.TestCase):
    def test_class_with_notify_method_is_a_valid_listener(self):
        class TestListener:
            def notify(self, event: str, *args, **kwargs):
                pass

        self.assertTrue(isinstance(TestListener(), EventListener))

    def test_class_without_notify_method_is_not_a_valid_listener(self):
        class TestListener:
            pass

        self.assertFalse(isinstance(TestListener(), EventListener))

    def test_class_with_notify_method_with_invalid_signature_is_not_a_valid_listener(
        self,
    ):
        class TestListener:
            def notify(self, event: str):
                pass

        self.assertFalse(isinstance(TestListener(), EventListener))


if __name__ == "__main__":
    unittest.main()
