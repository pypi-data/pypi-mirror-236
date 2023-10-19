from mtmaod.aeronet import LEVReader


if __name__ == '__main__':
    # 读取数据
    lev_file_path = r"E:\data-dbl\AOD_retrieval\AERONET\AERONET_lev15\19930101_20210102_Beijing_RADI.lev15"
    reader = LEVReader(lev_file_path)

    # 筛选高质量数据
    df = reader.filter_high_quality_aod_rows()

    # 插值550nm波段的AOD, 当使用"scipy_curvefit" 或 "cubic+scipy"方法时, 调用多核CPU, 需要在"if __name__ == '__main__'"环境中使用
    df["AOD_550nm"] = reader.interp_aod_xxxnm(df, method="cubic_spline", wavelength=550)

    # 对比不同AOD插值方法在500nm波段的表现
    reader.compare(df, filter_high_quality=True, wavelength=500)

    # 更新reader实例的df变量
    reader.df = df

    # 只保留AOD列
    df_aod = reader._only_keep_aod_column(df)

