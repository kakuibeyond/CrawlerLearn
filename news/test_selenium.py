# from selenium import webdriver

# browser = webdriver.Chrome()
# browser.get('http://www.baidu.com/')

# from bs4 import BeautifulSoup
# soup = BeautifulSoup('hello','lxml')
# print(soup.p.string)

# import tesserocr
# from PIL import Image
# image = Image.open('image.png')
# print(tesserocr.image_to_txt(image))

# from  PIL import  Image
# import pytesseract
# # 不依赖opencv写法
# text=pytesseract.image_to_string(Image.open('image.png'))
# print(text)

# 测试flask安装成功
# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# def hello():
#     return 'hello world ,im the first flask exe'
# if __name__ =='__main__':
#     app.run()

# 验证tornado成功安装
# import tornado.ioloop
# import tornado.web
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write('hello world im tornado.')
# def make_app():
#     return tornado.web.Application([(r'/',MainHandler),])
# if __name__ == '__main__':
#     app=make_app
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user mynames cw!')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
