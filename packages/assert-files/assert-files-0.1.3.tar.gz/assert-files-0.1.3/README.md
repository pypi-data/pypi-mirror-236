# Assert-files

This lib is a support assert to validate files content (txt, csv, pdf, docx, xlsx and etc.).

## Features

* Implemented
    * PDF
        *  Form Comparing
* Not Implemente
    * PDF
        *All text comparing
    * TXT
    * CSV
    * DOCX
    * XLSX

___
## Installation
Follow lib instructions on https://pypi.org/project/assert-files/

```sh
pip install assert-files
```

## How to use

You are able to use assert_file.file.File object or just provide the path of local file

```python
from assert_files.assert_files import assert_objects
from assert_files.file import File

fields = ['field1', 'field2']
assert_objects(
    File(filepath='./tests/files/test_main.pdf'), 
    File(filepath='./tests/files/test_main_copy.pdf'), 
    fields=fields
)
```

```python
from assert_files.assert_files import assert_files_by_path

fields = ['field1', 'field2']
assert_files_by_path(
    './tests/files/test_main.pdf', 
    './tests/files/test_main_copy.pdf', 
    fields=fields
)
```
