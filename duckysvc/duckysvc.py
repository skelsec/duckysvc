import json
import asyncio
import traceback
from duckysvc import logger
from duckysvc.external.duckencoder.duckencoder import DuckEncoder

import websockets


class DuckySvc:
	def __init__(self, listen_ip, listen_port, ssl_ctx = None, lang = 'us', keyboard_device = '/dev/hidg0'):
		self.lang = lang
		self.listen_ip = listen_ip
		self.listen_port = listen_port
		self.ssl_ctx = ssl_ctx
		self.keyboard_device = keyboard_device
		self.server = None
		self.device_lock = asyncio.Lock()
		self.__request_id = 0

	def __next_request_id(self):
		self.__request_id += 1
		return self.__request_id
	
	async def handle_client(self, ws, path):
		try:
			#print('Client connected!')
			while True:
				data = await ws.recv()
				reqid = self.__next_request_id()
				source = json.loads(data)
				logger.info('[%s] Incoming dict: %s' % (reqid, repr(source)))
				language = source.get('language', self.lang)
				if language is None:
					language = self.lang
				text = source.get('text', None)
				if text is None:
					await ws.send(json.dumps({
						'result': 'ERROR',
						'error': 'text missing from request'}))
					continue
				if language is None:
					await ws.send(json.dumps({
						'result': 'ERROR',
						'error': 'language missing from request'}))
					continue
				if self.keyboard_device is None:
					await ws.send(json.dumps({
						'result': 'ERROR',
						'error': 'No HID device is configured!'}))
					continue
				
				
				logger.info('[%s] Incoming ducky text: %s' % (reqid, repr(text)))

				async with self.device_lock:
					try:
						payload = DuckEncoder.generatePayload(text, language)
					except Exception as e:
						await ws.send(json.dumps({
							'result': 'ERROR',
							'error': 'Ducky encoder failed! Reason: %s' % str(e)}))
						continue
					logger.info('[%s] Payload bytes: %s' % (reqid, repr(payload)))
					with open(self.keyboard_device,'wb') as f:
						for i in range(0, len(payload), 2):
							out = b""
							key = ord(payload[i:i+1])
							if len(payload[i+1:i+2]) == 0:
								continue
							mod = ord(payload[i+1:i+2])
							if (key == 0):
								# delay code
								d = float(mod)/1000.0
								await asyncio.sleep(d)
							out = bytes([mod]) + b'\x00' + bytes([key]) + b'\x00\x00\x00\x00\x00' + b'\x00\x00\x00\x00\x00\x00\x00\x00'
							logger.debug('[%s] Bytes sent to %s: %s' % (reqid, self.keyboard_device, repr(out)))
							f.write(out)
							f.flush()
				
				await ws.send(json.dumps({'result': 'OK'}))

		except websockets.exceptions.ConnectionClosed:
			logger.info('Client disconnected!')
		except Exception as e:
			traceback.print_exc()
			await ws.send(
				json.dumps({
					'result': 'ERROR',
					'error': 'Generic error! Reason: %s' % str(e)
				})
			)
			

	async def run(self):
		try:
			self.server = await websockets.serve(self.handle_client, self.listen_ip, self.listen_port, ssl=self.ssl_ctx)
			await self.server.wait_closed()
		except Exception as e:
			traceback.print_exc()