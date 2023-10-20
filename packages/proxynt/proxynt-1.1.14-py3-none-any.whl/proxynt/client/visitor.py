import logging
import os
import socket
import time
import traceback
from threading import Thread
from typing import List, Dict

from client.tcp_forward_client import TcpForwardClient, PrivateSocketConnection
from common import websocket
from common.logger_factory import LoggerFactory
from common.nat_serialization import NatSerialization
from common.pool import SelectPool
from common.register_append_data import ResisterAppendData
from common.speed_limit import SpeedLimiter
from constant.message_type_constnat import MessageTypeConstant
from context.context_utils import ContextUtils
from entity.message.message_entity import MessageEntity
from entity.message.push_config_entity import Visitor


class VisitListenServer:
    def __init__(self, s: socket.socket, name: str, client_name: str):
        self.socket: socket.socket = s
        self.name: str = name
        self.client_name: str = client_name


class VisitConnection:
    """连接本地监听端口的客户端， 这个客户端是其他程序连的"""

    def __init__(self, uid: bytes, visit_listen_server: VisitListenServer):
        self.uid: bytes = uid
        self.visit_listen_server: VisitListenServer = visit_listen_server


class Visitor(TcpForwardClient):
    def __init__(self, ws):
        super(Visitor, self).__init__(ws)
        self.uid_to_visit_connection: Dict[bytes, VisitConnection] = dict()
        self.listen_socket_to_listen_server: Dict[socket.socket, VisitListenServer] = {}
        self.is_running = True
        self.socket_event_loop = SelectPool()

    def create_visit_listen(self, config: List[Visitor]):
        for c in config:
            client_name = c['client_name']
            name = c['name']
            listen_port = c['listen_port']
            s = self._create_listen_socket(listen_port)
            listen_server = VisitListenServer(s, name, client_name)
            self.listen_socket_to_listen_server[s] = listen_server
            self.socket_event_loop.register(s, ResisterAppendData(self.start_accept, None))

    def handle_message(self, each: socket.socket, data: ResisterAppendData):
        connection = self.socket_to_socket_connection[each]
        if data.speed_limiter and data.speed_limiter.is_exceed()[0]:
            if LoggerFactory.get_logger().isEnabledFor(logging.DEBUG):
                LoggerFactory.get_logger().debug('over speed')
            self.socket_event_loop.unregister_and_register_delay(each, data, 1)
        try:
            recv = each.recv(data.read_size)
            if data.speed_limiter:
                data.speed_limiter.add(len(recv))
        except OSError as e:
            LoggerFactory.get_logger().warn('get os error: {str(e)}, close')
            recv = b''
        send_message: MessageEntity = {
            'type_': MessageTypeConstant.VISIT_TCP_OVER_WEBSOCKET,
            'data': {
                'uid': connection.uid,
                'from_name': '',
                'to_name': to_name.decode(),
                'to_client_name': to_client_name.decode(),
                'ip_port': ip_port.decode(),
                'data': socket_dta
            }
        }
        start_time = time.time()
        self.ws.send(NatSerialization.dumps(send_message, ContextUtils.get_password()), websocket.ABNF.OPCODE_BINARY)
        if LoggerFactory.get_logger().isEnabledFor(logging.DEBUG):
            LoggerFactory.get_logger().debug(f'send to ws cost time {time.time() - start_time}')
        if not recv:
            try:
                self.close_connection(each)
            except Exception:
                LoggerFactory.get_logger().error(f'close error: {traceback.format_exc()}')


    def close_remote_socket(self, connection: PrivateSocketConnection):
        name = connection.name
        send_message: MessageEntity = {
            'type_': MessageTypeConstant.VISIT_TCP_OVER_WEBSOCKET,
            'data': {
                'name': name,
                'data': b'',
                'uid': connection.uid,
                'ip_port': ''
            }
        }
        self.ws.send(NatSerialization.dumps(send_message, ContextUtils.get_password()), websocket.ABNF.OPCODE_BINARY)

    def start_accept(self, server_socket: socket, register_append_data: ResisterAppendData):
        try:
            client, address = server_socket.accept()
            client: socket.socket
        except OSError:
            return
        LoggerFactory.get_logger().info(f'get connect : {address}')
        server = self.listen_socket_to_listen_server[server_socket]
        # 当前 服务端的client 也会对应服务端连接内网服务的一个 client
        uid = os.urandom(4)
        visit_connection = VisitConnection(uid, server)
        self.uid_to_visit_connection[uid] = visit_connection
        Thread(target=self.request_to_connect, args=(visit_connection,)).start()
        append_data = ResisterAppendData(self.handle_message, register_append_data.speed_limiter)
        self.socket_event_loop.register(client, append_data)

    def request_to_connect(self, client_socket_connection: VisitConnection):
        """请求连接客户端"""
        send_message: MessageEntity = {
            'type_': MessageTypeConstant.VISIT_REQUEST_TO_CONNECT.encode(),
            'data': {
                'uid': client_socket_connection.uid,
                'from_name': '',
                'to_name': client_socket_connection.visit_listen_server.name,
                'to_client_name': client_socket_connection.visit_listen_server.client_name,
                'ip_port': '',
                'data': b''
            }
        }
        self.ws.send(NatSerialization.dumps(send_message, ContextUtils.get_password()), websocket.ABNF.OPCODE_BINARY)

    def _create_listen_socket(self, port):
        s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)
        return s
