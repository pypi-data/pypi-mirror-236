import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", message=".*Covariance of the parameters could.*")

# 检查swifter模块是否开启
try:
    from swifter import set_defaults
    set_defaults(progress_bar=False)
    _swifter_enable = True
except ImportError:
    _swifter_enable = False
    pass

def quadratic_polynomial_formula(x, a0, a1, a2):
    """二次多项式公式, 用于scipy.optimize.curve_fit(), 用于拟合AOD数据"""
    return np.exp(a0 + a1 * np.log(x) + a2 * np.log(x)**2)

def polyfit2(df, wavelength=550, x=None):
    """单个数据行的AOD插值函数, 调用quadratic_polynomial_formula"""
    # 提取要拟合的数据列
    y = df.to_numpy()
    params, _ = curve_fit(quadratic_polynomial_formula, x, y, check_finite=False, nan_policy='omit')
    # print(params)
    yfit = quadratic_polynomial_formula(wavelength, *params)
    return yfit

def group_arr_by_nan(arr):
    """将数组按nan分组, 返回字典, key为非nan的索引, value为对应的行索引"""
    index_dict = {}
    for idx, t in enumerate(arr):
        a = ",".join(map(str, np.where(~np.isnan(t))[0]))
        if a in index_dict:
            index_dict[a].append(idx)
        else:
            index_dict[a] = [idx]
    return index_dict

class LEVReader:
    """
    LEVReader实例的df变量即为读取的数据

    LEVReader实例的方法若不指定dataframe参数, 则默认使用实例的df变量作为数据源
    """

    def __init__(self, filepath, header=6) -> None:
        self.df = pd.read_csv(filepath, header=header, encoding="Windows 1252")
        self.df = self.df.replace(-999.0, np.nan)
        self.df = self._convert_time_to_utc()

    def _get_dataframe(self, dataframe=None):
        if dataframe is None:
            df = self.df.copy()
        else:
            df = dataframe.copy()
        return df

    def filter_high_quality_aod_rows(self, dataframe=None):
        """筛选出质量较高的AOD数据行, 要求AOD_440nm, AOD_500nm, AOD_675nm, AOD_870nm均大于0

        Parameters
        ----------
        dataframe : DataFrame
            数据源

        Returns
        -------
        DataFrame
            筛选后的数据
        """
        df = self._get_dataframe(dataframe)
        df = df.query("AOD_440nm > 0.0")
        df = df.query("AOD_500nm > 0.0")
        df = df.query("AOD_675nm > 0.0")
        df = df.query("AOD_870nm > 0.0")
        return df
    
    def _convert_time_to_utc(self, dataframe=None):
        df = self._get_dataframe(dataframe)
        df.loc[:, "CustomDate"] = df.loc[:, "Date(dd:mm:yyyy)"] + " " + df.loc[:, "Time(hh:mm:ss)"]
        df.loc[:, "CustomDate"] = pd.to_datetime(df.loc[:, "CustomDate"], format='%d:%m:%Y %H:%M:%S', utc=True)
        df.set_index("CustomDate", inplace=True)
        df.sort_index(inplace=True)
        return df

    def _only_keep_aod_column(self, dataframe=None):
        """只保留AOD列, 并将列名改为波长名"""
        df = self._get_dataframe(dataframe)
        # 删除非AOD以及无效的数据列
        columns = [title for title in df.columns if title.startswith('AOD_') and "Empty" not in title]
        df = df.loc[:, columns]
        df = df.replace(-999.0, np.nan)
        df = df.dropna(axis=1, how="all")
        # 将数据列名改为波长名
        columns = df.columns
        columns = [i.replace("AOD_", "").replace("nm", "") for i in columns]
        df.columns = columns
        # 根据波长大小对列名进行排序
        try:
            columns = [(int(i), i) for i in columns]
        except Exception as e:
            print("Aeronet数据格式与代码不同，请修改!")
            raise e
        columns = sorted(columns, key=lambda x: x[0])
        _, columns = zip(*columns)
        df = df.loc[:, columns]
        return df

    def interp_aod_xxxnm(self, dataframe=None, method="cubic", wavelength:float=550):
        dataframe = self._get_dataframe(dataframe)
        if method in ['linear', 'nearest', 'nearest-up', 'zero_spline', 'slinear_spline', 'quadratic_spline', 'cubic_spline']:
            # 采用scipy的插值方法
            df_aod = self._only_keep_aod_column(dataframe.copy())
            x = np.array(list(map(int, df_aod.columns)))
            y = df_aod.to_numpy()
            method_real = method.replace("_spline", "") # 为了兼容scipy的插值参数格式, 去掉_spline后缀
            group_dict = group_arr_by_nan(y)
            series_list = []
            for key in group_dict:
                columns = list(map(int, key.split(",")))
                x_temp = x[columns]
                if (method_real == "cubic" and len(x_temp) < 4) or min(x_temp) > wavelength or max(x_temp) < wavelength:
                    yfit_temp = np.zeros(len(group_dict[key]))
                    yfit_temp[:] = np.nan
                    series_list.append(pd.Series(data=yfit_temp, index=group_dict[key]))
                    continue
                y_temp = y[group_dict[key], :][:, columns]
                f = interp1d(x=x_temp, y=y_temp, kind=method_real, bounds_error=False)
                yfit_temp = f(wavelength)
                series_list.append(pd.Series(data=yfit_temp, index=group_dict[key]))
            yfit = pd.concat(series_list).sort_index()
        elif method in ["scipy_curvefit"]:
            # https://blog.csdn.net/weixin_42182090/article/details/131018277
            df_aod = self._only_keep_aod_column(dataframe.copy())
            x = np.array(list(map(int, df_aod.columns)))
            if _swifter_enable:
                yfit = df_aod.swifter.apply(polyfit2, axis=1, wavelength=wavelength, x=x)
            else:
                warnings.warn("no module 'swifter' for useing multi cpus.")
                yfit = df_aod.apply(polyfit2, axis=1, wavelength=wavelength, x=x)
        elif method in ["numpy_polyfit"]:
            df_aod = self._only_keep_aod_column(dataframe.copy())
            x = np.log(np.array(list(map(int, df_aod.columns))))
            y = np.log(df_aod.to_numpy().T)
            coef = np.polyfit(x, y, 2)
            yfit = np.exp(np.polyval(coef, np.log(wavelength)))
        elif method in ["Angstrom"]:
            df_raw = dataframe.copy()
            df_raw['440-675_Angstrom_Exponent'] = df_raw['440-675_Angstrom_Exponent'].astype(float)
            yfit = df_raw.apply(lambda x: x['AOD_440nm']*np.power((wavelength/440), -x['440-675_Angstrom_Exponent']), axis=1)
        elif method in ["cubic+scipy"]:
            yfit_scipy = self.interp_aod_xxxnm(dataframe=dataframe, method="scipy_curvefit", wavelength=wavelength)
            yfit_cubic = self.interp_aod_xxxnm(dataframe=dataframe, method="cubic_spline", wavelength=wavelength)
            yfit = (yfit_scipy + yfit_cubic)/2
        else:
            raise ValueError("method参数错误")
        return np.array(yfit)
    
    def compare(self, dataframe=None, filter_high_quality=True, wavelength=500):
        """对比不同AOD插值方法在xxxnm波段的表现, 并输出均值、最大值、耗时, 默认使用500nm波段"""
        import time
        df = self._get_dataframe(dataframe)
        df_src = df_src.query(f"AOD_{wavelength}nm > 0.0")
        if filter_high_quality:
            df_src = df_src.query("AOD_440nm > 0.0")
            df_src = df_src.query("AOD_500nm > 0.0")
            df_src = df_src.query("AOD_675nm > 0.0")
            df_src = df_src.query("AOD_870nm > 0.0")
        print("数据筛选与否: filter_high_quality = " + str(filter_high_quality))
        df = pd.DataFrame(index=df_src.index)
        df["true"] = df_src[f"AOD_{wavelength}nm"]
        df_src = df_src.drop(columns=[f"AOD_{wavelength}nm"])
        for method in ["Angstrom", "quadratic_spline", "cubic_spline", "scipy_curvefit", "cubic+scipy"]:
            name = method.split("_")[0]
            t_start = time.time()
            df[name] = self.interp_aod_xxxnm(dataframe=df_src, method=method, wavelength=wavelength)
            t_spended = time.time() - t_start
            bias = np.abs(df[name]-df["true"])
            print("{:15s}: 均误差{:10.6f}, 最大误差{:10.6f}, 耗时{:6.3f}s".format(name, bias.mean(), bias.max(), t_spended))