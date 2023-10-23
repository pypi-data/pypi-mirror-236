import unittest
from unittest.mock import MagicMock

from pygame.surface import Surface
from parameterized import parameterized

from pygutils.animation import Animation


class AnimationTest(unittest.TestCase):
    animation_frames: list[Surface] = [
        Surface((10, 10)),
        Surface((20, 20)),
    ]

    def test_can_get_finished_status_from_animation(self):
        animation = Animation(self.animation_frames, 1)

        animation.index = 1
        self.assertFalse(animation.finished)

        animation.index = 2
        self.assertTrue(animation.finished)

    def test_can_retrieve_next_frame(self):
        animation = Animation(self.animation_frames, 1)
        animation.index = 0

        self.assertEqual(animation.next(), self.animation_frames[0])

    def test_can_reset_animation(self):
        animation = Animation(self.animation_frames, 1)
        animation.index = 1

        animation.reset()

        self.assertEqual(animation.index, 0)

    def test_update_do_nothing_for_finished_animation_that_isnt_a_loop(self):
        animation = Animation(self.animation_frames, 1, loop=False)
        animation.index = 1

        animation.update(1)

        self.assertEqual(animation.finished, True)
        self.assertEqual(animation.index, 2)

    def test_update_reset_finished_animation_when_it_is_a_loop(self):
        animation = Animation(self.animation_frames, 1)
        animation.index = 1

        animation.update(1)

        self.assertEqual(animation.finished, False)
        self.assertEqual(animation.index, 0)

    def test_call_callback_on_animation_finish(self):
        callback_mock = MagicMock(return_value=None)

        animation = Animation(self.animation_frames, 1, on_finish=callback_mock)
        animation.index = 1

        animation.update(1)

        callback_mock.assert_called_once()

    @parameterized.expand([(10, 0.02, 0.2), (10, 0.15, 1.5), (10, 0.1, 1)])
    def test_update_animation_index_relative_to_animation_speed_and_delta_time(
        self, animation_speed: int, delta_time: float, expected_index: float
    ):
        animation = Animation(self.animation_frames, animation_speed)
        animation.update(delta_time)

        self.assertEqual(animation.index, expected_index)

    def test_animation_can_make_a_copy_of_himself(self):
        animation = Animation(self.animation_frames, 1)
        animation.index = 1

        animation_copy = animation.copy()

        self.assertEqual(animation.loop, animation_copy.loop)
        self.assertEqual(animation.on_finish, animation_copy.on_finish)
        self.assertListEqual(animation.frames_sequence, animation_copy.frames_sequence)
        self.assertEqual(animation.animation_speed, animation_copy.animation_speed)
        self.assertEqual(0, animation_copy.index)
