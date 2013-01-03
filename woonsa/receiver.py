import gevent
from gevent import monkey; monkey.patch_all()
from gevent.server import StreamServer

from .logger import get_logger
from .mtr import Mtr

class ReceiveServer(StreamServer):
    def __init__(self, listener, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.logger = get_logger(__name__)

    def handle(self, socket, addr):
        self.logger.info("New connection from %s:%s" % addr)
        gevent.spawn(self.recv_all, socket, addr)

    def recv_all(self, socket, addr):
        mtr = Mtr()
        sockf = socket.makefile()
        while True:
            line = sockf.readline()
            if not line:
                self.logger.info("client disconnected")
                break
            line = line.strip()
            mtr.feed(line)
            self.logger.debug(line)

        for l in mtr.rows:
            self.logger.debug('%r' % l)


    def close(self):
        if not self.closed:
            self.logger.info("Close Server")
            StreamServer.close(self)

