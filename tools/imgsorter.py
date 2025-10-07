import os
import sys

types = {
	's': 'soft',
	'e': 'ecchi',
	'h': 'hard',
	'm': 'mild'
}

acceptable_files = ['gif','jpg','jpeg','png']
tracker = {}
for filename in os.listdir('./'):
	if os.path.isfile(filename):
		if filename[0] == '.':
			continue
		fileparts = filename.split('.')
		lastpart = fileparts[len(fileparts)-1].lower()
		if lastpart in acceptable_files:
			msg = f'open "{filename}"'
			os.system(msg)
			while True:
				inputval = input(f'What flavor was {filename}? ')
				if inputval[0].lower() in types.keys:
					mvpath = f'{types[inputval[0].lower()]}/{filename}'
					msg = f'mv "{filename}" "{mvpath}"'
					print(msg)