"""Exact finite-population arithmetic controls, not native timing observations."""
import itertools
import statistics
import unittest
from analyze_precision import conditional_cell

class ConditionalRemainderTests(unittest.TestCase):
    def test_exact_srs_unbiased_total_and_variance(self):
        known, remainder = [2.,8.], [1.,3.,5.,9.]
        population = len(known)+len(remainder)
        draws = list(itertools.combinations(remainder,2))
        cells = [conditional_cell(population,known,list(x)) for x in draws]
        truth = sum(known)+sum(remainder)
        self.assertAlmostEqual(statistics.mean(x["estimate"] for x in cells),truth)
        actual_variance = statistics.mean((x["estimate"]-truth)**2 for x in cells)
        self.assertAlmostEqual(statistics.mean(x["variance"] for x in cells),actual_variance)
        naive = [population*statistics.mean(known+list(x)) for x in draws]
        self.assertNotAlmostEqual(statistics.mean(naive),truth)

    def test_full_remainder_is_census(self):
        c = conditional_cell(6,[2.,8.],[1.,3.,5.,9.])
        self.assertEqual(c["estimate"],28.)
        self.assertEqual(c["variance"],0.)

    def test_single_non_census_draw_has_no_variance_estimate(self):
        with self.assertRaises(ValueError):
            conditional_cell(6,[2.,8.],[1.])

    def test_invalid_draw_count(self):
        for fresh in [[],[1.,2.,3.]]:
            with self.assertRaises(ValueError):
                conditional_cell(3,[2.],fresh)

if __name__ == "__main__":
    unittest.main()
