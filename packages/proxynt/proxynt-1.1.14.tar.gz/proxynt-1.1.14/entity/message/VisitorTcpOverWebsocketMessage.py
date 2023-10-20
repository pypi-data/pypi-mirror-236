from typing_extensions import TypedDict


class VisitTcpOverWebsocketMessage(TypedDict):
    uid: bytes  # 连接id
    from_name: str
    to_name: str
    to_client_name: str
    ip_port: str # ip和端口 127.0.0.1:8000
    data: bytes
