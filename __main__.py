from src.WebSocket import WebSocket
import builtins

builtins.gameserver = WebSocket('127.0.0.1', 9000)
gameserver.startServer()