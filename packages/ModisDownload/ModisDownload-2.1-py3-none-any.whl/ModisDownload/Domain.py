# -*- coding: utf-8 -*-
# @Time    : 2022/5/21 22:20
# @Author  : qxcnwu
# @FileName: Domain.py
# @Software: PyCharm

import numpy as np
import logging

# 设置日志的等级
logging.basicConfig(level=logging.INFO)


def list_to_str(lists):
    string = ""
    for i in lists:
        string += str(i) + ":"
    return string[0:-1]


class Sensor:
    def __init__(self):
        """
        传感器json文件解析类
        """
        self.ESDT = None
        self.Lname = None
        self.isImg = None
        self.isData = None
        self.isAnc = None
        self.geoESDT = None
        self.day = None
        self.night = None
        self.dnbound = None
        self.period = None
        self.plevel = None
        self.res = None
        self.grps = None
        self.sensor = None
        self.platform = None
        self.instr = None
        self.collections = None

    def __str__(self):
        return self.ESDT + "," + list_to_str(self.collections) + "," + self.sensor


class DownLoadFile:
    def __init__(self, obj: dict):
        """
        下载文件json解析类
        :param obj: dict
        """
        self.obj = obj
        self.name = None
        self.size = None
        self.fileURL = None
        self.GRingLongitude1 = None
        self.GRingLongitude2 = None
        self.GRingLongitude3 = None
        self.GRingLongitude4 = None
        self.GRingLatitude1 = None
        self.GRingLatitude2 = None
        self.GRingLatitude3 = None
        self.GRingLatitude4 = None
        self.init_this()

    def init_this(self):
        for (key, value) in self.obj.items():
            if dir(self).__contains__(key):
                setattr(self, key, value)
        return

    def __str__(self):
        return self.name + "," + self.size + "," + self.fileURL


class Country:
    def __init__(self, contry_dict: dict):
        """
        国家与地区Json解析类
        :param contry_dict:
        """
        self.country_dict = contry_dict
        self.CNTRY_NAME = None
        self.ISOSHRTNAM = None
        self.LONG_NAME = None
        self.ISO_NUM = None
        self.geometry = None
        self.properties = None
        self.coordinates = None

        self.lon_max = None
        self.lon_min = None
        self.lat_max = None
        self.lat_min = None

        self.canuse = False

        # 初始化类
        self.init_this()

    def init_this(self):
        if not self.country_dict.keys().__contains__("properties"):
            logging.warning("Some things wrong in parse properties")
            return
        self.properties = self.country_dict.get("properties")
        self.geometry = self.country_dict.get("geometry")
        self.canuse = self.parse_properties() and self.parse_geometry()
        return

    def parse_properties(self):
        try:
            self.CNTRY_NAME = self.properties["CNTRY_NAME"].lower()
            self.ISOSHRTNAM = self.properties["ISOSHRTNAM"]
            self.LONG_NAME = self.properties["LONG_NAME"]
            self.ISO_NUM = self.properties["ISO_NUM"]
            return True
        except Exception as ex:
            logging.error("parse properties error!!")
        return False

    def _common_utiles(self, array):
        """
        公共组件
        :param array:
        :return:
        """
        self.lon_max = str(np.round(np.max(array[:, 0]), 2))
        self.lon_min = str(np.round(np.min(array[:, 0]), 2))
        self.lat_max = str(np.round(np.max(array[:, 1]), 2))
        self.lat_min = str(np.round(np.min(array[:, 1]), 2))
        return

    def parse_geometry(self):
        try:
            self.coordinates = self.geometry["coordinates"]
            array = np.reshape(np.array(self.coordinates), (-1, 2))
            self._common_utiles(array)
            return True
        except Exception as ex:
            try:
                return self.parse_error()
            except Exception as ex:
                logging.error(self.coordinates + " parse geometry error!!")
        return False

    def parse_error(self):
        """
        解析错误
        :return:
        """

        temp_data = np.array(self.coordinates)
        temp_list = []
        if len(temp_data.shape) == 1:
            for i in temp_data:
                temp_list.append(np.reshape(i, (-1, 2)))
            temp = np.vstack(temp_list)
            self._common_utiles(temp)
            return True
        else:
            logging.error(self.coordinates)
            logging.error("parse geometry error!!")
            return False

    def __str__(self):
        return "x" + self.lon_min + "y" + self.lat_max + ",x" + self.lon_max + "y" + self.lat_min
