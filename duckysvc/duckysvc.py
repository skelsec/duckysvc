import asyncio
import traceback
from duckysvc.external.duckencoder.duckencoder import DuckEncoder

import websockets


class DuckySvc:
	def __init__(self, listen_ip, listen_port, ssl_ctx = None, lang = 'us', keyboard_device = '/dev/hidg1'):
		self.lang = lang
		self.listen_ip = listen_ip
		self.listen_port = listen_port
		self.ssl_ctx = ssl_ctx
		self.keyboard_device = keyboard_device
		self.server = None
		self.keyboard_task = None
		self.in_q = None
		

	async def keyboard_writer(self):
		try:
			with open(self.keyboard_device,'wb') as f:
				while True:
					data = await self.in_q.get()
					for i in range(0, len(data), 2):
						out = b""
						key = ord(data[i:i+1])
						if len(data[i+1:i+2]) == 0:
							continue
						mod = ord(data[i+1:i+2])
						if (key == 0):
							# delay code
							d = float(mod)/1000.0
							await asyncio.sleep(d)
						out = bytes([mod]) + b'\x00' + bytes([key]) + b'\x00\x00\x00\x00\x00' + b'\x00\x00\x00\x00\x00\x00\x00\x00'
						f.write(out)
						f.flush()
		except Exception as e:
			traceback.print_exc('keyboard_writer')
	
	async def handle_client(self, ws, path):
		try:
			print('Client connected!')
			while True:
				data = await ws.recv()
				print('DATA')
				print(data)
				source = data
				#for line in data:
				#	if line == '':
				#		continue
				#	source += data
				print('source')
				print(repr(source))
				result = DuckEncoder.generatePayload(source, self.lang)
				print('result')
				print(repr(result))
				await self.in_q.put(result)


		except Exception as e:
			traceback.print_exc('handle_client')

	async def run(self):
		try:
			self.in_q = asyncio.Queue()
			self.keyboard_task = asyncio.create_task(self.keyboard_writer())
			self.server = await websockets.serve(self.handle_client, self.listen_ip, self.listen_port, ssl=self.ssl_ctx)
			await self.server.wait_closed()
		except Exception as e:
			traceback.print_exc('run')