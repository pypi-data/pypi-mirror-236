
import sys

from .fileserver import HTTPServer, RequestHandler


if __name__ == '__main__':
    if int(sys.version_info[0]) == 2:
        print("python 2 m test success")
    elif int(sys.version_info[0]) == 3:
        # print("python 3 m test success")

        PORT = 8001
        server = HTTPServer(('localhost', PORT), RequestHandler)
        print('Server running on port %s' % PORT)
        server.serve_forever()