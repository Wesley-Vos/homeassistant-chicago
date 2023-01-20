from dataclasses import dataclass
from typing import Any, Optional, List

import csv
import os


class Episode:
    episode_id: int
    serie: str
    season: int
    episode: int

    def __init__(
        self, episode_id: int, serie: str, name: str, season: int, episode: int
    ):
        self.episode_id = episode_id
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
    def __init__(self, episode_id: int, season: int, episode: int):
        super().__init__(episode_id, "PD", "Police", season, episode)

    @property
    def icon_color(self):
        return "blue"

    @property
    def icon(self):
        return "mdi:police-badge"


class MedEpisode(Episode):
    def __init__(self, episode_id: int, season: int, episode: int):
        super().__init__(episode_id, "Med", "Medical", season, episode)

    @property
    def icon_color(self):
        return "yellow"

    @property
    def icon(self):
        return "mdi:ambulance"


class FireEpisode(Episode):
    def __init__(self, episode_id: int, season: int, episode: int):
        super().__init__(episode_id, "Fire", "Fire", season, episode)

    @property
    def icon_color(self):
        return "red"

    @property
    def icon(self):
        return "mdi:fire-truck"


class LawAndOrderEpisode(Episode):
    def __init__(self, episode_id: int, season: int, episode: int):
        super().__init__(episode_id, "LawAndOrder", "Law and Order", season, episode)

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

    episodes = []
    for row in data:
        episode_id = int(row[0])
        episode_type = row[1]
        season_episode = row[2].split("x")
        season = int(season_episode[0])
        episode_number = int(season_episode[1])

        if episode_type == "Fire":
            episode = FireEpisode(
                episode_id=episode_id, season=season, episode=episode_number
            )
        elif episode_type == "Med":
            episode = MedEpisode(
                episode_id=episode_id, season=season, episode=episode_number
            )
        elif episode_type == "PD":
            episode = PDEpisode(
                episode_id=episode_id, season=season, episode=episode_number
            )
        elif episode_type == "Law & Order: SVU":
            episode = LawAndOrderEpisode(
                episode_id=episode_id, season=season, episode=episode_number
            )

        episodes.append(episode)

    data = ChicagoData(episodes)
    return data


class ChicagoData:
    all_episodes: Any
    _all_episodes_keys: Any
    selected_episode: str
    selected_episode_idx: int
    selected_episode_obj: Episode

    def __init__(self, options):
        self.all_episodes = {option.label: option for option in options}
        self._all_episodes_keys = [option.label for option in options]
        self.set_episode(options[0].label)

    @property
    def episodes_lists(self):
        return list(self.all_episodes.keys())

    def set_episode(self, episode):
        self.selected_episode_obj = self.all_episodes[episode]
        self.selected_episode_idx = self._all_episodes_keys.index(episode)
        self.selected_episode = episode

    def next_episode(self):
        if self.selected_episode_idx + 1 >= len(self._all_episodes_keys):
            return

        self.selected_episode_idx += 1
        self.selected_episode = self._all_episodes_keys[self.selected_episode_idx]
        self.selected_episode_obj = self.all_episodes[self.selected_episode]

    def previous_episode(self):
        if self.selected_episode_idx - 1 < 0:
            return

        self.selected_episode_idx -= 1
        self.selected_episode = self._all_episodes_keys[self.selected_episode_idx]
        self.selected_episode_obj = self.all_episodes[self.selected_episode]
