import os
from zipfile import is_zipfile, ZipFile

import yaml

from extractzip.model import Config, Text, Course, ZipType

CONFIG_FILE = "/etc/extractzip/config.yaml"
DST_PATH = os.environ.get("HOME", os.path.expanduser("~"))


def load_config(config_file: str = CONFIG_FILE) -> Config:
    with open(config_file) as cfg:
        content = yaml.safe_load(cfg)
    result = Config.from_dict(content)
    return result


def extract_base_path(config: Config, *, text: Text) -> str:
    base_path = config.base_path
    if base_path == "" or base_path is None or not os.path.isdir(base_path):
        raise AttributeError(text.base_path_error)
    return base_path


def extract_course(config: Config, course_name: str, *, text: Text) -> Course:
    course = config.find(course_name)
    if course is None:
        raise AttributeError(text.config_error.format(course_name=course_name))
    return course


def extract_zip_name(course: Course, zip_type: ZipType, *, text: Text) -> str:
    zip_name = course.get(zip_type)
    if zip_name is None:
        raise AttributeError(
            text.course_error.format(zip_type=zip_type, course_name=course.name)
        )
    return zip_name


def extract_zip_file(
    base_path: str, course_name, zip_name, zip_type: ZipType, *, text: Text
) -> str:
    zip_file = os.path.join(base_path, course_name, zip_name)
    if not os.path.isfile(zip_file):
        raise FileNotFoundError(text.file_error.format(zip_type=zip_type))
    if not is_zipfile(zip_file):
        raise FileExistsError(text.zip_file_error.format(zip_type=zip_type))
    return zip_file


def extract_zip_file_name(
    config_path: str, course_name: str, zip_type: ZipType, *, text: Text
) -> str:
    config = load_config(config_path)
    base_path = extract_base_path(config, text=text)
    course = extract_course(config, course_name, text=text)
    zip_name = extract_zip_name(course, zip_type, text=text)
    zip_file = extract_zip_file(base_path, course_name, zip_name, zip_type, text=text)

    return zip_file


def is_encrypted(zip_file: str) -> bool:
    with ZipFile(zip_file, "r") as archive:
        for zi in archive.infolist():
            if zi.flag_bits & 1:
                return True
    return False


def dst_content_exists(zip_file: str, dst_dir: str) -> bool:
    with ZipFile(zip_file, "r") as archive:
        for zi in archive.infolist():
            if os.path.exists(os.path.join(dst_dir, zi.filename)):
                return True
            return False
