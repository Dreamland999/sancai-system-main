/**
 * 情绪识别 API — 上传人脸图片到后端 ONNX 模型推理
 *
 * 后端接口: POST /api/emotion/predict
 * 请求格式: multipart/form-data, 字段名 file
 */

const BASE_URL = 'http://10.191.219.32:8000';

export function predictEmotion(filePath, timeout = 10000) {
  return new Promise((resolve, reject) => {
    console.log('[emotion] upload start', filePath);

    const task = uni.uploadFile({
      url: `${BASE_URL}/api/emotion/predict`,
      filePath: filePath,
      name: 'file',
      timeout: timeout,
      success(res) {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          console.error('[emotion] upload failed, status', res.statusCode);
          reject(new Error(`HTTP ${res.statusCode}`));
          return;
        }
        try {
          const data = JSON.parse(res.data);
          console.log('[emotion] response', data);
          resolve(data);
        } catch (e) {
          console.error('[emotion] JSON parse failed', e);
          reject(e);
        }
      },
      fail(err) {
        console.error('[emotion] upload failed', err);
        reject(err);
      }
    });
  });
}
