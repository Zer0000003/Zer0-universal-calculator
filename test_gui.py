"""Headless tests for the GUI-to-engine boundary; no display server required."""
import subprocess
import unittest
from unittest.mock import patch

from gui import ROOT, compute


class ComputeTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(compute("2+3*4"), (True, "14"))

    def test_equation(self):
        self.assertEqual(compute("2x+7=19"), (True, "{6}"))

    def test_bad_input(self):
        ok, message = compute("2+")
        self.assertFalse(ok)
        self.assertTrue(message)

    @patch("gui.subprocess.run")
    def test_validation(self, run):
        self.assertFalse(compute("   ")[0])
        self.assertFalse(compute("1"*4097)[0])
        run.assert_not_called()

    @patch("gui.subprocess.run", side_effect=subprocess.TimeoutExpired("engine", 20))
    def test_timeout(self, run):
        self.assertFalse(compute("2+2")[0])
        self.assertEqual(run.call_args.kwargs["cwd"], ROOT)
        self.assertEqual(run.call_args.kwargs["timeout"], 20)

    @patch("gui.subprocess.run")
    def test_argument_vector(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="4\n", stderr="")
        self.assertEqual(compute("2+2"), (True, "4"))
        args, kwargs = run.call_args
        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0][2], "2+2")
        self.assertFalse(kwargs.get("shell", False))

    @patch("gui.subprocess.run")
    def test_output_limit(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="a"*30001, stderr="")
        ok, output = compute("1")
        self.assertTrue(ok)
        self.assertTrue(output.endswith("[Display truncated]"))


if __name__ == "__main__":
    unittest.main()
