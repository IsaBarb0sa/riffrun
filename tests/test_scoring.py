import unittest

from riffrun.scoring import DUEL_STAR_THRESHOLDS, RunScore


class ScoringTests(unittest.TestCase):
    def test_defeat_awards_only_collected_riffs_and_freezes_time(self):
        run = RunScore()
        run.advance(25_000)
        result = run.finish(4, completed=False)
        run.advance(5000)
        self.assertEqual(result.total, 4000)
        self.assertEqual(result.time_bonus, 0)
        self.assertEqual(result.stars, 0)
        self.assertEqual(run.elapsed_ms, 25_000)

    def test_riffs_and_time_both_contribute(self):
        run = RunScore()
        run.advance(75_000)
        result = run.finish(8)
        self.assertEqual(result.riff_points, 8000)
        self.assertEqual(result.time_bonus, 1050)
        self.assertEqual(result.total, 9050)
        self.assertEqual(result.time_text, "01:15")

    def test_slow_completions_keep_riff_points_without_negative_bonus(self):
        run = RunScore()
        run.advance(240_000)
        result = run.finish(10)
        self.assertEqual(result.total, 10000)
        self.assertEqual(result.time_bonus, 0)

    def test_result_and_time_freeze_after_finish(self):
        run = RunScore()
        run.advance(20_000)
        result = run.finish(5)
        run.advance(90_000)
        self.assertIs(run.finish(10), result)
        self.assertEqual(run.elapsed_ms, 20_000)
        self.assertEqual(result.riffs, 5)

    def test_new_attempt_starts_from_zero(self):
        previous = RunScore()
        previous.advance(80_000)
        previous.finish(7)
        new = RunScore()
        self.assertEqual(new.elapsed_ms, 0)
        self.assertIsNone(new.result)

    def test_more_riffs_outweigh_small_time_differences(self):
        fast = RunScore()
        fast.advance(60_000)
        collector = RunScore()
        collector.advance(90_000)
        self.assertGreater(collector.finish(10).total, fast.finish(9).total)

    def test_campaign_star_thresholds_include_the_time_bonus(self):
        for riffs, elapsed, expected in ((5, 80_100, 1), (5, 80_000, 2),
                                          (9, 80_100, 2), (9, 80_000, 3)):
            with self.subTest(riffs=riffs, elapsed=elapsed):
                run = RunScore()
                run.advance(elapsed)
                self.assertEqual(run.finish(riffs).stars, expected)

    def test_duel_star_thresholds_use_the_victory_time(self):
        for elapsed, expected in ((120_100, 1), (120_000, 2), (60_100, 2), (60_000, 3)):
            with self.subTest(elapsed=elapsed):
                run = RunScore(star_thresholds=DUEL_STAR_THRESHOLDS)
                run.advance(elapsed)
                self.assertEqual(run.finish(0).stars, expected)
