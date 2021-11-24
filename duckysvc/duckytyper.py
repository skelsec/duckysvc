import sys
import time
import traceback

from duckysvc.external.duckencoder.duckencoder import DuckEncoder

class DuckyTyper:
	def __init__(self, device, infile = sys.stdin, language = 'us'):
		self.input_file = infile
		self.language = language
		self.keyboard_device = device
	
	def keyboard_typer(self, data):
		try:
			with open(self.keyboard_device,'wb') as f:
				for i in range(0, len(data), 2):
					out = b""
					key = ord(data[i:i+1])
					if len(data[i+1:i+2]) == 0:
						continue
					mod = ord(data[i+1:i+2])
					if (key == 0):
						# delay code
						d = float(mod)/1000.0
						time.sleep(d)
					out = bytes([mod]) + b'\x00' + bytes([key]) + b'\x00\x00\x00\x00\x00' + b'\x00\x00\x00\x00\x00\x00\x00\x00'
					f.write(out)
					f.flush()
		except Exception as e:
			traceback.print_exc('keyboard_writer')

	def run(self):
		try:
			close_file = False
			if isinstance(self.input_file, str):
				self.input_file = open(self.input_file, 'r')
				close_file = True

			for line in self.input_file:
				result = DuckEncoder.generatePayload(line, self.language)
				self.keyboard_typer(result)
		except Exception as e:
			traceback.print_exc('main error!')
		finally:
			if close_file is True:
				self.input_file.close()

def main():
	import argparse

	parser = argparse.ArgumentParser(description='duckysvc')
	parser.add_argument('device', help = 'USB HID keyboard device. Usually /dev/hidg0. !Keyboard device must not be in raw mode!')
	parser.add_argument('-i', '--infile', help = 'Input file to read Ducky script from. Default: STDIN')
	parser.add_argument('-l', '--language', default='us', help = 'Keyboard language layout. Default: us')

	args = parser.parse_args()

	infile = args.infile
	if infile is None or infile == '':
		infile = sys.stdin

	typer = DuckyTyper(args.device, infile, args.language)
	typer.run()

if __name__ == '__main__':
	main()