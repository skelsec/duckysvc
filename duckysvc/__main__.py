import asyncio
import traceback
from duckysvc.duckysvc import DuckySvc

async def amain(args):
	try:
		dsvc = DuckySvc(args.server_ip, args.server_port, lang = args.lang, keyboard_device = args.device)
		await dsvc.run()
	except:
		traceback.print_exc('Error in ducksvc amain')

def main():
	import argparse

	parser = argparse.ArgumentParser(description='duckysvc')
	parser.add_argument('device', help = 'USB HID keyboard device. Usually /dev/hidg0. !Keyboard device must not be in raw mode!')
	parser.add_argument('--server-ip', default='127.0.0.1', help = 'server listen ip')
	parser.add_argument('--server-port', default = 1212, type=int, help = 'server listen port')
	parser.add_argument('-l', '--lang', default='us', help = 'Keyboard language layout')

	args = parser.parse_args()

	asyncio.run(amain(args))

if __name__ == '__main__':
	main()