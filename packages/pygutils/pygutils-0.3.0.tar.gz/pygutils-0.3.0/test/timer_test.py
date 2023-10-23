import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pygutils.timer import Timer


class TimerTest(TestCase):
    @patch("time.time", return_value=10)
    def test_can_get_current_time_in_milliseconds(self, time_mock: MagicMock):
        self.assertEqual(10000, Timer.current_ms_time())
        time_mock.assert_called_once()

    def test_can_activate_timer(self):
        with patch.object(Timer, "current_ms_time", return_value=1000) as mock:
            timer = Timer(1000, None)
            timer.activate()

            self.assertEqual(1000, timer.start_time)
            mock.assert_called_once()

    def test_timer_by_default_is_not_active(self):
        timer = Timer(1000, None)
        self.assertFalse(timer.active)

    def test_can_check_timer_activation_status(self):
        timer = Timer(1000, None)
        timer.activate()

        self.assertTrue(timer.active)

    def test_can_deactivate_timer(self):
        timer = Timer(1000, None)
        timer.activate()
        timer.deactivate()

        self.assertFalse(timer.active)

    def test_timer_is_deactivated_after_end(self):
        with patch.object(Timer, "current_ms_time", side_effect=[10, 20]) as mock:
            timer = Timer(10, None)
            timer.deactivate = MagicMock(return_value=None)

            timer.activate()
            timer.update()

            timer.deactivate.assert_called_once()
            mock.assert_called()

    def test_callback_is_called_after_timer_end(self):
        with patch.object(Timer, "current_ms_time", side_effect=[10, 20]) as mock:
            callback_mock = MagicMock(return_value=None)

            timer = Timer(10, callback_mock)
            timer.activate()
            timer.update()

            callback_mock.assert_called_once()
            mock.assert_called()


if __name__ == "__main__":
    unittest.main()
