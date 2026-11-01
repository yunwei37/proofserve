"""Response contract for matched target-only checker costs; no native execution."""
import json
import unittest
from native_no_memory_option import accepted_replay


class ReplayContract(unittest.TestCase):
    def setUp(self):
        self.good = [
            {"event": "accept", "module": "X.Y", "mutation": "none"},
            {"event": "one_complete", "parts": 1},
        ]

    def encode(self, events):
        return "\n".join(json.dumps(x) for x in events)

    def test_exact_completed_target(self):
        self.assertTrue(accepted_replay(self.encode(self.good), "X.Y")[0])

    def test_incomplete_wrong_or_malformed_is_not_acceptance(self):
        cases = [
            [], self.good[:1], self.good[1:],
            [{"event": "reject", "module": "X.Y"}, self.good[1]],
            [{"event": "accept", "module": "X.Z", "mutation": "none"}, self.good[1]],
            [{"event": "accept", "module": "X.Y", "mutation": "bvar"}, self.good[1]],
            self.good + [self.good[0]],
            [self.good[0], {"event": "one_complete", "parts": 0}],
            [self.good[0], {"event": "one_complete", "parts": True}],
            [self.good[0], {"event": "one_complete", "parts": "1"}],
            [None, None], [[], []], [1, 2],
        ]
        for case in cases:
            with self.subTest(case=case):
                self.assertFalse(accepted_replay(self.encode(case), "X.Y")[0])

    def test_non_json_native_failure_is_not_acceptance(self):
        self.assertFalse(accepted_replay("INTERNAL PANIC\n" + self.encode(self.good), "X.Y")[0])


if __name__ == "__main__":
    unittest.main()
