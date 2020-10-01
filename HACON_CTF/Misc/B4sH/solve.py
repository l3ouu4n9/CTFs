import subprocess

file = '93531.zip'


while '.zip' in file:
	p = subprocess.check_output(['unzip', '-P', file.split('.')[0], file])
	command = 'rm ' + file
	subprocess.Popen(['rm', file])
	file = p.split('extracting: ')[1].strip()