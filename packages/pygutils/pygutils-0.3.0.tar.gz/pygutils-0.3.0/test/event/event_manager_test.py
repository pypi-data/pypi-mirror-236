import unittest
from unittest.mock import MagicMock

from pygutils.event import EventManager


class TestListener:
    def notify(self, event: str, *args, **kwargs):
        pass


class EventManagerTest(unittest.TestCase):
    def test_can_subscribe_to_an_event(self):
        listener = TestListener()

        manager = EventManager()
        manager.subscribe("event:test", listener)

        self.assertTrue(listener in manager.listeners["event:test"])

    def test_cant_subscribe_a_object_that_isnt_a_listener(self):
        class NotHasNotifyMethod:
            pass

        with self.assertRaises(TypeError):
            manager = EventManager()
            manager.subscribe("event:test", NotHasNotifyMethod())

    def test_can_unsubscribe_from_an_event(self):
        listener = TestListener()

        manager = EventManager()
        manager.subscribe("event:test", listener)

        self.assertTrue(listener in manager.listeners["event:test"])

        manager.unsubscribe("event:test", listener)

        self.assertFalse(listener in manager.listeners["event:test"])

    def test_subscribers_are_notified(self):
        listener = MagicMock(spec=TestListener)

        manager = EventManager()
        manager.subscribe("event:test", listener)
        manager.notify("event:test", arg1=1, arg2=2)

        listener.notify.assert_called_once_with("event:test", arg1=1, arg2=2)

    def test_notify_only_correct_subscribers(self):
        listener1 = MagicMock(spec=TestListener)
        listener2 = MagicMock(spec=TestListener)

        manager = EventManager()
        manager.subscribe("event:test1", listener1)
        manager.subscribe("event:test2", listener2)
        manager.notify("event:test1")

        listener1.notify.assert_called_once()
        listener2.notify.assert_not_called()
