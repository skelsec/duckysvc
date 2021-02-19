import asyncio
import websockets
from duckysvc.duckysvc import DuckySvc

async def amain():
	dsvc = DuckySvc('localhost', 11112, lang = 'us', keyboard_device = 'test.txt')
	asyncio.create_task(dsvc.run())
	await asyncio.sleep(1)
	uri = "ws://localhost:11112"
	async with websockets.connect(uri) as websocket:
		data = 'STRING hello world!\r\nENTER'
		await websocket.send(data)

if __name__ == '__main__':
	asyncio.run(amain())