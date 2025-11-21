import sys 
sys.path.append('c:\\python312\\lib\\site-packages')
import os
import imageio
from paraview.simple import *

# 定义输出路径
output_base_dir = r'G:\PaperWork\Towrite_SecondDevolopementCase\Data'

# 获取当前活动视图并配置
view = GetActiveViewOrCreate('RenderView')
view.ViewSize = [1920, 1080]
view.UseFXAA = True

# 核心修复1：使用 Orientation Axes 替代 GetAxesGrid
view.OrientationAxesVisibility = 1  # 强制显示坐标轴
view.OrientationAxesLabelColor = [0, 0, 0]  # 黑色标签
view.OrientationAxesOutlineColor = [0, 0, 0]  # 灰色边框

# 捕获初始视图参数
current_cam_params = {
    "Position": view.CameraPosition,
    "FocalPoint": view.CameraFocalPoint,
    "ViewUp": view.CameraViewUp,
    "ParallelScale": view.CameraParallelScale,
    "ViewAngle": view.CameraViewAngle
}

# 获取所有数据源
sources = GetSources()

for idx, (source_name, source) in enumerate(sources.items()):
    # 核心修复2：隐藏其他数据源
    for other_source in sources.values():
        Hide(other_source, view)
    
    # 显示当前数据源
    SetActiveSource(source)
    display = Show(source, view)
    
    case_name = os.path.basename(source.FileName)
    output_dir = os.path.join(output_base_dir, f'{case_name}_gif')
    os.makedirs(output_dir, exist_ok=True)

    # 应用视图参数
    view.CameraPosition = current_cam_params["Position"]
    view.CameraFocalPoint = current_cam_params["FocalPoint"]
    view.CameraViewUp = current_cam_params["ViewUp"]
    
    # 刷新视图
    view.ResetCamera()
    Render(view)

    # 配置颜色映射
    display.Representation = 'Surface'
    display.ColorArrayName = ['POINTS', 'alpha.water']
    alphaLUT = GetColorTransferFunction('alpha.water')
    alphaLUT.RescaleTransferFunction(0.0, 1.0)
    display.LookupTable = alphaLUT

    # 时间步处理
    animation_scene = GetAnimationScene()
    time_steps = [t for t in animation_scene.TimeKeeper.TimestepValues if 0 <= t <= 2]
    
    png_files = []
    for time_idx, time_step in enumerate(time_steps):
        animation_scene.AnimationTime = time_step
        
        # 维持视图参数
        view.CameraPosition = current_cam_params["Position"]
        view.CameraFocalPoint = current_cam_params["FocalPoint"]
        view.CameraViewUp = current_cam_params["ViewUp"]
        
        UpdatePipeline(time_step)
        Render(view)
        
        output_file = os.path.join(output_dir, f'frame_{time_idx:04d}.png')
        SaveScreenshot(
            output_file, 
            view, 
            ImageResolution=view.ViewSize,
            TransparentBackground=0
        )
        png_files.append(output_file)

    # 生成GIF（保留PNG）
    with imageio.get_writer(
        os.path.join(output_dir, f'{case_name}.gif'),
        mode='I',
        duration=0.2,
        loop=0,
        fps=15,
        subrectangles=True
    ) as writer:
        for png in png_files:
            writer.append_data(imageio.imread(png))

    print(f'生成完成: {case_name}.gif')

print('所有任务处理完毕')
