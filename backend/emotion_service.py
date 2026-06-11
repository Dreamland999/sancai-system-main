"""
情绪识别服务 —— OpenCV MobileFaceNet + YuNet

模型文件:
  backend/models/facial_expression_recognition_mobilefacenet_int8bq.onnx  (情绪分类)
  backend/models/face_detection_yunet_2023mar.onnx                        (人脸检测)

用法:
    service = EmotionService()
    result = service.predict(image_bytes)
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional

import onnxruntime as ort

# ─── 模型路径 ──────────────────────────────────────────
MODEL_DIR = Path(__file__).resolve().parent / "models"
EMOTION_MODEL = MODEL_DIR / "facial_expression_recognition_mobilefacenet_int8bq.onnx"
FACE_MODEL    = MODEL_DIR / "face_detection_yunet_2023mar.onnx"

# ─── 类别顺序 ──────────────────────────────────────────
CLASSES = ["angry", "disgust", "fearful", "happy", "neutral", "sad", "surprised"]

EMOTION_CN = {
    "angry":    "生气",
    "disgust":  "厌恶",
    "fearful":  "害怕",
    "happy":    "开心",
    "neutral":  "平静",
    "sad":      "低落",
    "surprised":"惊讶",
    "unknown":  "不确定",
}

# ─── 置信度阈值 ────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.55

# ─── YuNet 参数 ────────────────────────────────────────
YUNET_INPUT_SIZE = (320, 320)
YUNET_SCORE_THRESH = 0.6
YUNET_NMS_THRESH = 0.3


class EmotionService:
    """OpenCV MobileFaceNet 情绪识别 + YuNet 人脸检测"""

    def __init__(self):
        for path, name in [(EMOTION_MODEL, "情绪模型"), (FACE_MODEL, "人脸检测模型")]:
            if not path.exists():
                raise FileNotFoundError(f"{name}不存在: {path}")

        self._emotion_session = ort.InferenceSession(
            str(EMOTION_MODEL), providers=["CPUExecutionProvider"]
        )
        # 量化模型可能把 initializer 暴露为输入
        # 给所有非数据输入传零张量即可正常运行
        self._emotion_feed = {}
        self._emotion_input = None
        for inp in self._emotion_session.get_inputs():
            shape = list(inp.shape)
            if shape == [1, 3, 112, 112]:
                self._emotion_input = inp.name
            else:
                self._emotion_feed[inp.name] = np.zeros(shape, dtype=np.float32)

        # YuNet 人脸检测器
        self._face_detector = cv2.FaceDetectorYN.create(
            str(FACE_MODEL), "", YUNET_INPUT_SIZE,
            YUNET_SCORE_THRESH, YUNET_NMS_THRESH
        )

    # ── 公开接口 ───────────────────────────────────

    def predict(self, image_bytes: bytes) -> dict:
        """
        从图片字节流预测情绪

        返回:
          { success, emotion, emotion_cn, confidence, scores, message }
        """
        img = self._decode_image(image_bytes)

        face = self._detect_face(img)
        if face is None:
            return self._unknown_result("未检测到清晰人脸或置信度过低")

        tensor = self._preprocess(face)
        scores = self._infer(tensor)

        best_idx = int(np.argmax(list(scores.values())))
        best_class = CLASSES[best_idx]
        best_score = scores[best_class]

        if best_score < CONFIDENCE_THRESHOLD:
            return self._unknown_result("未检测到清晰人脸或置信度过低")

        return {
            "success": True,
            "emotion": best_class,
            "emotion_cn": EMOTION_CN[best_class],
            "confidence": round(best_score, 4),
            "scores": {k: round(v, 4) for k, v in scores.items()},
            "message": "ok",
        }

    # ── 图片解码 ───────────────────────────────────

    @staticmethod
    def _decode_image(image_bytes: bytes) -> np.ndarray:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("无法解码图片")
        return img

    # ── 人脸检测 (YuNet) ───────────────────────────

    def _detect_face(self, img: np.ndarray) -> Optional[np.ndarray]:
        """
        YuNet 检测人脸，返回最大的一张裁剪人脸 BGR 图像。
        后续如需替换为其他检测器，只需修改此方法。
        """
        h, w = img.shape[:2]
        self._face_detector.setInputSize((w, h))
        _, faces = self._face_detector.detect(img)

        if faces is None or len(faces) == 0:
            return None

        # 取置信度最高的一张脸
        best = max(faces, key=lambda f: f[14])
        score = best[14]
        if score < YUNET_SCORE_THRESH:
            return None

        # bbox: x, y, w, h (前4个值)
        x, y, bw, bh = int(best[0]), int(best[1]), int(best[2]), int(best[3])
        pad = int(max(bw, bh) * 0.25)
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(w, x + bw + pad)
        y2 = min(h, y + bh + pad)
        return img[y1:y2, x1:x2]

    # ── 预处理 (MobileFaceNet) ─────────────────────

    @staticmethod
    def _preprocess(face_bgr: np.ndarray) -> np.ndarray:
        """
        BGR 人脸 → MobileFaceNet 输入 [1, 3, 112, 112]

        MobileFaceNet 预处理:
          1. BGR → RGB
          2. Resize 112×112
          3. float32, 范围 [0, 1]
          4. HWC → NCHW
        """
        face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
        face_resized = cv2.resize(face_rgb, (112, 112))
        face_f32 = face_resized.astype(np.float32) / 255.0
        tensor = face_f32.transpose(2, 0, 1)  # HWC → CHW
        return tensor[np.newaxis, :, :, :].astype(np.float32)

    # ── 推理 ──────────────────────────────────────

    def _infer(self, tensor: np.ndarray) -> dict:
        feed = dict(self._emotion_feed)
        feed[self._emotion_input] = tensor
        raw = self._emotion_session.run(None, feed)
        logits = np.array(raw[0]).squeeze()
        probs = self._softmax(logits)
        return {CLASSES[i]: float(probs[i]) for i in range(len(CLASSES))}

    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        e = np.exp(x - np.max(x))
        return e / e.sum()

    @staticmethod
    def _unknown_result(message: str) -> dict:
        return {
            "success": True,
            "emotion": "unknown",
            "emotion_cn": EMOTION_CN["unknown"],
            "confidence": 0,
            "scores": {},
            "message": message,
        }


# ─── 模块级单例 ──────────────────────────────────────

_service: Optional[EmotionService] = None


def get_service() -> EmotionService:
    global _service
    if _service is None:
        _service = EmotionService()
    return _service
