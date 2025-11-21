# postProcess 脚本集

本仓库收集了一组基于 ParaView 的 Python 脚本，用于处理 OpenFOAM 模型的可视化和数据提取任务。每个脚本都针对特定的后处理需求，例如生成等值线、导出沿线速度、创建切片序列 GIF，或计算截面体积分数。下表为脚本概览：

| 脚本 | 主要功能 |
| --- | --- |
| `ContourCreater.py` | 在指定时间步提取等值线并导出 XY 坐标。 |
| `ExtractVelocityAlongLine.py` | 在给定时间沿直线提取速度（或其他场量）并输出 CSV。 |
| `GifCreater.py` | 为每个数据源生成时间序列截图并合成为 GIF。 |
| `SliceGifCreater.py` | 对所有数据源创建固定平面切片，逐时间步保存 PNG。 |
| `TotalValueCaculaterBehindSlice_all.py` | 计算切片两侧的体积分数总和随时间变化并导出。 |
| `meanValueCaculaterInSlice_all.py` | 计算指定截面上场量的时间序列平均值并保存 CSV。 |

## 使用说明

所有脚本均假设在 ParaView 的 Python 环境中运行（`paraview.simple` 可用），且已加载 OpenFOAM 数据。部分脚本包含硬编码的输出路径和字段名称，使用前请根据实际路径与字段调整。

### ContourCreater.py
- 作用：在目标时间步（默认 39s）生成 `alpha.sludge` 的等值线（等值面 0.5），导出轮廓线 XY 坐标到桌面 CSV 文件。
- 关键点：
  - 使用当前活动数据源和时间步列表；时间步缺失会抛错。
  - 自动处理 MultiBlock 数据集，将所有块的点坐标写入 CSV。

### ExtractVelocityAlongLine.py
- 作用：遍历当前会话的所有数据源，在指定时间点沿给定直线导出字段（默认 `U_X`）到 CSV。
- 关键点：
  - 选择最接近的时间步并校验时间点是否存在。
  - 使用 `PlotOverLine` 与 `Calculator` 提取线上的点数据，并将结果写入 `G:\data` 下的 CSV。
  - 默认直线为 `[0, 1.9, 1.5]` 到 `[20, 1.9, 1.5]`，可自行修改。

### GifCreater.py
- 作用：对每个数据源按时间窗口截图并合成为 GIF。
- 关键点：
  - `CUSTOM_PARAMS` 中配置输出目录、视窗大小、时间窗口、GIF 播放参数、颜色字段等。
  - 在生成每个 GIF 时会隐藏其他数据源、重置相机、应用色标并可选去除白色背景。
  - PNG 将保留在输出目录，以便后续复用。

### SliceGifCreater.py
- 作用：对所有数据源创建固定平面切片（默认法向 `[1,0,0]`，原点 `[5.5, 10, 10]`），遍历时间步保存 PNG。
- 关键点：
  - 需提前调整视图/图例；脚本会隐藏原始源，保留切片显示。
  - 颜色映射默认使用 `p_rgh` 点数据，可根据需求更换。
  - 输出目录基于数据源文件夹名创建在 `G:\data` 下。

### TotalValueCaculaterBehindSlice_all.py
- 作用：批量读取指定目录下的 `.foam` 案例，计算切片两侧（`y<5.5` 与 `y>=5.5`）的 `alpha.water` 总和随时间变化，导出 CSV。
- 关键点：
  - 需要设置 `foam_dir`（.foam 文件路径）和 `output_dir`。
  - 在每个时间步获取切片数据，遍历 MultiBlock 数据累加点的 `alpha.water` 数值。
  - CSV 列为 `Time, Left Volume Fraction Sum, Right Volume Fraction Sum`。

### meanValueCaculaterInSlice_all.py
- 作用：对每个数据源计算指定截面（默认 `x=5.5`）的 `alpha.sludge` 平均值随时间的变化，保存 CSV。
- 关键点：
  - 遍历时间步创建切片并用 `IntegrateVariables` 计算单元数据，再求平均。
  - 输出路径默认 `G:\data2`，文件名包含案例名。
  - 完成后打印每个案例的平均值序列，便于快速检查。

## 快速开始
1. 在 ParaView 的 Python Shell 或 `pvpython` 中打开脚本前，确保已加载目标 OpenFOAM 数据或将路径参数改为你的文件位置。
2. 根据自身环境更新脚本内的硬编码路径（如 `G:\data`、`G:\case`）、字段名（如 `alpha.water`、`alpha.sludge`、`U_X`）以及切片/时间窗口等参数。
3. 逐个运行所需脚本即可完成对应的后处理任务。

## 注意事项
- 脚本默认使用 Windows 路径分隔符，请在其他平台上相应调整。
- 部分脚本依赖 Pillow、imageio 等第三方库，请确保在 ParaView 的 Python 环境中可用。
- 建议在运行前保存 ParaView 会话，以便出现异常时快速恢复视图与数据源配置。
