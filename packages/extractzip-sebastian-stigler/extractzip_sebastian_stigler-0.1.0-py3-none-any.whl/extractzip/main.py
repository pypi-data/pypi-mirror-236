import argparse
import os
import re
import sys
from zipfile import ZipFile

from extractzip.helper import (
    load_config,
    extract_zip_file_name,
    is_encrypted,
    dst_content_exists,
    CONFIG_FILE,
    DST_PATH,
    extract_base_path,
    extract_course,
    extract_zip_name,
    extract_zip_file,
)
from extractzip import __version__
from extractzip.lang import lang
from extractzip.model import ZipType, Text
from extractzip.utils import red, green, blue, bold

OK = "  \U0001f929 "
NOT_OK = "  \U0001f47f "
NOT_EXIST_YET = "  \U0001f480 "
JUST_CNT = 50


def extract(
    course_name: str,
    zip_type: ZipType,
    *,
    text: Text = lang.en,
    config_path: str = CONFIG_FILE,
    dst_path: str = DST_PATH,
) -> str | None:
    try:
        zip_file = extract_zip_file_name(config_path, course_name, zip_type, text=text)
    except (AttributeError, FileExistsError, FileNotFoundError) as err:
        print(str(err), file=sys.stderr)
        return
    if dst_content_exists(zip_file, dst_path):
        print(blue(text.already_exists_text.format(zip_type=zip_type)))
        return
    if is_encrypted(zip_file):
        pwd = input(text.input_text).encode()
    else:
        pwd = None
    try:
        with ZipFile(zip_file, mode="r") as archive:
            archive.extractall(dst_path, pwd=pwd)
    except RuntimeError as err:
        if str(err).startswith("Bad password"):
            print(red(text.bad_password))
            return
        raise err
    print(green(text.success_text.format(zip_type=zip_type)))


def check(course_name: str) -> str:
    mask = 0xFFF
    check_ok = bold(blue("-" * JUST_CNT)) + "\n" + bold(green("Check complete!"))
    check_abborted = bold(blue("-" * JUST_CNT)) + "\n" + bold(red("Check incomplete!"))
    result = check_ok

    print(bold(blue(f"-----Course name".ljust(JUST_CNT, "-"))))
    pattern = re.compile(r"^[a-z0-9_]+$")
    res = pattern.match(course_name)
    if res is None:
        print(
            NOT_OK,
            red(
                f"The course name '{course_name}' is not well formed. Allowed: [a-z0-9_]+"
            ),
        )
        return check_abborted
    else:
        print(OK, f"The course name '{course_name}' is well formed.")

    print(bold(blue(f"-----Check config file".ljust(JUST_CNT, "-"))))
    try:
        config = load_config()
    except Exception as err:
        print(NOT_OK, red("Couldn't load config file:", str(err)))
        return check_abborted
    print(OK, "Config file loaded.")

    print(bold(blue("-----Check base path".ljust(JUST_CNT, "-"))))
    expected_base_path_mode = (
        0o42771  # Directory, GID, user and group full right, other only execute
    )
    try:
        base_path = extract_base_path(config, text=lang.en)
        base_path_mode = os.stat(base_path).st_mode
        if base_path_mode != expected_base_path_mode:
            raise ValueError(
                "Base path mode is %o but it should be %o"
                % (base_path_mode & mask, expected_base_path_mode & mask)
            )
    except Exception as err:
        print(NOT_OK, red(str(err)))
        return check_abborted
    print(OK, "Base path is ok.")

    print(
        bold(blue(f"-----Check course '{course_name}' directory".ljust(JUST_CNT, "-")))
    )
    expected_course_path_mode = 0o42751
    try:
        course = extract_course(config, course_name, text=lang.en)
        course_path_mode = os.stat(os.path.join(base_path, course_name)).st_mode
        if course_path_mode != expected_course_path_mode:
            raise ValueError(
                "Course path mode is %o but it should be %o"
                % (course_path_mode & mask, expected_course_path_mode & mask)
            )
    except Exception as err:
        print(NOT_OK, red(str(err)))
        return check_abborted
    print(OK, "Course path is ok.")

    for zip_type in ZipType:
        print(
            bold(
                blue(
                    f"-----Check {zip_type.name} in course '{course_name}'".ljust(
                        JUST_CNT, "-"
                    )
                )
            )
        )
        try:
            zip_name = extract_zip_name(course, zip_type, text=lang.en)
        except Exception as err:
            print(NOT_OK, red(str(err)))
            continue
        if zip_name is None:
            print(OK, f"{zip_type.name} is not defined in the config.")
            continue
        else:
            print(OK, f"{zip_type.name} is defined in the config.")
        expected_zip_file_mode = 0o100644
        try:
            zip_file = extract_zip_file(
                base_path, course_name, zip_name, zip_type, text=lang.en
            )
            zip_file_mode = os.stat(zip_file).st_mode
            if zip_file_mode != expected_zip_file_mode:
                raise ValueError(
                    f"{zip_name} mode is %o but it should be %o"
                    % (zip_file_mode & mask, expected_zip_file_mode & mask)
                )
        except FileNotFoundError as err:
            print(NOT_EXIST_YET, str(err))
            continue
        except Exception as err:
            print(NOT_OK, red(str(err)))
            result = check_abborted
            continue
        print(OK, f"The file {zip_name} is ok.")
        if is_encrypted(zip_file):
            print(OK, f"The file {zip_name} is encrypted.")
        else:
            print(OK, f"The file {zip_name} is not encrypted.")
    return result


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Check the config, the directories and zipfile for ExtractZip"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="CheckExtractZip {ver}".format(ver=__version__),
    )
    parser.add_argument("course_name", type=str, help="name of the directory")
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    print(check(args.course_name))


def run():
    main(sys.argv[1:])


class ExtractZip:
    """Extract files for course
    =======================

        ExtractZip().extract_<lang>_<zip_type>_<course>()

    Where

    * <lang> is either ``de`` for german or ``en`` for english,
    * <exam_type> is either ``slides``, ``examples``, ``exercises``, ``solutions``, ``testexam`` or ``exam`` and
    * <course> is the name of the course from the `config.yaml`.



    Example:
    --------

    You want the german form for a testexam for the course 23w_python101,
    then you call:

        ExtractZip().extract_de_testexam_23w_python101()
    ----------------------------------------------------------------------
    """

    def __getattr__(self, name):
        pattern = re.compile(
            r"^extract_(?P<lang>de|en)_(?P<zip_type>slides|examples|exercises|solutions|testexam|exam)_(?P<course>[a-z0-9_]+)$"
        )
        parsed = pattern.match(name)
        if parsed is None:
            raise AttributeError(
                f"type object '{self.__class__.name}' has no attribute '{name}'"
            )
        lng, zip_type, course = parsed.groups()
        return lambda: extract(course, ZipType(zip_type), text=getattr(lang, lng))
