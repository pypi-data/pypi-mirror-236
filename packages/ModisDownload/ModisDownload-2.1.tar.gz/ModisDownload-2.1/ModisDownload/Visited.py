import json
import os

import numpy as np
import pandas as pd

from ModisDownload.DownloadMain import download_main
from ModisDownload.GetAPI import sensor, search, searchData, geo

import logging


# 设置日志
logging.basicConfig(level=logging.INFO)


def get_geo():
    """
    获取geo
    :return:
    """
    g = geo()
    g.parse_answer()
    return g


class GetHtml:
    def __init__(self, token):
        """

        :param token:
        """

        logging.info(
            "查询前请确保Token字符串的有效性！具体Token获取请访问 https://ladsweb.modaps.eosdis.nasa.gov/#generate-token")
        self.answer = []
        self.update = False
        self.token = token
        self.sensor = self.get_sensor()
        self.g = get_geo()

    def get_sensor(self, refresh=False):
        """
        获取传感器参数
        :param refresh: 是否重新初始化
        :return:
        """
        self.update = True
        sens = sensor()
        if refresh:
            sens.visit()
            sens.parse_answer()
        else:
            if not os.path.exists(sens.csv_path):
                self.get_sensor(True)
        sens.init_dict()
        return sens

    def get_search(self, sensor_name: str, date: str, area: str):
        """
        查询
        :param area:
        :param sensor_name:
        :param date:
        :return:
        """
        searchdata = searchData(sensor_name, date, area, self.sensor, self.g)
        sea = search(searchdata)
        sea.make_post_url()
        sea.parse_answer()
        return sea

    def download_main(self, sensor_name: str, dates: str, area: str, download_dir: str, thread_num: int = 5,
                      max_try: int = 10, port: int = None, chunk_size: int = 1 << 20):
        """
        下载
        :param area:
        :param chunk_size:
        :param max_try:
        :param port:
        :param thread_num:
        :param sensor_name:
        :param dates:
        :param download_dir:
        :return:
        """
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        sea = self.get_search(sensor_name, dates, area.lower())
        if not sea.canuse:
            logging.warning("未查询到可下载数据")
            return
        download_main(download_dir, self.token, sea.file_name_path, thread_num=thread_num,
                      max_try=max_try, port=port, chunk_size=chunk_size)
        return

    def download_main_url(self, sensor_name: str, dates: str, area: str, download_dir: str, save_dir: str):
        """
        只导出url
        :param save_dir:
        :param area:
        :param sensor_name:
        :param dates:
        :param download_dir:
        :return:
        """
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        sea = self.get_search(sensor_name, dates, area.lower())
        if not sea.canuse:
            logging.warning("未查询到可下载数据")
            return
        sea.read_csv(save_dir)
        return


def reload():
    origin = os.path.join(os.path.dirname(__file__), "temp")
    for file in os.listdir(origin):
        try:
            os.remove(os.path.join(origin, file))
        except Exception as ex:
            pass
    logging.info("重新初始化完成")
    return


def search_p():
    GetHtml("")
    origin = os.path.dirname(__file__) + "/temp/sensor.csv"
    data = np.array(pd.read_csv(origin, header=None, index_col=False))
    for idx, i in enumerate(data):
        logging.info(idx, " ", i)
    return data


def search_area():
    GetHtml("")
    origin = os.path.dirname(__file__) + "/temp/country.json"
    with open(origin, "r") as fd:
        dicts = json.load(fd)
    for key, value in dicts.items():
        logging.info(key, ":", value)
    return dicts
