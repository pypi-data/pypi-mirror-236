# -*- coding: utf-8 -*-
# @Time    : 2022/5/21 22:20
# @Author  : qxcnwu
# @FileName: DownloadMain.py
# @Software: PyCharm

import os
import socket
import threading
from typing import List

import numpy as np
import pandas as pd
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
from tqdm import tqdm
import logging


# 设置通过IPV4进行解析以及链接
def allowed_gai_family():
    """
     https://github.com/shazow/urllib3/blob/master/urllib3/util/connection.py
    """
    family = socket.AF_INET
    return family


# 全局下载进度条组件
bar = tqdm()

# 设置日志的等级
logging.basicConfig(level=logging.INFO)

# 设置通过IPV4进行解析以及链接
urllib3_cn.allowed_gai_family = allowed_gai_family


class DownLoadThread:
    def __init__(self, urls: List[str], dirs: List[str], sizes: List[int], token: str, port: int,
                 chunk_size: int):
        """
        下载多个文件
        :param urls: 下载文件网址
        :param sizes: 下载文件大小
        :param token: 用户身份标识
        :param dirs: 保存路径
        :param port: 端口号 clash默认端口号为7080
        :param sizes: 大小
        :param chunk_size: 流式下载的块大小默认是1Mb
        """
        # 是否启用代理
        self.useClash = port is not None
        # http以及https代理配置
        self.proxies = {
            'http': 'http://127.0.0.1:' + str(port),
            'https': 'http://127.0.0.1:' + str(port),
        }
        self.urls = urls
        self.dirs = dirs
        self.size = sizes
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            'Authorization': 'Bearer ' + token
        }
        # 位运算加速等价于1024*1024等于1Mb
        self.chunk_size = chunk_size

    def download_main(self):
        """
        核心下载函数
        :return:
        """
        global bar
        # 复用链接
        s = requests.Session()
        for url, dir, size in zip(self.urls, self.dirs, self.size):
            # 存在就不进行下载
            if os.path.exists(dir) and os.path.getsize(dir) == size:
                bar.update(size)
                continue
            # todo 2023年10月21日 暂时没有更好的方法判断当前的代理端口是否有效，只能尝试采用try catch
            try:
                if self.useClash:
                    res = s.get(url, stream=True, headers=self.headers, proxies=self.proxies)
                else:
                    res = s.get(url, stream=True, headers=self.headers)
            except Exception as ex:
                logging.warning("代理端口无效,尝试不通过代理下载" + str(ex))
                res = s.get(url, stream=True, headers=self.headers)
            # 流式下载每次写入的块大小为1Mb
            with open(dir, 'wb') as f:
                for chunk in res.iter_content(self.chunk_size):
                    f.write(chunk)
                    bar.update(self.chunk_size)
            f.close()
        return


def read_csv(csv_path: str, save_dir: str, url: str) -> [List[str], List[str], List[int], int]:
    """
    # 创建文件名称池文件大小池
    :param csv_path: csv文件路径 默认格式 文件名：日期：文件大小
    :param save_dir: 保存路径
    :param url: 服务器地址
    :return: filename_list,save_list
    """
    data = np.array(pd.read_csv(csv_path, header=None, index_col=None))
    filename_list = [url + page for page in data[:, 2].tolist()]
    save_dir = [os.path.join(save_dir, filename) for filename in data[:, 0].tolist()]
    size = [int(s) for s in data[:, 1].tolist()]
    return [filename_list, save_dir, size, sum(size)]


def threading_download(filename_list: list, save_list: list, sizes: list, token: str, total_size: int,
                       thread_num: int = 8, port: int = 7080, chunk_size: int = 1 << 20):
    """
    多线程下载主函数
    :param chunk_size:
    :param port:
    :param filename_list: 下载文件的名称
    :param save_list: 下载文件的保存路径
    :param sizes: 下载文件的大小
    :param token: 用户的token
    :param total_size: 文件的总大小
    :param thread_num: 线程数量默认是8
    :return:
    """

    def download_main(filenames: List[str], save_list: List[str], size: List[int], token: str, port,
                      chunk_size: int):
        """
        下载主函数
        :param size:
        :param port:
        :param chunk_size:
        :param filenames:
        :param save_list:
        :param token:
        :return:
        """
        # 内函数目的是包装下载的函数
        # todo 2023年10月21日 可以将类更改为静态方法，避免对象创建浪费空间
        DownLoadThread(filenames, save_list, size, token, port=port, chunk_size=chunk_size).download_main()
        return

    # 进度条
    global bar
    bar = tqdm(total=total_size)
    # 分线程进行下载
    threads = []
    # 单个线程下载的数量=(向下取整)(总数量/线程数量)
    size = len(filename_list) // thread_num

    # todo 2023年10月21日 可以尝试使用线程池的方式进行下载
    # 启动线程
    for i in range(thread_num):
        t = threading.Thread(target=download_main, args=(
            filename_list[i * size:min(i * size + size, len(filename_list))],
            save_list[i * size:min(i * size + size, len(filename_list))],
            sizes[i * size:min(i * size + size, len(filename_list))],
            token, port, chunk_size,))
        # 所有下载线程都设置为守护线程，避免主线程退出，子线程变成孤儿线程
        t.setDaemon(True)
        threads.append(t)
    for i in range(thread_num):
        threads[i].start()
    for i in range(thread_num):
        threads[i].join()
    return


def log_check(save_dir: str, token: str, csv_path: str, thread_num: int,
              url: str, port: int, chunk_size: int):
    """

    :param chunk_size:
    :param port:
    :param save_dir: 保存路径
    :param token: token: 用户token
    :param csv_path: csv路径
    :param thread_num: 线程数量
    :param url:
    :return:
    """
    # 读取下载清单
    filename_list, save_dir, size, total_size = read_csv(csv_path, save_dir, url)
    # 多线程下载的主函数
    threading_download(filename_list, save_dir, size, token, total_size, thread_num, port, chunk_size)
    return


def check_complete(csv_path: str, save_dir: str) -> bool:
    """
    文件完整性校验
    主要是校验文件的大小以及文件的数量是否正确
    :return:
    """
    filename_list, save_dir, size, _ = read_csv(csv_path, save_dir, "")
    for file, s in zip(save_dir, size):
        if os.path.exists(file) and os.path.getsize(file) == s:
            continue
        else:
            return False
    return True


def download_main(save_dir: str, token: str, csv_path: str, thread_num=5, url="https://ladsweb.modaps.eosdis.nasa.gov",
                  max_try=10, port: int = 7080, chunk_size: int = 1 << 20):
    """
    # 下载主函数
    :param chunk_size: 流式下载的块大小
    :param port: port设置代理的端口，如果为None那么不采用代理
    :param url: URL
    :param save_dir: 保存路径
    :param token: TOKEN
    :param csv_path: csv路径
    :param thread_num: 线程数量
    :param max_try: 最大轮询数量
    :return:
    """
    global bar
    # 轮询下载
    while max_try != 0:
        logging.info("剩余下载轮询次数" + str(max_try))
        max_try -= 1
        # 尝试进行下载
        log_check(save_dir, token, csv_path, thread_num, url, port, chunk_size)
        bar.close()
        # 完整性校验
        if check_complete(csv_path, save_dir):
            logging.info("文件下载完成!!")
            break
    return