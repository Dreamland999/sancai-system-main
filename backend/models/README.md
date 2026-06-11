# 情绪识别模型

## 模型文件

| 文件 | 用途 | 来源 |
|------|------|------|
| `face_detection_yunet_2023mar.onnx` | YuNet 人脸检测 | opencv/face_detection_yunet |
| `facial_expression_recognition_mobilefacenet_int8bq.onnx` | MobileFaceNet 情绪分类 | opencv/facial_expression_recognition |

## 下载命令

```bash
python -c "
from huggingface_hub import hf_hub_download
import shutil
hf_hub_download('opencv/face_detection_yunet', 'face_detection_yunet_2023mar.onnx')
hf_hub_download('opencv/facial_expression_recognition', 'facial_expression_recognition_mobilefacenet_2022july_int8bq.onnx')
"
```

## 类别顺序

```
0: angry     (生气)
1: disgust   (厌恶)
2: fearful   (害怕)
3: happy     (开心)
4: neutral   (平静)
5: sad       (低落)
6: surprised (惊讶)
```

## 预处理

- 情绪模型输入: [1, 3, 112, 112], float32, [0, 1]
- 人脸检测: YuNet, 置信度阈值 0.6
