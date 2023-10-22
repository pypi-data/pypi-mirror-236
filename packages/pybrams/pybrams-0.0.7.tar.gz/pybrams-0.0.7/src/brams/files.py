from __future__ import annotations
from types import NoneType
from typing import Any, Dict, Literal, Optional
import json_fix # type: ignore
import os
import json
import requests
from . import systems
from .wav import Wav
from .signal import Signal
from .pps import PPS
from .api import base_url
from .cache import Cache

endpoint = f"{base_url}/file.php"


class File:

    def __init__(self, year: int, month: int, day: int, hours: int, minutes: int, sample_rate: float,
                 pps_count: int, duration: int, precise_start: int, precise_end: int, system_code: str,
                 location_code: str, location_url: str, system_url: str, wav_url: str, wav_name: str, png_url: str,
                 png_name: str, beacon_frequency: Optional[float] = None):

        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hours: int = hours
        self.minutes: int = minutes
        self.sample_rate: float = sample_rate
        self.pps_count: int = pps_count
        self.duration: int = duration
        self.precise_start: int = precise_start
        self.precise_end: int = precise_end
        self.system_code: str = system_code
        self.location_code: str = location_code
        self.location_url: str = location_url
        self.system_url: str = system_url
        self.wav_url: str = wav_url
        self.wav_name: str = wav_name
        self.png_url: str = png_url
        self.png_name: str = png_name
        self.beacon_frequency: Optional[float] = beacon_frequency

        self.system: Optional[systems.System] = None
        self.signal: Optional[Signal] = None

        self.corrected_wav_name = f"{self.wav_name[:-4]}.corrected.wav"
        self.type = "AR" if "BEHUMA" in self.system_code else "RSP2" if self.sample_rate == 6048 else "ICOM"
        self.wav: Optional[Wav] = None

    def __json__(self) -> Dict[str, Any]:

        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hours": self.hours,
            "minutes": self.minutes,
            "sample_rate": self.sample_rate,
            "pps_count": self.pps_count,
            "duration": self.duration,
            "precise_start": self.precise_start,
            "precise_end": self.precise_end,
            "system_code": self.system_code,
            "location_code": self.location_code,
            "location_url": self.location_url,
            "system_url": self.system_url,
            "wav_url": self.wav_url,
            "wav_name": self.wav_name,
            "png_url": self.png_url,
            "png_name": self.png_name,
            "beacon_frequency": self.signal.beacon_frequency if self.signal else None
        }

    def load(self) -> None:

        wav_content = Cache.get(self.wav_name, False)

        if not wav_content:

            while not wav_content or not len(wav_content):

                response = requests.get(self.wav_url)
                wav_content = response.content

            Cache.cache(self.wav_name, wav_content, False)

        self.wav = Wav(wav_content)
        self.pps = PPS(self.wav.pps.index, self.wav.pps.time)
        self.signal = Signal(self.wav.header.samplerate, self.wav.data.signal, self.beacon_frequency)
        self.signal.compute_fft()

    def save(self, path: str = ".") -> None:

        self.load() if not self.wav else None

        if self.wav:

            with open(os.path.join(path, self.wav_name), "wb") as file:

                file.write(self.wav.write())

    def process(self) -> None:

        corrected_wav_content = Cache.get(self.corrected_wav_name, False)

        if not corrected_wav_content:

            self.load() if not self.wav else None

            self.corrected_pps = self.pps.to_corrected_PPS(self.type)
            self.wav.pps.pps = [val for pair in zip(self.corrected_pps.index, self.corrected_pps.time) for val in pair]

            self.signal = Signal(
                self.wav.header.samplerate, self.wav.data.signal)
            self.signal.process()
            self.wav.data.set(self.signal)

            Cache.cache(self.json_string(), json.dumps(self, indent=4))
            Cache.cache(self.corrected_wav_name, self.wav.write(), False)

        else:

            self.wav = Wav(corrected_wav_content)
            self.pps = PPS(self.wav.pps.index, self.wav.pps.time)
            self.signal = Signal(self.wav.header.samplerate, self.wav.data.signal, self.beacon_frequency)
            self.signal.compute_fft()


    def json_string(self) -> str:

        return f"{self.system_code}.{str(self.year).zfill(4)}{str(self.month).zfill(2)}{str(self.day).zfill(2)}_{str(self.hours).zfill(2)}{str(self.minutes).zfill(2)}"


    def __eq__(self, other: File) -> File | Literal[False]:

        if isinstance(other, File):

            return (
                self.year == other.year and
                self.month == other.month and
                self.day == other.day and
                self.hours == other.hours and
                self.minutes == other.minutes and
                self.sample_rate == other.sample_rate and
                self.pps_count == other.pps_count and
                self.duration == other.duration and
                self.precise_start == other.precise_start and
                self.precise_end == other.precise_end and
                self.system_code == other.system_code and
                self.location_code == other.location_code and
                self.location_url == other.location_url and
                self.system_url == other.system_url and
                self.wav_url == other.wav_url and
                self.wav_name == other.wav_name and
                self.png_url == other.png_url and
                self.png_name == other.png_name and
                self.corrected_wav_name == other.corrected_wav_name and
                self.system == other.system and
                self.type == other.type and
                self.signal == other.signal
            )

        return False


def get(start: str, system: systems.System | str | list[systems.System] | list[str] | Dict[str, systems.System] | None = None) -> File | Dict[str, File]:

    year = start[:4]
    month = start[5:7]
    day = start[8:10]
    hours = start[11:13]
    minutes = start[14:16]

    if isinstance(system, (str, systems.System)):

        system_code = system if isinstance(system, str) else system.system_code
        cached_file = Cache.get(
            f"{system_code}.{year}{month}{day}_{hours}{minutes}")

        file = None

        if not cached_file:

            payload = {
                "start": start,
                "system_code": system_code
            }

            response = requests.post(endpoint, data=payload)
            json_file = response.json()
            file = File(*json_file.values())

        else:

            file = File(*json.loads(cached_file).values())

        file.system = systems.get(system_code=system_code)

        return file

    elif isinstance(system, (list, dict)):

        files: dict[str, File] = {}
        system_codes = []

        if isinstance(system, dict):

            system_codes = [s.system_code for s in system.values()]

        elif isinstance(system, list):

            if isinstance(system[0], str):

                system_codes = system

            elif isinstance(system[0], systems.System):

                system_codes = [s.system_code for s in system]

        for system_code in system_codes.copy():

            cached_file = Cache.get(
                f"{system_code}.{year}{month}{day}_{hours}{minutes}")

            if cached_file:

                files[system_code] = File(*json.loads(cached_file).values())
                files[system_code].system = systems.get(
                    system_code=system_code)
                system_codes.remove(system_code)

        if any(system_codes):

            payload = {
                "start": start,
                "system_code[]": system_codes
            }

            response = requests.post(endpoint, data=payload)
            json_files = response.json()

            if isinstance(json_files, dict):
                json_files = [json_files]

            json_files = {file["system_code"]: file for file in json_files}

            for system_code, json_file in json_files.items():

                files[system_code] = File(*json_file.values())
                files[system_code].system = systems.get(
                    system_code=system_code)

    elif isinstance(system, NoneType):

        files: dict[str, File] = {}

        system_codes = [
            system.system_code for system in systems.all().values()]

        for system_code in system_codes.copy():

            cached_file = Cache.get(
                f"{system_code}.{year}{month}{day}_{hours}{minutes}")

            if cached_file:

                files[system_code] = File(*json.loads(cached_file).values())
                files[system_code].system = systems.get(
                    system_code=system_code)
                system_codes.remove(system_code)

        if any(system_codes):

            payload = {
                "start": start,
                "system_code[]": system_codes
            }

            response = requests.post(endpoint, data=payload)
            json_files = response.json()

            json_files = {file["system_code"]: file for file in json_files}

            for system_code, json_file in json_files.items():

                files[system_code] = File(*json_file.values())
                files[system_code].system = systems.get(
                    system_code=system_code)

    return files
