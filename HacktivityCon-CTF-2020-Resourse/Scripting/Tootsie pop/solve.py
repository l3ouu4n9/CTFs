import magic
import os
import subprocess

filename = '94228b'
os.system('cp 94228b.bak 94228b')
while True:
	t = magic.from_file(filename)
	print(filename, t)

	if 'gz' in t:
		if '.gz' not in filename:
			os.system('mv {} {}.gz'.format(filename, filename))
			os.system('gzip -d {}.gz'.format(filename))
		else:
			os.system('gzip -d {}'.format(filename))
	elif 'XZ' in t:
		if '.xz' not in filename:
			os.system('mv {} {}.xz'.format(filename, filename))
			os.system('xz -d {}.xz'.format(filename))
		else:
			os.system('xz -d {}'.format(filename))
	elif 'bzip2' in t:
		if '.bzip2' not in filename:
			os.system('mv {} {}.bz2'.format(filename, filename))
			os.system('bzip2 -d {}.bz2'.format(filename))
		else:
			os.system('bzip2 -d {}'.format(filename))
	elif 'Zip archive' in t:
		if '.zip' not in filename:
			os.system('mv {} {}.zip'.format(filename, filename))
			out = subprocess.check_output(['unzip', '{}.zip'.format(filename)])
			os.system('rm {}.zip'.format(filename))
		else:
			out = subprocess.check_output(['unzip', filename])
			os.system('rm {}'.format(filename))
		filename = out.split(' ')[4]
		new_filename = filename.split('.')[0]
		os.system('mv {} {}'.format(filename, new_filename))
		filename = new_filename
	else:
		break