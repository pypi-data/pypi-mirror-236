from assert_files.file import File

def __validate_mantadory_field(attb, value):
    if not value:
        raise ValueError(f'File {attb} not provided')

def assert_objects(file1, file2, fields):
    __validate_mantadory_field('file1', file1)
    __validate_mantadory_field('file2', file2)
    __validate_mantadory_field('fields', fields)
    error_list = []
    for field in fields:
        try:
            assert file1.fields[field], file2.fields[field]
        except KeyError:
            error_list.append(field)
        except AssertionError:
            error_list.append(field)
    if error_list:
        raise AssertionError(
            f'Fields {error_list} are not equal between files\n' +
            f'{file1.filepath}: {file1.get_filtered_fields(error_list)}\n' +
            f'{file2.filepath}: {file2.get_filtered_fields(error_list)}'
        )

def assert_files_by_path(filepath1, filepath2, fields):
    file1 = File(filepath=filepath1)
    file2 = File(filepath=filepath2)
    assert_objects(file1, file2, fields)

if __name__ == "__main__":
    fields = [
        'Given Name', 
        'Family Name', 
        'House nr', 
        'Address 2', 
        'Postcode', 
        'Country', 
        'Height', 
        'City', 
        'Driving License', 
        'Favourite Colour', 
        'Language 1', 
        'Language 2', 
        'Language 3', 
        'Language 4', 
        'Language 5', 
        'Gender', 
        'Address 1'
    ]
    assert_files_by_path('./tests/files/test_main.pdf', './tests/files/test_main_copy.pdf', fields=fields)
