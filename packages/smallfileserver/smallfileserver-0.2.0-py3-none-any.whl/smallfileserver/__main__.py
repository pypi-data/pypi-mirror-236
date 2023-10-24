
import sys
import argparse


from .fileserver import HTTPServer, RequestHandler
from .versions import version


if __name__ == '__main__':

    # 创建解析器
    parser = argparse.ArgumentParser(description='这是一个简单的文件服务器，支持文件下载与文件上传')

    # 添加命令行参数
    parser.add_argument('-p', '--port', type=int, required=False, default="8001", help='默认服务的端口')
    parser.add_argument('-ip', '--ip', type=str, required=False, default="0.0.0.0", help='默认的服务的IP')
    parser.add_argument('-v', '--verbose', action='store_true', help='当前软件的版本')

    # 解析命令行参数
    args = parser.parse_args()

    if args.verbose:
        print("Version is", version)
        exit(0)

    if int(sys.version_info[0]) == 2:
        print("python 2 m test success")
    elif int(sys.version_info[0]) == 3:
        # print("python 3 m test success")

        server = HTTPServer((args.ip, args.port), RequestHandler)
        print('Server running on %s port %s' % (args.ip, args.port))
        server.serve_forever()