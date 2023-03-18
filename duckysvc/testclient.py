import asyncio
import websockets
import json
from duckysvc.duckysvc import DuckySvc

async def amain():
	dsvc = DuckySvc('localhost', 11112, lang = 'us', keyboard_device = 'test')
	asyncio.create_task(dsvc.run())
	await asyncio.sleep(1)
	uri = "ws://localhost:11112"
	async with websockets.connect(uri) as websocket:
		data = json.dumps({
			'language': 'us',
			'text': 'STRING hello world!\r\nENTER'
		})
		await websocket.send(data)
		resp = await websocket.recv()
		print(json.loads(resp))

		data = json.dumps({
			'language': 'us',
		})
		await websocket.send(data)
		resp = await websocket.recv()
		print(json.loads(resp))

		data = json.dumps({
			'language': 'us',
			'text': None,
		})
		await websocket.send(data)
		resp = await websocket.recv()
		print(json.loads(resp))

		data = json.dumps({
			'language': 'us',
			'text': 'STRING hello world!\r\nENTER'
		})
		await websocket.send(data)
		resp = await websocket.recv()
		print(json.loads(resp))

		data = json.dumps({
			'language': 'us',
			'text': 'STRING hello world!'
		})
		await websocket.send(data)
		resp = await websocket.recv()
		print(json.loads(resp))

if __name__ == '__main__':
	asyncio.run(amain())