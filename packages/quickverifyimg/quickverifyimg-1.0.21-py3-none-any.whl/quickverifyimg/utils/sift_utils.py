import datetime
import logging
import os.path

import numpy as np
import cv2
import pysift
from matplotlib import pyplot as plt
from quickverifyimg.log.logger import get_logger
logger = get_logger(__name__)
MIN_MATCH_COUNT = 10

img1 = cv2.imread('../../tests/images/1.png', 0)         # queryImage
img2 = cv2.imread('../../tests/images/6.png', 0)     # trainImage


def showSiftImg(img1, img2):
    """
    TODO: 如果img1的宽度大于img2的宽度，异常报错
    :param img1:
    :param img2:
    :return:
    """
    # Compute SIFT keypoints and descriptors
    kp1, des1 = pysift.computeKeypointsAndDescriptors(img1)
    kp2, des2 = pysift.computeKeypointsAndDescriptors(img2)

    # Initialize and use FLANN
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Lowe's ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        # Estimate homography between template and scene
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)[0]

        # Draw detected template in scene image
        h, w = img1.shape
        pts = np.float32([[0, 0],
                          [0, h - 1],
                          [w - 1, h - 1],
                          [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        h1, w1 = img1.shape
        h2, w2 = img2.shape
        nWidth = w1 + w2
        nHeight = max(h1, h2)
        hdif = int((h2 - h1) / 2)
        newimg = np.zeros((nHeight, nWidth, 3), np.uint8)

        for i in range(3):
            newimg[hdif:hdif + h1, :w1, i] = img1
            newimg[:h2, w1:w1 + w2, i] = img2

        # Draw SIFT keypoint matches
        for m in good:
            pt1 = (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1] + hdif))
            pt2 = (int(kp2[m.trainIdx].pt[0] + w1), int(kp2[m.trainIdx].pt[1]))
            cv2.line(newimg, pt1, pt2, (255, 0, 0))

        plt.imshow(newimg)
        plt.show()
    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))


def getMatchNum(matches, ratio):
    """返回特征点匹配数量和匹配掩码"""
    matchesMask = [[0, 0] for i in range(len(matches))]
    matchNum = 0
    for i, (m, n) in enumerate(matches):
        if m.distance < ratio * n.distance:  # 将距离比率小于ratio的匹配点删选出来
            matchesMask[i] = [1, 0]
            matchNum += 1
    return (matchNum, matchesMask)


def getSiftSimilar(img1, img2, outputName=None, outputDir=None):
    # 创建FLANN匹配对象
    start_time = datetime.datetime.now()
    FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)

    init_time = datetime.datetime.now()
    logger.debug(f'初始化耗时：{init_time - start_time}')
    kp1, des1 = pysift.computeKeypointsAndDescriptors(img1)  # 提取样本图片的特征
    img1_time=  datetime.datetime.now()
    logger.debug(f'图片1采集特征耗时：{img1_time - init_time}')
    kp2, des2 = pysift.computeKeypointsAndDescriptors(img2)  # 提取比对图片的特征
    img2_time =  datetime.datetime.now()
    logger.debug(f'图片2采集特征耗时：{img2_time - img1_time}')

    matches = flann.knnMatch(des1, des2, k=2)  # 匹配特征点，为了删选匹配点，指定k为2，这样对样本图的每个特征点，返回两个匹配

    matche_time = datetime.datetime.now()
    logger.debug(f'匹配特征点耗时：{matche_time - img2_time}')


    (matchNum, matchesMask) = getMatchNum(matches, 0.9)  # 通过比率条件，计算出匹配程度
    matchRatio = matchNum / len(matches)

    ratio_time = datetime.datetime.now()
    logger.debug(f'计算匹配程度耗时：{ratio_time - matche_time}')

    if outputName is not None and outputDir is not None:
        drawParams = dict(matchColor=(0, 255, 0),
                          singlePointColor=(255, 0, 0),
                          matchesMask=matchesMask,
                          flags=0)
        comparisonImage = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **drawParams)
        plt.imshow(comparisonImage)
        plt.savefig(os.path.join(outputDir, f'{outputName}_{"%.2f%%" % (float(matchRatio)*100) }.png'))
        imshow_time = datetime.datetime.now()
        logger.debug(f'绘制图片耗时：{imshow_time - ratio_time}')

    all_time = datetime.datetime.now()
    logger.debug(f'总耗时：{all_time - start_time}')

    return matchRatio

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    img1 = cv2.imread('../../tests/images/1.png', 0)  # queryImage
    img2 = cv2.imread('../../tests/images/6.png', 0)  # trainImage
    outputDir = '../../tests/images/'
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    print(getSiftSimilar(img1, img2, 'test', outputDir))