import argparse
import csv
import os
from collections import defaultdict


class TrainRoutes:

    def __init__(self, routes: csv.DictReader) -> None:
        self.paths = defaultdict(list)
        self.times = {}
        self._generate_possible_paths(routes)

    def get_shortest_path(self, start: str, end: str) -> str:
        """Finding the shortest path from start to end.

        :param start: starting point
        :param end: ending point

        :return: message with information about the trip,
            including required time and amount of stops.
        """
        if start == end:
            return 'Start is the end, nowhere to go.'

        shortest_paths = {start: (None, 0)}
        current_station = start
        visited = set()

        while current_station != end:
            visited.add(current_station)
            destinations = self.paths[current_station]
            time_to_current_station = shortest_paths[current_station][1]

            for next_station in destinations:
                direction = (current_station, next_station)
                time = self.times[direction] + time_to_current_station
                time_to_station = (current_station, time)

                if next_station not in shortest_paths:
                    shortest_paths[next_station] = time_to_station
                else:
                    current_fastest_time = shortest_paths[next_station][1]
                    if current_fastest_time > time:
                        shortest_paths[next_station] = time_to_station

            next_destinations = {
                station: shortest_paths[station]
                for station in shortest_paths if station not in visited
            }
            if not next_destinations:
                return f'No routes from {start} to {end}.'

            current_station = min(
                next_destinations, key=lambda k: next_destinations[k][1]
            )

        total_stops = -2  # don't count start and end
        total_time = shortest_paths[current_station][1]
        while current_station is not None:
            total_stops += 1
            current_station = shortest_paths[current_station][0]

        stops = 'stop' if total_stops == 1 else 'stops'

        return (
            f'Your trip from {start} to {end} includes {total_stops} '
            f'{stops} and will take {total_time} minutes.'
        )

    def _generate_possible_paths(self, routes: csv.DictReader) -> None:
        """Convert routes to paths and times.

        :param routes: a DictReader object with rows as start, end and time
        """
        for route in routes:
            start, end, time = route.values()
            self.paths[start].append(end)
            self.paths[end].append(start)
            self.times[(start, end)] = int(time)
            self.times[(end, start)] = int(time)


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
