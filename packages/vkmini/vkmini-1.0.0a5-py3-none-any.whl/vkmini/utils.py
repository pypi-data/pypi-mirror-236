from multiprocessing import Process
from multiprocessing.connection import Pipe

from humanfriendly import format_size


def writer(connection):
    buf = b'?' * (4294967295 - 32 - 16)
    print(len(buf))
    connection.send_bytes(buf)


def reader():
    print(format_size(len(out_.recv_bytes())))


if __name__ == '__main__':
    in_, out_ = Pipe()

    Process(target=writer, args=(in_,)).start()
    reader()
