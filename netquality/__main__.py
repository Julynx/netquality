#!/usr/bin/env python3
"""
@file     netquality
@brief    Benchmark your internet connection.
@date     14/12/2023
@author   Julio Cabria
"""

import os
import sys

import speedtest
from match_func import match
from string_grab import grab_all
from pythonping import ping

# https://i.stack.imgur.com/9UVnC.png
GREEN = "\033[92m"  # Bright green
RED = "\033[91m"  # Bright red
BLUE = "\033[96m"  # Bright cyan
YELLOW = "\033[93m"  # Bright yellow
RESET = "\033[0m"  # Reset to default color

COUNT = 50


class NetworkTest:
    def __init__(self) -> None:
        self._ping_results = None
        self._speedtest_results = None

    def _ping(self):
        if self._ping_results is not None:
            return self._ping_results

        ping_output = ping(target="8.8.8.8", count=COUNT, interval=0.2, timeout=2)

        self._packet_loss = (
            ping_output.stats_packets_sent - ping_output.stats_packets_returned
        ) / COUNT
        self._ping_results = "".join(str(r) for r in ping_output._responses)
        return self._ping_results

    def _speedtest(self):
        if self._speedtest_results is not None:
            return self._speedtest_results

        try:
            test = speedtest.Speedtest()
            test.get_best_server()
            test.download()
            test.upload(pre_allocate=False)
        except speedtest.ConfigRetrievalError as e:
            print(e)
            sys.exit(1)

        self._speedtest_results = test.results.dict()
        return self._speedtest_results

    @property
    def packet_loss(self):
        return round(self._packet_loss, 2)

    @property
    def jitter(self):
        times = [float(time) for time in grab_all(self._ping(), start=" in ", end="ms")]
        avg_time = sum(times) / len(times)
        differences = [abs(value - avg_time) for value in times]
        return round(sum(differences) / len(differences), 2)

    @property
    def upload(self):
        raw_upload = self._speedtest()["upload"]
        return round(raw_upload / 1000000, 2)

    @property
    def download(self):
        raw_download = self._speedtest()["download"]
        return round(raw_download / 1000000, 2)

    @property
    def ping(self):
        raw_ping = self._speedtest()["ping"]
        return round(raw_ping, 2)


class ResultsTable:
    def __init__(self, test) -> None:
        assert isinstance(test, NetworkTest)
        self._test = test
        self._rating = None

        self._download_color = None
        self._upload_color = None
        self._ping_color = None
        self._jitter_color = None
        self._packet_loss_color = None
        self._rating_color = None

    def __repr__(self) -> str:
        self._compute_rating()

        upl_col = self._upload_color
        dwl_col = self._download_color
        png_col = self._ping_color
        jit_col = self._jitter_color
        pkt_col = self._packet_loss_color
        rat_col = self._rating_color

        upl = self._test.upload
        dwl = self._test.download
        png = self._test.ping
        jit = self._test.jitter
        pkt = self._test.packet_loss
        rat = self._rating

        return (
            f"   Download: {dwl_col}{dwl}{RESET} Mbps\n"
            f"     Upload: {upl_col}{upl}{RESET} Mbps\n"
            f"       Ping: {png_col}{png}{RESET} ms\n"
            f"     Jitter: {jit_col}{jit}{RESET} ms\n"
            f"Packet loss: {pkt_col}{pkt}{RESET} %\n"
            f"     Rating: {rat_col}{rat}{RESET}\n"
        )

    def _compute_rating(self):
        def get_rating(color, rating_dict):
            return match(color, rating_dict)

        self._download_color = match(
            self._test.download,
            {range(0, 50): RED, range(50, 100): YELLOW, range(100, 500): GREEN},
            default=BLUE,
        )

        self._upload_color = match(
            self._test.upload,
            {range(0, 25): RED, range(25, 50): YELLOW, range(50, 250): GREEN},
            default=BLUE,
        )

        self._ping_color = match(
            self._test.ping,
            {range(0, 20): BLUE, range(20, 50): GREEN, range(50, 100): YELLOW},
            default=RED,
        )

        self._jitter_color = match(
            self._test.jitter,
            {range(0, 5): BLUE, range(5, 10): GREEN, range(10, 20): YELLOW},
            default=RED,
        )

        self._packet_loss_color = match(
            self._test.packet_loss,
            {range(0, 1): BLUE, range(1, 3): GREEN, range(3, 6): YELLOW},
            default=RED,
        )

        rating_dict = {BLUE: 3, GREEN: 2, YELLOW: 1, RED: 0}

        weights = [0.15, 0.15, 0.2, 0.2, 0.3]
        ratings = [
            get_rating(color, rating_dict)
            for color in [
                self._download_color,
                self._upload_color,
                self._ping_color,
                self._jitter_color,
                self._packet_loss_color,
            ]
        ]

        global_rating = min(
            (round(sum(w * r for w, r in zip(weights, ratings)) / 3 * 100, 2)), 100
        )

        self._rating_color = match(
            global_rating,
            {
                range(0, 50): RED,  # D, E, F
                range(50, 65): YELLOW,  # C
                range(65, 90): GREEN,  # A, B
                range(90, 100): BLUE,  # S
            },
            default=RED,
        )

        self._rating = match(
            global_rating,
            {
                range(0, 15): "F",
                range(15, 35): "E",
                range(35, 50): "D",
                range(50, 65): "C",
                range(65, 75): "B",
                range(75, 90): "A",
                range(90, 100): "S",
            },
            default="F",
        )


def terminal_clear():
    """Clear the terminal screen with cross-platform support."""
    os.system("cls" if os.name == "nt" else "clear")


def main():
    terminal_clear()
    print("Testing connection quality, please wait...")
    test = NetworkTest()
    table = ResultsTable(test)
    table_str = str(table)
    terminal_clear()
    print(table_str)


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print()
        sys.exit(0)
