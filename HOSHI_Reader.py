# -*- coding: utf-8 -*-
"""
Created on Fri Jan 3rd

@author: Bingyang Tan
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.ticker as ticker
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

G_GRAV = 6.67428e-8 # in cm^3/g/s^2

R_SUN = 6.9566e10 # in cm
M_SUN = 1.9891e33 # in g
L_SUN = 3.839e33 # in erg/

def set_plot_xtickers(
    ax: plt.Axes,
    x_interval: float, 
    x_minorTicks_num: int,
    major_tick_length: float = 6,
    minor_tick_length: float = 3,
    
    ):
        # 设置刻度线
    ax.tick_params(axis='both', which='major', direction='in', length=major_tick_length, top=True, bottom=True)
    ax.tick_params(axis='both', which='minor', direction='in', length=minor_tick_length, top=True, bottom=True)
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_interval))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(x_minorTicks_num))
    
    return None

def set_plot_ytickers(
    ax: plt.Axes,
    y_interval: float, 
    y_minorTicks_num: int,
    major_tick_length: float = 6,
    minor_tick_length: float = 3,
    
    ):
        # 设置刻度线

    ax.tick_params(axis='both', which='major', direction='in', length=major_tick_length, left=True, right=True)
    ax.tick_params(axis='both', which='minor', direction='in', length=minor_tick_length, left=True, right=True)
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(y_interval))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(y_minorTicks_num))
    
    return None

class HOSHI_Reader:
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.summary_dir = os.path.join(work_dir, 'summary')
        self.writestr_dir = os.path.join(work_dir, 'writestr')
        self.check_dir()

    
    def check_dir(self):
        if not os.path.exists(self.summary_dir):
            #os.makedirs(self.summary_dir)
            logging.info('No summary directory found')
        if not os.path.exists(self.writestr_dir):
            #os.makedirs(self.writestr_dir)
            logging.info('No writestr directory found')
        
class HoshiHistory(HOSHI_Reader):
    var_names = []
    def __init__(self, path):
        if os.path.isdir(path):
            if path.endswith('summary'):
                self.path = os.path.join(path, 'summary.txt')
            else:
                self.path = os.path.join(path, 'summary', 'summary.txt')
        elif os.path.isfile(path) and path.endswith('summary.txt'):
            self.path = path
        else:
            raise ValueError("Invalid path provided. Path should be either a directory or a summary.txt file.")
        
        self.var_names = self._get_var_names()

    def _get_var_names(self) -> list:
        with open(self.path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    header_line = line
                    break
        
        cleaned_header = header_line.replace('#', '')
        cleaned_header = re.sub(r'\d+:', ' ', cleaned_header)
        variable_names = cleaned_header.split()

        return variable_names
    
    def data(self, var_name: str, dtype=float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the file.")
            return np.array([])  # 返回一个空的 numpy 数组
        
        # 获取变量名在 var_names 中的索引
        col_index = self.var_names.index(var_name)
        
        # 使用 pandas 读取指定列的数据
        df = pd.read_csv(
            self.path, 
            comment='#', 
            delim_whitespace=True, 
            header=None, 
            usecols=[col_index],
            dtype=dtype,
            )
        return df.iloc[:, 0].values
    

class HoshiProfile(HOSHI_Reader):
    def __init__(self, path: str, str_num: int):
        if os.path.isdir(path):
            self.path = os.path.join(path, 'writestr', f'str{str_num:05d}.txt')
        elif os.path.isfile(path) and path.endswith(f'str{str_num:05d}.txt'):
            self.path = path
        else:
            logging.error("Invalid path provided. Path should be either a directory or a profile file.")
            return
        
        self.var_names = self._get_var_names()

    def _get_var_names(self) -> list:
        with open(self.path, 'r') as file:
            # jump the first two lines
            for _ in range(2):
                next(file)
            # get the line with variable names
            header_line = next(file)
        
        cleaned_header = header_line.replace('#', '')
        cleaned_header = re.sub(r'\d+:', ' ', cleaned_header)
        variable_names = cleaned_header.split()

        return variable_names
    
    def data(self, var_name: str, dtype = float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the file.")
            return np.array([])  # 返回一个空的 numpy 数组
        
        # 获取变量名在 var_names 中的索引
        col_index = self.var_names.index(var_name)
        
        # 使用 pandas 读取指定列的数据
        df = pd.read_csv(
            self.path, 
            comment='#', 
            delim_whitespace=True, 
            header=None, 
            usecols=[col_index],
            skiprows=2,
            dtype=dtype,
            )
        return df.iloc[:, 0].values


    