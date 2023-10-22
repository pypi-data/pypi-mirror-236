"""Tests for :mod:`pylegacy.shutil`."""

import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from pylegacy import os
from pylegacy.builtins import callable


class TestPyLegacyShutil(unittest.TestCase):
    """Unittest class for :mod:`pylegacy.shutil`."""

    def setUp(self):
        """Define the test scope variables."""

    @unittest.skipIf(sys.version_info[:2] >= (3, 3), reason="it exists")
    def test_which_missing(self):
        """Test that :func:`shutil.which` does not exist."""

        def test_callable():
            """Helper function."""
            # pylint: disable=no-name-in-module
            from shutil import which
            return which

        self.assertRaises(ImportError, test_callable)

    def test_pylegacy_which_available(self):
        """Test that :func:`pylegacy.shutil.which` is available."""

        def test_callable():
            """Helper function."""
            from pylegacy.shutil import which
            return which

        self.assertTrue(callable(test_callable()))

    def test_pylegacy_which_python(self):
        """Test :func:`pylegacy.shutil.which` with a valid executable."""

        from pylegacy.shutil import which

        result = which("python")
        expected = sys.executable
        self.assertIsNot(result, None)
        self.assertEqual(result if os.name != "nt" else result.lower(),
                         expected if os.name != "nt" else expected.lower())

    def test_pylegacy_which_python_and_empty_path(self):
        """Test :func:`pylegacy.shutil.which` with empty path."""

        from pylegacy.shutil import which

        result = which("python", path="")
        self.assertIs(result, None)

    def test_pylegacy_which_python_with_absolute_path(self):
        """Test :func:`pylegacy.shutil.which` with absolute executable path."""

        from pylegacy.shutil import which

        result = which(sys.executable)
        expected = sys.executable
        self.assertEqual(result, expected)

    def test_pylegacy_which_nonexisting_executable(self):
        """Test :func:`pylegacy.shutil.which` with an invalid executable."""

        from pylegacy.shutil import which

        result = which("a_non_existing_executable_anywhere")
        self.assertIs(result, None)


if __name__ == "__main__":
    unittest.main()
