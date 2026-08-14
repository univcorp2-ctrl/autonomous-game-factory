import json
import tempfile
import unittest
from pathlib import Path

from game_factory.autopilot import run_batch
from game_factory.feedback import learn_preferences
from game_factory.generator import generate_project
from game_factory.ideation import generate_ideas
from game_factory.qa import quality_score


class FactoryTests(unittest.TestCase):
    def test_ideas_are_generated(self):
        ideas = generate_ideas(8, 42)
        self.assertEqual(len(ideas), 8)
        self.assertTrue(all(x.mode in {"survivor", "dodger", "collector"} for x in ideas))

    def test_project_generation_and_qa(self):
        with tempfile.TemporaryDirectory() as td:
            spec = generate_ideas(1, 7)[0]
            project = generate_project(spec, td)
            result = quality_score(project)
            self.assertTrue(result.ok, result.errors)
            self.assertTrue((project / "marketing" / "store-copy.md").exists())

    def test_batch_is_bounded(self):
        with tempfile.TemporaryDirectory() as td:
            result = run_batch(9, 3, 99, td)
            self.assertEqual(result["kept"], 3)
            self.assertEqual(len(result["portfolio"]), 3)

    def test_feedback_learning(self):
        with tempfile.TemporaryDirectory() as td:
            metrics = Path(td) / "metrics.csv"
            metrics.write_text(
                "slug,mode,wishlists,conversion_rate,positive_review_rate,median_playtime_minutes,refund_rate\n"
                "a,survivor,1000,0.12,0.9,60,0.02\n"
                "b,dodger,100,0.03,0.7,10,0.08\n",
                encoding="utf-8",
            )
            out = Path(td) / "prefs.json"
            prefs = learn_preferences(metrics, out)
            self.assertGreater(prefs["mode_weights"]["survivor"], prefs["mode_weights"]["dodger"])


if __name__ == "__main__":
    unittest.main()
