import sys
sys.path.append('c:\\python312\\lib\\site-packages')
import os
import glob
import csv
import numpy as np
from paraview.simple import *
# 按某一时间  提取某一条直线上的XYZ和合力数据
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

 

    def export_plot_over_line_x_velocity_at_time(time_point, point1, point2, variable_name, output_filename):
        try:
            # 获取当前活动的数据源
            foam_data = GetActiveSource()
            if foam_data is None:
                raise RuntimeError("没有找到活动数据源，请确保你已经加载了OpenFOAM文件并将其设置为活动数据源。")

            # 获取时间步并找到最接近的时间步
            time_steps = foam_data.TimestepValues
            if not time_steps:
                raise RuntimeError("未找到时间步信息。")
            
            # 找到最接近的时间步
            closest_time_step = min(time_steps, key=lambda x: abs(x - time_point))
            
            if abs(closest_time_step - time_point) > 1e-6:  # 如果时间步与目标时间点的差别太大，可能需要调整精度
                raise RuntimeError(f"在案例中找不到接近 {time_point} 秒的时间步。最接近的时间步是 {closest_time_step} 秒。")

            # 设置动画时间步
            animationScene = GetAnimationScene()
            animationScene.AnimationTime = closest_time_step

            # 创建 PlotOverLine 过滤器
            plot_over_line = PlotOverLine(Input=foam_data)

            # 设置直线的起点和终点
            plot_over_line.Point1 = point1  # 起点
            plot_over_line.Point2 = point2  # 终点

            # 更新管道以生成数据
            plot_over_line.UpdatePipeline()

            # 提取所需的变量（假设 X 方向速度为 U_X）
            calculator = Calculator(Input=plot_over_line)
            calculator.ResultArrayName = variable_name
            calculator.Function = variable_name

            # 更新管道以生成数据
            calculator.UpdatePipeline()

            # 获取当前案例名
            foam_file_path = foam_data.FileName
            case_name = os.path.splitext(os.path.basename(foam_file_path))[0]

            # 确定保存路径
            csv_file_path = f'G:\\data\{case_name}_{output_filename}.csv'

            # 创建一个 CSV writer
            writer = CreateWriter(csv_file_path, calculator)

            # 写入数据到 CSV 文件
            writer.UpdatePipeline()

            print(f"PlotOverLine {variable_name} data at time {closest_time_step} saved to '{csv_file_path}'")

        except Exception as e:
            print(f"发生错误: {e}")

    # 调用函数来执行任务
    export_plot_over_line_x_velocity_at_time(
        time_point=30.0,  # 指定时间点，例如5秒
        point1=[0, 1.9, 1.5],  # 起点
        point2=[20, 1.9, 1.5],  # 终点
        variable_name='U_X',  # 目标变量
        output_filename='velocityX_Xline_at_30s.csv'  # 输出文件名
    )

    

    
    # 隐藏当前数据源
    Hide(source_proxy, view)
    
    # 删除当前数据源（如果需要）
    # Delete(source_proxy)
    # del source_proxy

# 再次刷新视图以确保所有操作都已完成
Render(view)

print("All data sources have been processed.")
