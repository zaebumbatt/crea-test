import unittest

from main import main, validate_file

correct_results = [
    ('A', 'B',
     'Your trip from A to B includes 0 stops and will take 5 minutes.'),
    ('B', 'A',
     'Your trip from B to A includes 0 stops and will take 5 minutes.'),
    ('A', 'C',
     'Your trip from A to C includes 1 stop and will take 10 minutes.'),
    ('C', 'A',
     'Your trip from C to A includes 1 stop and will take 10 minutes.'),
    ('E', 'J',
     'Your trip from E to J includes 2 stops and will take 30 minutes.'),
    ('J', 'E',
     'Your trip from J to E includes 2 stops and will take 30 minutes.'),
    ('A', 'D',
     'Your trip from A to D includes 0 stops and will take 15 minutes.'),
    ('D', 'A',
     'Your trip from D to A includes 0 stops and will take 15 minutes.'),
    ('A', 'J', 'No routes from A to J.'),
    ('A', 'A', 'Start is the end, nowhere to go.'),
]


class TestTrainRoutes(unittest.TestCase):

    def test_correct_results(self):
        file_path = 'routes.csv'
        for start, end, msg in correct_results:
            with self.subTest():
                self.assertEqual(main(file_path, start, end), msg)

    def test_file_validation(self):
        # correct case
        self.assertTrue(validate_file('routes.csv'))

        # invalid format
        with self.assertRaisesRegex(
                ValueError, 'File should have CSV format.'
        ):
            validate_file('routes.json')

        # invalid path
        with self.assertRaisesRegex(
                ValueError, 'The file in this directory does not exist.'
        ):
            validate_file('random_dir/routes.csv')
