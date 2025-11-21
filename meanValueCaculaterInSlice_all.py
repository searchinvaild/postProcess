import sys
sys.path.append('c:\\python312\\lib\\site-packages')
import os
from paraview.simple import *
# 获取某一截面的浆液均值随着时间的变化规律
# 获取当前工作界面的所有数据源
sources = GetSources()

# 获取活动视图
view = GetActiveViewOrCreate('RenderView')

# 获取数据源列表
source_list = list(sources.items())

# 遍历所有数据源
for i, (source_name, source_proxy) in enumerate(source_list):
    # 激活第 i 个数据源
    SetActiveSource(source_proxy)
    # 显示数据源
    display = Show(source_proxy, view)
    
    # 刷新视图以确保数据源被正确显示
    Render(view)
    
    # 获取激活数据源的数据
    data_info = source_proxy.GetDataInformation()
    print(f"Data source {i+1}: {source_name[0]}")
    print(f"Number of cells: {data_info.GetNumberOfCells()}")
    print(f"Number of points: {data_info.GetNumberOfPoints()}")
    print(f"Bounds: {data_info.GetBounds()}")

    # 获取当前活动的数据源
    foam_data = GetActiveSource()

    # 获取时间步长列表
    time_steps = foam_data.TimestepValues

    # 定义截面位置
    x_position = 5.5  # 可以根据需要更改

    # 初始化结果存储
    time_series = []
    volume_fraction_averages = []

    # 遍历每个时间步长
    for time_step in time_steps:
        # 设置当前时间步长
        animation_scene = GetAnimationScene()
        animation_scene.AnimationTime = time_step

        # 创建切片
        slice = Slice(Input=foam_data)
        slice.SliceType = 'Plane'
        slice.SliceOffsetValues = [0.0]
        slice.SliceType.Origin = [x_position, 0, 0]
        slice.SliceType.Normal = [1, 0, 0]
        slice.UpdatePipeline()

        # 集成变量
        integrate_variables = IntegrateVariables(Input=slice)
        integrate_variables.UpdatePipeline()

        # 获取并处理结果
        result = servermanager.Fetch(integrate_variables)
        data = result.GetCellData().GetArray('alpha.sludge')  # 'alpha' 是相体积分数的数组名，需根据实际情况调整

        # 初始化相体积分数总和
        total_volume_fraction = 0.0

        if data:
            num_cells = data.GetNumberOfTuples()
            for i in range(num_cells):
                volume_fraction = data.GetTuple1(i)
                total_volume_fraction += volume_fraction

            # 计算平均值
            average_volume_fraction = total_volume_fraction / num_cells
        else:
            average_volume_fraction = 0.0  # 如果数据为空，设置平均值为0

        # 记录当前时间步长和相体积分数平均值
        time_series.append(time_step)
        volume_fraction_averages.append(average_volume_fraction)
        Delete(slice)
        del slice
        Delete(integrate_variables)
        del integrate_variables

    # 确定保存路径
    foam_file_path = foam_data.FileName
    case_name = os.path.splitext(os.path.basename(foam_file_path))[0]
    csv_file_path = f'G:\\data2\{case_name}_volumefraction_alongT.csv'
    # 将结果保存为CSV文件
    with open(csv_file_path, 'w') as file:
        file.write('Time,Average Volume Fraction\n')
        for time, avg_volume_fraction in zip(time_series, volume_fraction_averages):
            file.write(f'{time},{avg_volume_fraction}\n')

    print(f"Volume fraction time series saved to '{csv_file_path}'")

    # 打印结果以检查
    print(volume_fraction_averages)
    

    
    # 隐藏当前数据源
    Hide(source_proxy, view)
    
    # 删除当前数据源（如果需要）
    # Delete(source_proxy)
    # del source_proxy

# 再次刷新视图以确保所有操作都已完成
Render(view)

print("All data sources have been processed.")
