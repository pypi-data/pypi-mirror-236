from assert_files.assert_files import assert_objects
from assert_files import File

def test_assert_pdf():
    file1 = File(filepath='./tests/files/test_main.pdf')
    file2 = File(filepath='./tests/files/test_main_copy.pdf')
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
    assert_objects(file1, file2, fields=fields)

def test_different_fields():
    file1 = File(filepath='./tests/files/test_main.pdf')
    file2 = File(filepath='./tests/files/test_different.pdf')
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
    try:
        assert_objects(file1, file2, fields=fields)
    except Exception as e:
        error_message='''['Given Name', 'Address 2', 'Postcode', 'Country', 'City', 'Driving License', 'Favourite Colour', 'Language 3', 'Language 4', 'Gender']'''
        assert error_message in str(e)

def test_invalid_field():
    file1 = File(filepath='./tests/files/test_main.pdf')
    file2 = File(filepath='./tests/files/test_different.pdf')
    fields = ['Given']
    try:
        assert_objects(file1, file2, fields=fields)
    except Exception as e:
        assert '"Given": "field not found"' in str(e)

def test_missing_file():
    file1 = File(filepath='./tests/files/test_main.pdf')
    fields = ['Given']
    try:
        assert_objects(file1, None, fields=fields)
    except Exception as e:
        assert 'File file2 not provided' in str(e)
        
def test_missing_fields():
    file1 = File(filepath='./tests/files/test_main.pdf')
    file2 = File(filepath='./tests/files/test_different.pdf')
    fields = []
    try:
        assert_objects(file1, file2, fields=fields)
    except Exception as e:
        assert 'File fields not provided' in str(e)
        
def test_filepath_not_provided():
    try:
        File(None)
    except Exception as e:
        assert 'Filepath not provided' in str(e)
        
def test_file_get_fields():
    file = File(filepath='./tests/files/test_main.pdf')
    assert file.get_fields() == ['Given Name', 'Family Name', 'House nr', 'Address 2', 'Postcode', 'Country', 'Height', 'City', 'Driving License', 'Favourite Colour', 'Language 1', 'Language 2', 'Language 3', 'Language 4', 'Language 5', 'Gender', 'Address 1']
    
def test_file_get_filtered_fields():
    file = File(filepath='./tests/files/test_main.pdf')
    assert file.get_filtered_fields(['Country']) == '{\n    "Country": "TEST8"\n}'
    
def test_file_get_filtered_invalid_field():
    file = File(filepath='./tests/files/test_main.pdf')
    assert file.get_filtered_fields(['Country2']) == '{\n    "Country2": "field not found"\n}'