import cv2

def corp_margin_row(img, sum_thr=600):
    """
    上下切割 计算同一行像素的颜色强度，小于sum_thr 的判断为有效内容，
    :param img:
    :param sum_thr:
    :return:
    """
    img2 = img.sum(axis=2)
    (row, col) = img2.shape
    row_top = 0
    raw_down = 0
    row_top_first = False
    raw_down_first = False
    sum_axis = img2.sum(axis=1)
    for r in range(0, row):
        if sum_axis[r] < sum_thr * col:
            row_top = r
            if row_top_first:
                break
            else:
                continue
        # 当出现白色后才进行下一行检测
        row_top_first = True
    for r in range(row - 1, 0, -1):
        if sum_axis[r] < sum_thr * col:
            raw_down = r
            if raw_down_first:
                break
            else:
                continue
        # 当出现白色后才进行下一行检测
        raw_down_first = True
    if row_top < raw_down:
        new_img = img[row_top:raw_down, 0:col, 0:3]
    else:
        new_img = img
    return new_img


def corp_margin_col(img, sum_thr=600):
    """
    左右切割 计算同一列像素的颜色强度，小于sum_thr 的判断为有效内容，
    :param img:
    :param sum_thr:
    :return:
    """
    img2 = img.sum(axis=2)
    col_top = 0
    col_down = 0
    (row, col) = img2.shape
    col_top_first = False
    col_down_first = False
    sum_axis = img2.sum(axis=0)
    for c in range(0, col):
        if sum_axis[c] < sum_thr * row:
            col_top = c
            if col_top_first:
                break
            else:
                continue
        # 当出现白色后才进行下一列检测
        col_top_first = True

    for c in range(col - 1, 0, -1):
        if sum_axis[c] < sum_thr * row:
            col_down = c
            if col_down_first:
                break
            else:
                continue
        col_down_first = True

    if col_top < col_down:
        new_img = img[0:row, col_top:col_down, 0:3]
    else:
        new_img = img
    return new_img


def resize_img(img1, img2):
    # 确保两张图像大小一致
    h = min(img1.shape[0], img2.shape[0])
    w = min(img1.shape[1], img2.shape[1])
    # img1 = img1[0:h, 0:w]
    # img2 = img2[0:h, 0:w]
    # 调整图像尺寸为相同的形状
    img1 = cv2.resize(img1, (w, h))
    img2 = cv2.resize(img2, (w, h))
    return img1, img2


def get_single_auto_crop_image(img1, col_sum_thr=600, row_sum_thr=600):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img_re1 = corp_margin_row(img1, sum_thr=row_sum_thr)
    img_re1 = corp_margin_col(img_re1, sum_thr=col_sum_thr)
    return img_re1


def get_auto_crop_image(img1, img2, col_sum_thr=600, row_sum_thr=600):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_re1 = corp_margin_row(img1, sum_thr=row_sum_thr)
    img_re1 = corp_margin_col(img_re1, sum_thr=col_sum_thr)
    img_re2 = corp_margin_row(img2, sum_thr=row_sum_thr)
    img_re2 = corp_margin_col(img_re2, sum_thr=col_sum_thr)
    img_re1, img_re2 = resize_img(img_re1, img_re2)
    return img_re1, img_re2

if __name__ == '__main__':
    img1 = cv2.imread('../../tests/images/3.png')  # queryImage
    # img2 = cv2.imread('../../tests/images/6.png')  # trainImage
    # img1 = cv2.imread('E:/python_project/quickverifyimg/tests/images/DVA修改1697428845/7.png')  # queryImage
    # img2 = cv2.imread('result2.png')  # trainImage
    # img_re1, img_re2 = get_auto_crop_image(img1, img2)
    # cv2.imwrite('result.png', cv2.cvtColor(img_re1, cv2.COLOR_BGR2RGB))
    # cv2.imwrite('result2.png', cv2.cvtColor(img_re2, cv2.COLOR_BGR2RGB))
    img1 = get_single_auto_crop_image(img1)

    cv2.imwrite('result.png', cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))