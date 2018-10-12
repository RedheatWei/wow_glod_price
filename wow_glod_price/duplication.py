#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@auther = 'Redheat'
@create = '2018/10/10 18:14'
@email = 'qjyyn@qq.com'
'''
class RepeatFilter(object):
    def __init__(self):
        self.visited_url = set()

    @classmethod
    def from_settings(cls, settings):
        """
        初始化时，调用
        :param settings:
        :return:
        """
        return cls()

    def request_seen(self, request):
        """
        检测当前请求是否已经被访问过
        :param request:
        :return: True表示已经访问过；False表示未访问过
        """
        if request.url in self.visited_url:
            return True
        self.visited_url.add(request.url)
        return False

    def open(self):
        """
        开始爬去请求时，调用
        :return:
        """
        pass

    def close(self, reason):
        """
        结束爬虫爬取时，调用
        :param reason:
        :return:
        """
        pass

    def log(self, request, spider):
        """
        记录日志
        :param request:
        :param spider:
        :return:
        """
        # print('repeat', request.url)
        pass