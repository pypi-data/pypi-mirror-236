import json
import PyPDF2


class File():
	def __init__(self, filepath):
		if not filepath:
			raise ValueError('Filepath not provided')
		self.filepath = filepath
		file = open(filepath, "rb")
		self.fields = self.__load_pdf_fields(file)
		file.close()
	
	def get_fields(self):
		return list(self.fields.keys())

	def get_filtered_fields(self, filter):
		fields = {}
		for field in filter:
			try:
				fields.update({field: self.fields[field]})
			except KeyError:
				fields.update({field: 'field not found'})
		return json.dumps(fields, indent=4)

	def __load_pdf_fields(self, file):
		fields = {}
		self.pdf = PyPDF2.PdfReader(file)
		for item in self.pdf.get_fields().items():
			key, value = item[1]['/T'].split(' '), item[1]['/V']
			key = ' '.join(key[:len(key)-2])
			value = value if not value.startswith('/') else value[1:]
			fields.update({key: value})
		return fields

	def __repr__(self):
		obj = {
			'filepath': self.filepath,
			'fields': self.fields
		}
		return f'File({json.dumps(obj, indent=4)})'

if __name__ == "__main__":
    file = File(filepath='./files/test.pdf')
    print(file)
    print('\n')
    print(file.fields['Given Name'])
    print(file.get_fields())