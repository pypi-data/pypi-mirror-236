import unittest
import pandas as pd
from src.main import find_outliers


class TestOutliers(unittest.TestCase):
    def test_find_outliers(self):
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 1000],
                "col2": [20, 30, 40, 50, 60],
                "col3": [100, 200, 300, 400, 100000],
            }
        )

        expected = {"col1": [1000], "col3": [100000]}

        outliers = find_outliers(df)
        self.assertEqual(outliers, expected)


if __name__ == "__main__":
    unittest.main()
