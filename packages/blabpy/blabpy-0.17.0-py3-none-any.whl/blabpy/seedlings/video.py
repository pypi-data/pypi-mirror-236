"""
Functions that work with video files.
"""
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import pytz


def _parse_exiftool_output(exiftool_output):
    """
    Parses the output of the `exiftool` command-line application.
    :param exiftool_output: string output of the `exiftool` command-line application
    :return: a dictionary of property-value pairs
    """
    all_properties_lines = exiftool_output.rstrip().split('\n')
    # Each property looks like
    # 'Image Size                      : 1280x720'
    all_properties_dict = {key.strip(): value.strip()  # remove extra spaces
                           for key, value
                           in map(lambda line: line.split(' : '),
                                  all_properties_lines)}

    return all_properties_dict


def get_metadata(video_file_path):
    """
    Gets metadata of a video file using the `exiftool` command-line application.
    :param video_file_path: path to the video file
    :return: metadata as a dictionary of property-value pairs
    """
    cmd = ('exiftool', Path(video_file_path).absolute())
    exiftool_output = subprocess.run(cmd, capture_output=True, text=True).stdout
    metadata = _parse_exiftool_output(exiftool_output=exiftool_output)
    return metadata


def get_property_from_metadata(video_file_path, property_name):
    metadata = get_metadata(video_file_path)
    return metadata.get(property_name)


def get_start_dt_from_metadata(metadata):
    """
    Gets the start date and time of the video recording adjusted toward the correct time using a heuristic that worked
    for aligning the results with the day-by-day times.
    :param metadata: make of the camera from the same metadata
    :return: start timestamp as a datetime object
    """
    start_dt_string = metadata.get('Date/Time Original')
    if start_dt_string is None:
        return None
    make = metadata.get('Make')

    start_dt_string = start_dt_string.replace(' DST', '')  # Remove the DST suffix, it isn't informative
    # Panasonic camera(s) put "+" instead of minus in the timezone part.
    if make == 'Panasonic':
        start_dt_string = start_dt_string.replace('+', '-')
    # Parse, convert to UTC and then to US/Eastern to account for DST
    start_dt = (datetime.strptime(start_dt_string, '%Y:%m:%d %H:%M:%S%z')
                        .astimezone(tz=pytz.utc)
                        .astimezone(tz=pytz.timezone('US/Eastern')))
    # Panasonic camera(s) were one hour ahead of the Sony camera(s)
    if make == 'Panasonic':
        start_dt -= timedelta(hours=1)

    return start_dt


def get_start_dt_from_video_file(video_file_path):
    """
    Gets the start date and time of the video recording adjusted toward the correct time using a heuristic.
    :param video_file_path: path to the video file
    :return: start timestamp as a datetime object
    """
    metadata = get_metadata(video_file_path)
    return get_start_dt_from_metadata(metadata)
