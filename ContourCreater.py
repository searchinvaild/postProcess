from paraview.simple import *
import csv
import os
# 输出为轮廓线的坐标
# 获取活动数据源（假设已经加载了OpenFOAM文件）
foam_data = GetActiveSource()

# 获取时间步信息
time_steps = foam_data.TimestepValues

# 确保时间步信息存在
if not time_steps:
    raise RuntimeError("未找到时间步信息。")

# 设置时间步为39s（假设39s在时间步列表中）
target_time = 39.0
if target_time not in time_steps:
    raise RuntimeError(f"时间步 {target_time}s 不存在于时间步列表中。")

# 更新数据源到特定时间步
foam_data.UpdatePipeline(target_time)

# 创建等值线
contour = Contour(Input=foam_data)
contour.ContourBy = ['POINTS', 'alpha.sludge']
contour.Isosurfaces = [0.5]
contour.PointMergeMethod = "Uniform Binning"

# 显示等值线
contour_display = Show(contour)

# 刷新视图
Render()

# 获取等值线数据
contour_data = servermanager.Fetch(contour)

# 导出等值线XY坐标信息到CSV文件
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
case_name = foam_data.SMProxy.GetXMLName().split('/')[-1].split('.')[0]
csv_file_path = os.path.join(desktop_path, f"{case_name}_contour_xy.csv")

with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['X', 'Y'])

    # 处理多块数据集
    if contour_data.IsA("vtkMultiBlockDataSet"):
        for i in range(contour_data.GetNumberOfBlocks()):
            block = contour_data.GetBlock(i)
            if block is not None:
                for j in range(block.GetNumberOfPoints()):
                    point = block.GetPoint(j)
                    csvwriter.writerow([point[0], point[1]])
    else:
        for i in range(contour_data.GetNumberOfPoints()):
            point = contour_data.GetPoint(i)
            csvwriter.writerow([point[0], point[1]])

print(f"等值线提取和绘制完成，XY坐标信息已导出到 {csv_file_path}")
