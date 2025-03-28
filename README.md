


# OpenFOAM 后处理动画生成工具

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenFOAM](https://img.shields.io/badge/OpenFOAM-v7%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

本工具用于处理OpenFOAM案例生成的时序图像，自动移除白色背景并生成高质量透明GIF动画。特别适用于展示多相流、粒子运动等瞬态模拟结果。

## 🚀 功能特性

- 🎨 智能背景处理
  - 自动识别并移除白色背景（RGB > 200）
  - 支持保留阴影和半透明区域
  - 自动裁剪有效区域优化图像尺寸

- ⚡ 批量处理
  - 支持多线程处理（需自定义实现）
  - 自动遍历指定目录下的所有TIFF文件
  - 保留原始文件名结构

- 🎞️ 动画生成
  - 智能帧排序（支持任意前缀+四位序号格式）
  - 可调动画参数（帧率/循环次数）
  - 透明背景优化处理

## 📦 安装依赖

```bash
pip install Pillow
```

## 🛠️ 使用指南

### 基本参数

| 参数            | 类型   | 默认值       | 说明                          |
|-----------------|--------|--------------|-----------------------------|
| input_folder    | str    | 必需         | 原始图像存储路径              |
| output_folder   | str    | 必需         | 处理后图像存储路径            |
| gif_output      | str    | 必需         | 最终生成的GIF文件路径         |
| duration        | int    | 100 (ms)    | 帧间隔时间                    |
| loop            | int    | 0 (无限循环) | 动画循环次数                  |

### 命令行使用

```bash
python animation_generator.py \
    --input /path/to/raw_images \
    --output /path/to/processed \
    --gif /path/to/output.gif \
    --duration 150 \
    --loop 3
```

### 函数调用

```python
from foam_animation import batch_process_images

batch_process_images(
    input_folder="/path/to/raw_images",
    output_folder="/path/to/processed",
    gif_output="/path/to/output.gif",
    duration=150,
    loop=3
)
```

## 📁 文件命名规范

示例文件结构：
```
input_folder/
├── case_001.0001.tif
├── case_001.0002.tif
├── ...
└── case_001.0120.tif
```

命名要求：
- 必须包含四位序号段（`.XXXX.`）
- 支持任意前缀和后缀
- 扩展名不区分大小写（.tif/.TIFF均可）

## ⚠️ 注意事项

1. **图像预处理**
   - 建议原始图像分辨率不超过4096×4096
   - 确保白色背景为纯白（RGB=255,255,255）
   - 推荐使用ParaView导出透明背景的TIFF序列

2. **性能优化**
   - 1000帧以上建议分批次处理
   - 可通过调整`colors=127`降低GIF调色板大小
   - 处理超大数据集时添加内存优化：
     ```python
     Image.MAX_IMAGE_PIXELS = None  # 解除大图限制
     ```

3. **高级定制**
   - 修改背景阈值（第18行）：
     ```python
     if item[0] > threshold and item[1] > threshold and item[2] > threshold:
     ```
   - 添加进度条（需安装tqdm）：
     ```python
     from tqdm import tqdm
     for filename in tqdm(os.listdir(input_folder)):
     ```

## 📄 许可证

[MIT License](LICENSE) © 2024 Your Name

---



