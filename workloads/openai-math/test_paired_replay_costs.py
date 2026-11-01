"""Closed-form sampling arithmetic controls; never native performance evidence."""
import math
import unittest
from estimate_paired_replay_costs import paired_band, total_part


class PairedArithmetic(unittest.TestCase):
    def test_census_has_exact_totals(self):
        b, q, ratio = paired_band([(2, [(2., 1.), (6., 3.)])])
        self.assertEqual((b["estimate"], q["estimate"]), (8., 4.))
        self.assertEqual((b["variance"], q["variance"]), (0., 0.))
        self.assertEqual((ratio["estimate"], ratio["low"], ratio["high"]), (.5, .5, .5))

    def test_covariance_cancels_for_proportional_pairs(self):
        b, q, ratio = paired_band([(100, [(2., 1.), (6., 3.)])])
        self.assertGreater(b["variance"], 0.)
        self.assertGreater(q["variance"], 0.)
        self.assertEqual(ratio["variance"], 0.)

    def test_nonproportional_hand_variance(self):
        _, _, ratio = paired_band([(100, [(1., 2.), (3., 2.)])])
        self.assertEqual(ratio["estimate"], 1.)
        self.assertTrue(math.isclose(ratio["variance"], .245, rel_tol=1e-12))

    def test_population_weights_not_unweighted_observations(self):
        b, q, ratio = paired_band([
            (100, [(1., 2.), (3., 2.)]),
            (20, [(10., 1.), (20., 2.)]),
        ])
        self.assertEqual((b["estimate"], q["estimate"]), (500., 230.))
        self.assertEqual(ratio["estimate"], .46)

    def test_invalid_sampling_size(self):
        with self.assertRaises(ValueError):
            total_part(1, [1., 2.])


if __name__ == "__main__":
    unittest.main()
