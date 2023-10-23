import contextlib
import os

import cv2
import numpy as np

from quickverifyimg.log.logger import get_logger

logger = get_logger(__name__)

@contextlib.contextmanager
def video_capture(video_path: str):
    video_cap = cv2.VideoCapture(video_path)
    try:
        yield video_cap
    finally:
        video_cap.release()


def crop_frame(frame, size=(), offset=()):
    """
    获取图片的指定区域
    :param frame: 图像的narray
    :param size: 需要识别的区域的大小， 百分比
    :param offset: 需要识别的区域的左上角坐标点位置， 百分比
    """
    origin_h, origin_w = frame.shape[:2]
    if size[0] < 1 or size[1] < 1 or offset[0] < 1 or offset[1] < 1:
        skip_rect = {"startX": int(origin_w * offset[1]), "startY": int(origin_h * offset[0]),
                     "endX": int(origin_w * (offset[1] + size[1])),
                     "endY": int(origin_h * (offset[0] + size[0]))}
    else:
        skip_rect = {"startX": int(offset[1]), "startY": int(offset[0]),
                     "endX": int(offset[1] + size[1]),
                     "endY": int(offset[0] + size[0])}
    frame_crop = frame[skip_rect["startY"]:skip_rect["endY"], skip_rect["startX"]:skip_rect["endX"]]
    # logger.debug('裁剪图片：start_x: {}, start_y: {}, end_x: {}, end_y: {}'.format(skip_rect["startX"], skip_rect["startY"], skip_rect["endX"], skip_rect["endY"]))
    return frame_crop



def extract_video_frame(video_path, save_path, crop_region=None):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with video_capture(video_path) as cap:
        count = 1
        success, frame = cap.read()
        while success:
            frame_name = f"{count}.png"
            target_path = os.path.join(save_path, frame_name)
            if crop_region:
                frame = crop_frame(frame, **crop_region)
            # cv2.imwrite(target_path, frame)
            cv2.imencode(".png", frame)[1].tofile(target_path)
            success, frame = cap.read()
            count += 1

# 定义一个叫cv_imread的函数来读取中文路径的图片，filePath是图片的完整路径
def cv_imread(filePath):  # 读取中文路径的图片
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # imdecode读取的图像默认会按BGR通道来排列图像矩阵，如果后续需要RGB可以通过如下转换
    # cv_img=cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
    return cv_img