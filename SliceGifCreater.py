import sys
sys.path.append('c:\\python312\\lib\\site-packages')
import os
import numpy as np
import imageio
from paraview.simple import *
## 需要自己提前固定视图 调整好图例
# 定义输出路径
output_base_dir = r'G:\data'

# 获取活动视图
view = GetActiveViewOrCreate('RenderView')

# 获取当前活动的数据源
sources = GetSources()
if not sources:
    raise RuntimeError("No data sources found.")

# 遍历所有数据源
for source_name, source in sources.items():
    SetActiveSource(source)

    # 创建切片
    slice = Slice(Input=source)
    slice.SliceType = 'Plane'
    slice.SliceOffsetValues = [0.0]
    slice.SliceType.Normal = [1, 0, 0]
    slice.SliceType.Origin = [5.5, 10, 10]

    # 更新视图以显示切片
    Show(slice, view)
    Hide(source, view)

    # 获取显示属性
    slice_display = GetDisplayProperties(slice, view=view)

    # 设置切片的显示属性
    slice_display.SetRepresentationType('Surface')
    slice_display.Opacity = 1.0  # 设置不透明度为1.0以隐藏平面
    slice_display.MeshVisibility = 0  # 关闭网格可见性

    # 隐藏切片的平面显示
    slice_display.SetScalarBarVisibility(view, False)

    # 展示物理场选取alpha.sludge（点数据）
    ColorBy(slice_display, ('POINTS', 'p_rgh'))
    slice_display.RescaleTransferFunctionToDataRange(True, False)
    slice_display.UpdatePipeline()

    # 获取输出目录
    case_name = os.path.basename(os.path.dirname(source.FileName))
    output_dir = os.path.join(output_base_dir, case_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取时间步长
    animation_scene = GetAnimationScene()
    time_steps = animation_scene.TimeKeeper.TimestepValues

    # 保存每个时间步长的切片云图为PNG
    for time_step in time_steps:
        animation_scene.AnimationTime = time_step
        Render()

        output_file = os.path.join(output_dir, f'{case_name}_time_{time_step:.4f}.png')
        SaveScreenshot(output_file, view)

    # 隐藏当前切片
    Hide(slice, view)

print("All data sources have been processed.")
