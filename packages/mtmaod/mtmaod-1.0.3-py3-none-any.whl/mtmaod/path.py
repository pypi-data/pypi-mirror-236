import os, glob
from mtmtool.time import auto_parse_time_with_datefmt
import pandas as pd
from datetime import timezone

def find_paths_with_same_time(root_dir:str, columns:list, ext:str=".hdf", datefmt:str="A%Y%j.%H%M")->pd.DataFrame:
    """寻找同一时刻的文件, 并返回一个DataFrame, 列名即为columns参数中的元素, 可以按需添加时间列

    Parameters
    ----------
    root_dir : str
        根目录, 该目录下的所有子文件夹都会被遍历
    columns : list
        查找的文件类型关键字, 如"MOD02", "MOD03"等
    ext : str, optional
        文件的后缀名称列表, 注意必须带'.', by default ".hdf" (MODIS系列文件的后缀名)
    datefmt : str, optional
        文件名中时间的格式, %Y为年, %m为月, %d为月日, %j为年日, %H为时, %M为分, %S为秒, 如果一个文件有多个时间匹配该规则, 取第一个时间为文件时间, by default "A%Y%j.%H%M" (MODIS系列文件的时间格式)
    add_time_columns : bool, optional
        是否添加时间列, 为True将添加(年, 月, 月中日, 年中日, 时, 分, 秒)等列, by default False

    Returns
    -------
    pd.DataFrame
        一个DataFrame, 列名即为columns参数中的元素, 索引为文件的时间, 无效数据为NaN
    """
    # 检查输入参数
    if not os.path.isdir(root_dir):
        raise ValueError(f"root_dir: {root_dir} 不是一个有效的文件夹路径")
    if not isinstance(columns, list) or len(columns) == 0:
        raise ValueError(f"columns: {columns} 不是一个有效的列表")
    
    # 寻找同一时刻的文件, 并返回一个DataFrame, 列名即为columns参数中的元素
    df_list = []
    for file_type in columns: 
        # 保存临时数据的字典
        temp_data_dict = {}
        # 遍历所有子文件夹, 寻找符合条件的文件
        path = os.path.join(root_dir, "**", f"*{file_type}*{ext}") # 通配符 "**" 表示匹配0个或多个子文件夹
        for i in glob.glob(path, recursive=True):
            # 按照规则, 获取文件的时间, 并设置时区为UTC
            path_time = auto_parse_time_with_datefmt(i, datefmt=datefmt)[0].replace(tzinfo=timezone.utc)
            temp_data_dict[path_time] = i
        # 将字典转换为DataFrame, 方便后续合并不同列的数据
        df_list.append(pd.DataFrame.from_dict(temp_data_dict, orient="index", columns=[file_type]))
    df = pd.concat(df_list, axis=1,  join='outer') # 按照索引合并不同列的数据
    df.index.name = "datetime" # 设置索引名称
    return df
