from dataclasses import dataclass
from typing import Optional, List

import csv
import os


class Episode:
    serie: str
    season: int
    episode: int

    def __init__(self, serie: str, name: str, season: int, episode: int):
        self.serie = serie
        self._name = name
        self.season = season
        self.episode = episode

    @property
    def season_and_episode(self):
        return f"Seizoen { self.season } Aflevering { self.episode }"

    @property
    def icon(self):
        pass

    @property
    def icon_color(self):
        pass

    @property
    def name(self):
        return f"Chicago { self._name } department"

    @property
    def label(self):
        return f"{ self.serie } | S{ self.season } E{ self.episode }"


class PDEpisode(Episode):
    def __init__(self, season: int, episode: int):
        super().__init__("PD", "Police", season, episode)

    @property
    def icon_color(self):
        return "blue"

    @property
    def icon(self):
        return "mdi:police-badge"


class MedEpisode(Episode):
    def __init__(self, season: int, episode: int):
        super().__init__("Med", "Medical", season, episode)

    @property
    def icon_color(self):
        return "yellow"

    @property
    def icon(self):
        return "mdi:ambulance"


class FireEpisode(Episode):
    def __init__(self, season: int, episode: int):
        super().__init__("Fire", "Fire", season, episode)

    @property
    def icon_color(self):
        return "red"

    @property
    def icon(self):
        return "mdi:fire-truck"


class LawAndOrderEpisode(Episode):
    def __init__(self, season: int, episode: int):
        super().__init__("LawAndOrder", "Law and Order", season, episode)

    @property
    def icon_color(self):
        return "brown"

    @property
    def icon(self):
        return "mdi:gavel"

    @property
    def name(self):
        return self._name


def get_years():
    script_dir = os.path.dirname(__file__)
    return sorted(
        [file.split(".csv")[0] for file in os.listdir(f"{script_dir}/episode_lists")]
    )


def get_data(year):
    script_dir = os.path.dirname(__file__)
    with open(f"{script_dir}/episode_lists/{year}.csv", "r") as f:
        data = list(csv.reader(f, delimiter=","))

    options = []
    for row in data:
        type = row[1]
        season_episode = row[2].split("x")
        season = int(season_episode[0])
        episode_number = int(season_episode[1])

        if type == "Fire":
            episode = FireEpisode(season=season, episode=episode_number)
        elif type == "Med":
            episode = MedEpisode(season=season, episode=episode_number)
        elif type == "PD":
            episode = PDEpisode(season=season, episode=episode_number)
        elif type == "Law & Order: SVU":
            episode = LawAndOrderEpisode(season=season, episode=episode_number)

        options.append(episode)

    data = ChicagoData(options)
    return data


class ChicagoData:
    all_options: list[str]
    selected_option: str
    selected_option_obj: Episode

    def __init__(self, options):
        self.all_options = {option.label: option for option in options}
        self.selected_option_obj = options[0]
        self.selected_option = self.selected_option_obj.label

    @property
    def options_list(self):
        return list(self.all_options.keys())

    def set_option(self, option):
        self.selected_option_obj = self.all_options[option]
        self.selected_option = option
