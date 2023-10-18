import traceback

import cv2
import numpy
import numpy as np
from quickverifyimg.log.logger import get_logger
SSIM_DEFAULT_KERNEL = cv2.getGaussianKernel(11, 1.5)
SSIM_DEFAULT_WINDOW = SSIM_DEFAULT_KERNEL * SSIM_DEFAULT_KERNEL.T
logger = get_logger(__name__)



def filter2valid(src, window):
    # https://cn.mathworks.com/help/matlab/ref/filter2.html#inputarg_shape
    ret = cv2.filter2D(src, -1, window, anchor=(1, 1),
                       delta=0, borderType=cv2.BORDER_CONSTANT)
    return ret[1:ret.shape[0] - window.shape[0] + 2, 1:ret.shape[1] - window.shape[1] + 2]


def ssim(img1, img2, K=(0.01, 0.03), window=SSIM_DEFAULT_WINDOW, L=255, downsample=True):
    # SSIM（structural similarity）是一种用来衡量图片相似度的指标，也可用来判断图片压缩后的质量。
    img1 = img1.astype(float)
    img2 = img2.astype(float)
    assert(img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1])

    assert(len(K) == 2 and K[0] >= 0 and K[1] >= 0)

    M, N = img1.shape[0:2]
    H, W = window.shape[0:2]
    assert(H * W >= 4 and H <= M and W <= N)

    # automatic downsampling
    f = max(1, int(round(min(M, N) / 256.0)))
    # downsampling by f
    # use a simple low-pass filter
    if downsample and f > 1:
        lpf = numpy.ones((f, f))
        lpf = lpf / numpy.sum(lpf)

        # In opencv, filter2D use the center of kernel as the anchor,
        # according to http://docs.opencv.org/2.4.8/modules/imgproc/doc/filtering.html#void filter2D(InputArray src, OutputArray dst, int ddepth, InputArray kernel, Point anchor, double delta, int borderType)
        # but in matlab, imfilter use (2, 2) (matlab array starts with 1) as the anchor,
        # To ensure the results are the same with matlab's implementation, we
        # set filter2D's anchor to (1, 1) (python array starts with 0)
        img1 = cv2.filter2D(img1, -1, lpf, anchor=(1, 1),
                            borderType=cv2.BORDER_REFLECT)
        img2 = cv2.filter2D(img2, -1, lpf, anchor=(1, 1),
                            borderType=cv2.BORDER_REFLECT)

        img1 = img1[0::f, 0::f]
        img2 = img2[0::f, 0::f]

    C1, C2 = tuple((k * L) ** 2 for k in K)

    window = window / numpy.sum(window)

    mu1 = filter2valid(img1, window)
    mu2 = filter2valid(img2, window)

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2

    mu1_mu2 = mu1 * mu2

    sigma1_sq = filter2valid(img1 * img1, window) - mu1_sq

    sigma2_sq = filter2valid(img2 * img2, window) - mu2_sq

    sigma12 = filter2valid(img1 * img2, window) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
        ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    ssim_scalar = cv2.mean(ssim_map)

    return ssim_scalar[0]


# hist直方图算法
def compare_hist(image_a, image_b):
    # Get the histogram data of image 1, then using normalize the picture for better compare
    img1_hist = cv2.calcHist([image_a], [1], None, [256], [0, 256])
    img1_hist = cv2.normalize(img1_hist, img1_hist, 0, 1, cv2.NORM_MINMAX, -1)

    img2_hist = cv2.calcHist([image_b], [1], None, [256], [0, 256])
    img2_hist = cv2.normalize(img2_hist, img2_hist, 0, 1, cv2.NORM_MINMAX, -1)
    similarity = cv2.compareHist(img1_hist, img2_hist, 0)

    return similarity

def compare_hsv(img1, img2, chanel="all"):
    """
    :param img1:
    :param img2:
    :param chanel: 返回相似度类型: all: 三通道中最低相似度， h: 色调， s: 饱和度， v: 亮度
    :return:
    """
    # 将图片转换为HSV颜色
    try:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

        def ncc(img1, img2):

            # 确保两张图像大小一致
            h = min(img1.shape[0], img2.shape[0])
            w = min(img1.shape[1], img2.shape[1])
            # img1 = img1[0:h, 0:w]
            # img2 = img2[0:h, 0:w]
            # 调整图像尺寸为相同的形状
            img1 = cv2.resize(img1, (w, h))
            img2 = cv2.resize(img2, (w, h))

            # 原有的 NCC 计算
            mean1 = np.mean(img1)
            mean2 = np.mean(img2)
            ncc = ((img1 - mean1) * (img2 - mean2)).sum() / (np.std(img1) * np.std(img2) * img1.size)

            return ncc

        h1, s1, v1 = cv2.split(img1)
        h2, s2, v2 = cv2.split(img2)
        # 保存单独的通道图像
        # cv2.imwrite('h_channel_1.jpg', h1)
        # cv2.imwrite('s_channel_1.jpg', s1)
        # cv2.imwrite('v_channel_1.jpg', v1)
        # cv2.imwrite('h_channel_2.jpg', h2)
        # cv2.imwrite('s_channel_2.jpg', s2)
        # cv2.imwrite('v_channel_2.jpg', v2)

        # logger.info(f"亮度V：{v_ncc} 饱和度S: {s_ncc} 色调H:{h_ncc}")
        if chanel == "all":
            v_ncc = ncc(v1, v2)
            s_ncc = ncc(s1, s2)
            h_ncc = ncc(h1, h2)
            similarity = min(v_ncc, s_ncc, h_ncc)
        elif chanel == "h":
            h_ncc = ncc(h1, h2)
            similarity = h_ncc
        elif chanel ==  "s":
            s_ncc = ncc(s1, s2)
            similarity = s_ncc
        else:
            v_ncc = ncc(v1, v2)
            similarity = v_ncc
        return similarity
    except Exception as e:
        logger.error(f'hsv比对出现异常：{e}')
        logger.error(traceback.format_exc())
        return 0

def compare_hsv_h(img1, img2):
    """
    比对色调
    :param img1:
    :param img2:
    :return:
    """
    return compare_hsv(img1, img2, 'h')

def compare_hsv_s(img1, img2):
    """
    比对饱和度
    :param img1:
    :param img2:
    :return:
    """
    return compare_hsv(img1, img2, 's')

def comparet_hsv_v(img1, img2):
    """
    比对亮度
    :param img1:
    :param img2:
    :return:
    """
    return compare_hsv(img1, img2, 'v')

if __name__ == '__main__':
    # image1 = cv2.imread('../downloads/screenshot/41.png')
    # image2 = cv2.imread('../downloads/0_11403/793.png')
    # image1 = cv2.imread('../tests/images/video/origin_video_frame/1.png')
    # image2 = cv2.imread('../tests/images/video/target_video_frame/1.png')

    image1 = cv2.imread('../../tests/images/3.png')
    image2 = cv2.imread('../../tests/images/1.png')
    print(compare_hist(image1, image2))
    print(compare_hsv(image1, image2))
    # print(ssim(image1, image2))