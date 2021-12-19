import argparse
import csv
import os
from collections import defaultdict, deque


class TrainRoutes:

    def __init__(self, routes: csv.DictReader) -> None:
        self.paths, self.times = self._generate_possible_paths(routes)

    def get_shortest_path(self, start: str, end: str) -> str:
        """Finding the shortest path from start to end.

        :param start: starting point
        :param end: ending point

        :return: message with information about the trip,
            including required time and amount of stops.
        """
        if start == end:
            return 'Start is the end, nowhere to go.'

        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            directions = self.paths.get(path[-1], [])

            for direction in directions:
                new_path = path.copy()
                new_path.append(direction)
                queue.append(new_path)

                if direction != end:
                    continue

                (
                    total_stops, total_time
                ) = self._get_overall_time_and_stops(new_path)
                stops = 'stop' if total_stops == 1 else 'stops'

                return (
                    f'Your trip from {start} to {end} includes {total_stops} '
                    f'{stops} and will take {total_time} minutes.'
                )

        return f'No routes from {start} to {end}.'

    def _get_overall_time_and_stops(self, path: list[str]) -> tuple[int, int]:
        """Calculate overall time and number of stops for the path.

        :param path: a list with path including all stops

        :return: a tuple of total stops and total time
        """
        path_len = len(path)
        total_stops = path_len - 2
        total_time = 0
        for i in range(path_len - 1):
            total_time += self.times[(path[i], path[i + 1])]

        return total_stops, total_time

    @staticmethod
    def _generate_possible_paths(routes: csv.DictReader) -> tuple[dict, dict]:
        """Convert routes to paths and times.

        :param routes: a DictReader object with rows as start, end and time

        :return: a tuple of paths and time
            paths: undirected graph, key as start and value as list
            with all possible directions.
            times: key as tuple with start - end and value as time
            to get from start to end.
        """
        paths = defaultdict(list)
        times = {}
        for route in routes:
            start, end, time = route.values()
            paths[start].append(end)
            times[(start, end)] = int(time)

        return paths, times


def validate_file(file_path: str) -> bool:
    if not file_path.endswith('.csv'):
        raise ValueError('File should have CSV format.')

    if not os.path.exists(file_path):
        raise ValueError('The file in this directory does not exist.')

    return True


def main(file_path: str, start: str, end: str) -> str:
    try:
        with open(file_path) as file:
            routes = csv.DictReader(
                file, delimiter=',', fieldnames=['start', 'end', 'time']
            )
            train_route = TrainRoutes(routes)
    except FileNotFoundError as e:
        return str(e)
    return train_route.get_shortest_path(start, end)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='path to csv file', type=str)
    args = parser.parse_args()
    file_path = args.file
    while not file_path:
        file_path = input('Please specify the path to CSV file: ')
    validate_file(file_path)

    start = end = ''
    while not start:
        start = input('What station are you getting on the train? ')
    while not end:
        end = input('What station are you getting off the train? ')

    print(main(file_path, start, end))
