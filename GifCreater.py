import sys
sys.path.append('c:\\python312\\lib\\site-packages')
import os
import imageio
from PIL import Image
from paraview.simple import *


# ===== 自定义参数区域（可根据需要调整） =====
CUSTOM_PARAMS = {
    "output_base_dir": r'G:\PaperWork\Towrite_SecondDevolopementCase\Data',
    "view_size": [1920, 1080],
    "time_window": (0, 2),  # (开始时间, 结束时间)
    "gif_duration": 0.2,
    "gif_fps": 15,
    "gif_loop": 0,
    "transparent_background": True,  # 保存截图时启用透明背景
    "remove_white_background": True,  # 额外消除白色背景像素
    "white_threshold": 5,  # 白色判断阈值，数值越大越宽松
}
# =========================================


def remove_white_background(image_path: str, threshold: int = 5) -> None:
    """将白色背景替换为透明背景。

    Args:
        image_path: PNG 文件路径。
        threshold: 单通道白色阈值，0-255。越大意味着越多接近白色的像素会被处理。
    """

    image = Image.open(image_path).convert("RGBA")
    pixels = image.getdata()

    new_pixels = []
    for r, g, b, a in pixels:
        if r >= 255 - threshold and g >= 255 - threshold and b >= 255 - threshold:
            new_pixels.append((255, 255, 255, 0))
        else:
            new_pixels.append((r, g, b, a))

    image.putdata(new_pixels)
    image.save(image_path)


# 获取当前活动视图并配置
view = GetActiveViewOrCreate('RenderView')
view.ViewSize = CUSTOM_PARAMS["view_size"]
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
    output_dir = os.path.join(CUSTOM_PARAMS["output_base_dir"], f'{case_name}_gif')
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
    start_time, end_time = CUSTOM_PARAMS["time_window"]
    time_steps = [
        t for t in animation_scene.TimeKeeper.TimestepValues
        if start_time <= t <= end_time
    ]
    
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
            TransparentBackground=int(CUSTOM_PARAMS["transparent_background"])
        )

        if CUSTOM_PARAMS["remove_white_background"]:
            remove_white_background(output_file, threshold=CUSTOM_PARAMS["white_threshold"])
        png_files.append(output_file)

    # 生成GIF（保留PNG）
    with imageio.get_writer(
        os.path.join(output_dir, f'{case_name}.gif'),
        mode='I',
        duration=CUSTOM_PARAMS["gif_duration"],
        loop=CUSTOM_PARAMS["gif_loop"],
        fps=CUSTOM_PARAMS["gif_fps"],
        subrectangles=True
    ) as writer:
        for png in png_files:
            writer.append_data(imageio.imread(png))

    print(f'生成完成: {case_name}.gif')

print('所有任务处理完毕')
