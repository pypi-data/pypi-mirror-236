import os
import time

import cv2

from quickverifyimg.log.logger import get_logger
from quickverifyimg.quick_verify import QuickVerify
from quickverifyimg.quick_verify_simple import QuickVerifySimple

logger = get_logger(__name__)

from quickverifyimg.log.logger import get_logger
from quickverifyimg.utils.aircv_utils import match_image
from quickverifyimg.utils.cv2_utils import compare_hist, ssim, compare_hsv_h, compare_hsv_s, comparet_hsv_v, compare_hsv
from quickverifyimg.utils.hash_utils import getHash_similarity_p, getHash_similarity_d, getHash_similarity_a
from quickverifyimg.utils.image_utils import crop_frame
from quickverifyimg.utils.psnr import get_psnr_similar
from quickverifyimg.utils.thread_utils import MyThread

switcher = {
    'ac_tpl': match_image,
    'hist': compare_hist,
    'cv_hsv_h': compare_hsv_h,
    'cv_hsv_s': compare_hsv_s,
    'cv_hsv_v': comparet_hsv_v,
    'cv_hsv': compare_hsv,
    'ssim': ssim,
    'psnr': get_psnr_similar,
    'hash_p': getHash_similarity_p,
    'hash_a': getHash_similarity_a,
    'hash_d': getHash_similarity_d,
}
if __name__ == '__main__':
    """
    crop_place：{ size: 需要识别的区域的大小， 百分比, offset: 需要识别的区域的左上角坐标点位置， 百分比}
    quick_verify: 是否快速校验，即不对已校验过的对照集图片继续校验
    """
    # back = os.path.join("images", "video", "back.png")
    back = os.path.join("images", "video", "target1697512295", "1.png")

    img = os.path.join("images", "video", "origin1697512295", "1.png")
    image1 = cv2.imread(back)
    # size = (0.42917, 1.0)
    # offset = (0.18125, 0)
    # crop_place = {"size": size, "offset": offset}

    # image1 = crop_frame(image1, **crop_place)
    cv2.imwrite('result.png', image1)
    image2 = cv2.imread(img)
    for key, engine in switcher.items():
        logger.info("算法 {}".format(key))
        try:
            similar = engine(image1, image2)
            logger.info("相似度{}".format(similar))
        except Exception as e:
            logger.error("相似度计算异常：{}".format(e))