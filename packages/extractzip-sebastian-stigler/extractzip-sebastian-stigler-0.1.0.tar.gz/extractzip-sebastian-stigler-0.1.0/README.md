[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/extractzip-sebastian-stigler.svg)](https://pypi.org/project/extractzip-sebastian-stigler/)

# ExtractZip

> Extract Slides, Exercises, Solutions, TestExams or Exams!

## Installation

1.  Create the user `extractzip` and set the access rights for the home directory.

```{.}
# as user root:
adduser --disabled-password extractzip
chmod 2771 ~extractzip
```

2.  Add `extractzip` group to **admin users** that want to use this tool.

```{.}
# as user root:
adduser jupyter-sebastian extractzip
```

3.  Create the config directory and file and set access rights and ownership.

```{.}
# as user root
mkdir /etc/extractzip
chmod 755 /etc/extractzip
touch /etc/extractzip/config.yaml
chmod 664 /etc/extractzip/config.yaml
chown  extractzip:extractzip /etc/extractzip/config.yaml
```

4.  Edit the config file, where you specify the `base_path` (home directory of `extractzip`) and the `courses`.
    Each course has a `name` (the directory in `base_path`) that follows the pattern `^[a-z0-9_]+$` and optional 
    entries for `slides`, `exercises`, `solutions`, `testexam` and `exam` which points to the basename of the corresponding
    zip file.
    
```{.}
# as admin user with extractzip group (e.g. jupyter-sebastian)

# You can see here an course with the name 'testcourse'.
# The exam is commented out -> it can't be downloaded yet.

# /etc/extractzip/config.yaml

---
base_path: /home/extractzip
courses: 
  - name: testcourse
    slides: Slides.zip
    examples: Examples.zip
    exercises: Exercises.zip
    solutions: Solutions.zip
    # exam: Exam.zip
    testexam: Testexam.zip
```

5.  Create the corresponding directory for the configured course, copy the zip files in it and set the correct
    access rights.

```{.}
# as admin user with extractzip group (e.g. jupyter-sebastian)

cd ~extractzip
mkdir testcourse
chmod 2771 testcourse

# copy zipfiles to new directory from <src_dir>
cp <src_dir>/{Exercises,Solutions,Exam,Testexam}.zip testcourse/.
chmod 644 testcourse/*.zip
```

## Check config, course directory and zip files

Run the following command with the course directory to check:

```{.}
CheckExtractZip testcourse
```
The result of the checks will be prefix with an emoji to indicate **success** (🤩), **failure** (👿) or 
**the zipfile is not yet in the course directory** (💀). The last one is not an error (see the third example below). 


If everything is ok, the output should look like this (make sure that the last line reads **Check complete!**):

```{.}
-----Course name----------------------------------
  🤩  The course name 'testcourse' is well formed.
-----Check config file----------------------------
  🤩  Config file loaded.
-----Check base path------------------------------
  🤩  Base path is ok.
-----Check course 'testcourse' directory----------
  🤩  Course path is ok.
-----Check Exercises in course 'testcourse'-------
  🤩  Exercises is defined in the config.
  🤩  The file Exercises.zip is ok.
  🤩  The file Exercises.zip is not encrypted.
-----Check Solutions in course 'testcourse'-------
  🤩  Solutions is defined in the config.
  🤩  The file Solutions.zip is ok.
  🤩  The file Solutions.zip is not encrypted.
-----Check Exam in course 'testcourse'------------
  🤩  Exam is defined in the config.
  🤩  The file Exam.zip is ok.
  🤩  The file Exam.zip is encrypted.
-----Check TestExam in course 'testcourse'--------
  🤩  TestExam is defined in the config.
  🤩  The file Testexam.zip is ok.
  🤩  The file Testexam.zip is encrypted.
--------------------------------------------------
Check complete!
```

If the result is not ok, the output looks something like this (make sure the last line reads **Check incomplete!**):

```{.}
-----Course name----------------------------------
  🤩  The course name 'testcourse' is well formed.
-----Check config file----------------------------
  🤩  Config file loaded.
-----Check base path------------------------------
  🤩  Base path is ok.
-----Check course 'testcourse' directory----------
  🤩  Course path is ok.
-----Check Exercises in course 'testcourse'-------
  🤩  Exercises is defined in the config.
  👿  Exercises.zip mode is 444 but it should be 644
-----Check Solutions in course 'testcourse'-------
  🤩  Solutions is defined in the config.
  🤩  The file Solutions.zip is ok.
  🤩  The file Solutions.zip is not encrypted.
-----Check Exam in course 'testcourse'------------
  🤩  Exam is defined in the config.
  🤩  The file Exam.zip is ok.
  🤩  The file Exam.zip is encrypted.
-----Check TestExam in course 'testcourse'--------
  🤩  TestExam is defined in the config.
  🤩  The file Testexam.zip is ok.
  🤩  The file Testexam.zip is encrypted.
--------------------------------------------------
Check incomplete!
```

If you see lines like the following than it means, you have not put the configured zipfile for TestExam in the
course directory.

This is **not** an error because you could have intentionally withheld the file until it is convenient during the course:

```{.}
-----Check TestExam in course 'testcourse'--------
  🤩  TestExam is defined in the config.
  💀  The TestExam doesn't exist (yet).
--------------------------------------------------
```

## Using the ExtractZip package

The `ExtractZip` class has the following general method for extracting a specific zip file:

```{.}
ExtractZip().extract_<lang>_<zip_type>_<course>()
```
Where

* `<lang>` is either ``de`` for german or ``en`` for english,
* `<exam_type>` is either ``slides``, ``examples``, ``exercises``, ``solutions``, ``testexam`` or ``exam`` and
* `<course>` is the name of the course from the `config.yaml`.

In a Jupyter Notebook you can put the following in a cell to extract the **slides** of the **testcourse** with
**en**glish output:  

```python
from extractzip import ExtractZip
ExtractZip().extract_en_slides_testcourse()
```

When the cell is executed, the corresponding zipfile will be extracted in the home directory of the current user.

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see <https://pyscaffold.org/>.
