import math
import os
import time

import cv2
from natsort import ns, natsorted

import copy

from quickverifyimg.log.logger import get_logger
from quickverifyimg.utils.aircv_utils import match_image
from quickverifyimg.utils.crop_utils import get_auto_crop_image, resize_img, get_single_auto_crop_image
from quickverifyimg.utils.cv2_utils import compare_hist, ssim, compare_hsv_h, compare_hsv_s, comparet_hsv_v, compare_hsv
from quickverifyimg.utils.hash_utils import getHash_similarity_p, getHash_similarity_d, getHash_similarity_a
from quickverifyimg.utils.image_utils import crop_frame, extract_video_frame, cv_imread
from quickverifyimg.utils.psnr import get_psnr_similar
from quickverifyimg.utils.thread_utils import MyThread
logger = get_logger(__name__)

switcher = {
    'ac_tpl': match_image,
    'hist': compare_hist,
    'cv_hsv':compare_hsv,
    'cv_hsv_h': compare_hsv_h,
    'cv_hsv_s': compare_hsv_s,
    'cv_hsv_v': comparet_hsv_v,
    'ssim': ssim,
    'psnr': get_psnr_similar,
    'hash_p': getHash_similarity_p,
    'hash_a': getHash_similarity_a,
    'hash_d': getHash_similarity_d,
}


class QuickVerifyVideo():
    def __init__(self, verify_engine_list, match_rate_threshold,  crop_place=None, quick_verify=False, frame_save_dir=None, background_path=None, offset_size=10, background_similar=0.998, auto_crop=False, col_sum_thr=600, row_sum_thr=600, log=None):
        """
        :param verify_engine_list: 匹配算法列表
        :param match_rate_threshold: 整体匹配成功率
        :param crop_place: 需要裁剪的位置： {"size": (0.48, 0.95), "offset": (0.13, 0)}  # 高度为原来的0.48，宽度为原来的0.95， y轴向下移动0.13， x轴不变
        :param quick_verify:
        :param frame_save_dir:
        :param background_path:
        :param offset_size: 快速校验容差偏移量
        :param background_similar: 背景图阈值
        """
        self.crop_place = crop_place
        self.quick_verify = quick_verify
        self.frame_save_dir = frame_save_dir
        self.verify_engine_list = verify_engine_list
        self.match_rate_threshold = match_rate_threshold
        self.offset_size = offset_size
        self.background_similar = background_similar
        # 默认背景帧
        self.background_path = background_path
        self.background_img = None
        if self.background_path:
            self.background_img = cv_imread(self.background_path)
            if self.crop_place:
                self.background_img = crop_frame(self.background_img, **crop_place)
        # 排除掉背景图的帧列表
        self.origin_frame_img = []
        self.target_frame_img = []
        # 自动切割
        self.auto_crop = auto_crop
        self.col_sum_thr = col_sum_thr
        self.row_sum_thr = row_sum_thr
        if log:
            global logger
            logger = log


    def verify_video_effect(self, origin_video_path, target_video_path, img_threshold = 10):
        """
        :param origin_video_path: 源特效视频
        :param target_video_path: 目标特效视频
        :param img_threshold: 每50张图片开启一个线程
        """
        origin_video_path = os.path.abspath(origin_video_path)
        target_video_path = os.path.abspath(target_video_path)
        if self.frame_save_dir is None:
            # 帧保存地址默认为target_video_path统一级
            self.frame_save_dir = os.path.dirname(target_video_path)
        origin_video_file_name, suffix = os.path.splitext(os.path.basename(origin_video_path))
        target_video_file_name, suffix = os.path.splitext(os.path.basename(target_video_path))
        time_str = str(int(time.time()))
        origin_video_frame_path = os.path.join(self.frame_save_dir, origin_video_file_name + time_str)
        target_video_frame_path = os.path.join(self.frame_save_dir, target_video_file_name + time_str)
        start_time = time.time()
        extract_video_frame(origin_video_path, origin_video_frame_path, crop_region=self.crop_place)
        extract_video_frame(target_video_path, target_video_frame_path, crop_region=self.crop_place)
        logger.info(f"视频解帧耗时: {time.time() - start_time}")
        start_time1 = time.time()
        origin_frame_thread = MyThread(self._analyse_origin_frame, args=(), kwargs={"video_frame_path": origin_video_frame_path})
        origin_frame_thread.start()
        target_frame_thread = MyThread(self._analyse_origin_frame, args=(), kwargs={"video_frame_path": target_video_frame_path})
        target_frame_thread.start()
        origin_frame_thread.join()
        self.origin_frame_img = origin_frame_thread.get_result()
        target_frame_thread.join()
        self.target_frame_img = target_frame_thread.get_result()
        logger.info(f"源视频筛选后帧数: {len(self.origin_frame_img)}")
        logger.info(f"源视频帧: {self.origin_frame_img}")
        logger.info(f"目标视频筛选后帧数: {len(self.target_frame_img)}")
        logger.info(f"目标视频帧: {self.target_frame_img}")
        logger.info(f"梳理视频帧耗时: {time.time() - start_time1}")
        start_time2 = time.time()
        if len(self.target_frame_img) == 0 or len(self.origin_frame_img) == 0:
            logger.error(f'源视频排除背景图帧数:{len(self.origin_frame_img)}, 目标视频背景图帧数：{len(self.target_frame_img)}, 请检查特效是否生效,或者视频是否录制成功')
            return {
                'final_match_rate': 0,
                'verify_fail_screenshots':[],
                'result': False
            }
        thread_list = []
        match_times_sum = 0
        verify_fail_screenshots_all = []
        # 对照集的开始校验的图片序号
        verify_index = 0

        max_threads = 10  # 最大线程数
        if max_threads < math.ceil(len(self.target_frame_img) / img_threshold):
            # 如果超过最大线程数，调整每个线程数处理的图片数量
            img_threshold = math.ceil(len(self.target_frame_img) / max_threads)


        for i in range(0, len(self.target_frame_img), img_threshold):
            all_list_temp = self.target_frame_img[i:i + img_threshold]
            if self.quick_verify:
                # 如果是快速校验，则往前偏移指定量照片开始校验
                verify_index = verify_index - self.offset_size
                if verify_index < 0:
                    verify_index = 0
                if (verify_index + len(all_list_temp)) > len(self.origin_frame_img):
                    # 如果超过了源视频帧数，从头开始
                    verify_index = 0
            thread = MyThread(self._verify_img, args=(all_list_temp, verify_index),
                              kwargs={'verify_engine_list': self.verify_engine_list})
            thread.start()
            thread_list.append(thread)
            verify_index += img_threshold
        logger.info(f"总线程数：{len(thread_list)}")
        for t in thread_list:
            t.join()
            ret = t.get_result()
            match_times_sum += ret["match_times"]
            verify_fail_screenshots_all.extend(ret["verify_fail_screenshots"])

        # 计算匹配率 (达到相似度阈值的截图数量 / 非背景图的截图数量)
        if match_times_sum:
            final_match_rate = match_times_sum / len(self.target_frame_img)
        else:
            final_match_rate = 0
        ret = {
            'final_match_rate': final_match_rate,
            'verify_fail_screenshots': verify_fail_screenshots_all
        }
        if final_match_rate >= self.match_rate_threshold:
            ret['result'] = True
        else:
            ret['result'] = False
        logger.info(f"特效比对耗时: {time.time() - start_time2}")
        logger.info(f"总耗时: {time.time() - start_time}")
        return ret


    def _analyse_origin_frame(self, video_frame_path=""):
        all_effect_frame_save_dir_list = os.listdir(video_frame_path)
        all_effect_frame_save_dir_list.sort(key=lambda x: int(x[:-4]) if x[:-4].isdigit() else x[:-4])  # 去掉后缀名来排序
        if len(all_effect_frame_save_dir_list) == 0:
            return []
        # 默认设置第一帧为背景图
        if self.background_img is None:
            self.background_img = cv_imread(os.path.join(video_frame_path, all_effect_frame_save_dir_list[0]))

        def analyse_frame(all_list_temp, background_img, verify_engine_list):
            img_list = []
            for image_name in all_list_temp:
                img_path = os.path.join(video_frame_path, image_name)
                img = cv_imread(img_path)
                is_background, best_similar, best_engine = self._is_image_similar(img, background_img, verify_engine_list, is_background=True, skip_auto_crop=True)
                if not is_background:
                    img_list.append(img_path)
            return img_list

        img_threshold = 50
        thread_list = []
        all_img_list = []

        max_threads = 3  # 最大线程数
        if max_threads < math.ceil(len(all_effect_frame_save_dir_list) / img_threshold):
            # 如果超过最大线程数，调整每个线程数处理的图片数量
            img_threshold = math.ceil(len(all_effect_frame_save_dir_list) / max_threads)

        for i in range(0, len(all_effect_frame_save_dir_list), img_threshold):
            all_list_temp = all_effect_frame_save_dir_list[i:i + img_threshold]
            thread = MyThread(analyse_frame, args=(all_list_temp, self.background_img, self.verify_engine_list),  kwargs={})
            thread.start()
            thread_list.append(thread)
        for t in thread_list:
            t.join()
            ret = t.get_result()
            if ret:
                all_img_list.extend(ret)
        return all_img_list



    def _is_image_similar(self, image1, image2, verify_engine_list, is_background=False, skip_auto_crop=True):
        image1_crop = image1
        image2_crop = image2
        if self.auto_crop and not skip_auto_crop:
            # 自动裁剪
            image1_crop, image2_crop = get_auto_crop_image(image1, image2, col_sum_thr=self.col_sum_thr, row_sum_thr=self.row_sum_thr)
        best_similar = 0
        best_engine = ''
        for engine in verify_engine_list:
            get_similiar = switcher.get(engine[0], "")
            similar = get_similiar(image1_crop, image2_crop)
            require_similiar = engine[1]
            if is_background:
                require_similiar = self.background_similar
            if require_similiar <= similar:
                return True, similar, engine[0]
            else:
                if best_similar < similar:
                    best_similar = similar
                    best_engine = engine[0]
        return False, best_similar, best_engine

    def _verify_img(self, img_list, verify_img_index, verify_engine_list=[('ac_tpl', 0.99)]):
        """
        检验图片
        :param verify_engine_list: 校验图片算法
        :param img_list: 待校验图片集
        :param verify_img_index: 对照图片集开始顺序
        :return:
        """
        cut_match_index = -1
        match_times = 0  # 跟verify_images_dir对比，相似度超过阈值的图片数量
        verify_fail_screenshots = []
        verify_images = self.origin_frame_img[verify_img_index:len(self.origin_frame_img)]
        if verify_img_index > 0:
            verify_images.extend(self.origin_frame_img[0: verify_img_index -1 ])
        for img_path in img_list:
            img = cv_imread(img_path)
            best_matching_name = ''
            best_matching_similar = 0
            best_matching_engine = ''
            tmp_verify_images = copy.deepcopy(verify_images)
            for index, verify_img_path in enumerate(verify_images):
                # 因为截图和校验图都是连续的，所以如果有校验通过了的校验图，下次校验时可以跳过此次之前的图片
                if self.quick_verify and index <= cut_match_index:
                    continue
                verify_img = cv_imread(verify_img_path)
                is_similar, similar, engine = self._is_image_similar(img, verify_img, verify_engine_list)
                if is_similar:
                    logger.info(f"目标帧: {os.path.basename(img_path)} match 源视频帧：{os.path.basename(verify_img_path)}, similiar: {similar} , engine_type :{engine}")
                    if not self.quick_verify:
                        tmp_verify_images.pop(index)
                    cut_match_index = index
                    match_times += 1
                    best_matching_name = ""
                    break
                else:
                    if best_matching_similar < similar:
                        best_matching_similar = similar
                        best_matching_name = os.path.basename(verify_img_path)
                        best_matching_engine = engine
            if best_matching_name:
                verify_fail_screenshots.append(img_path)
                logger.info(
                    f"{os.path.basename(img_path)} 匹配不上任何帧, threshold: {verify_engine_list}, "
                    f"最佳匹配度照片: {best_matching_name}, "
                    f"相似度similiar : {best_matching_similar}, "
                    f"算法engine_type :{best_matching_engine}"
                )
        return {
           "match_times": match_times,
           "verify_fail_screenshots": verify_fail_screenshots
        }


if __name__ == '__main__':
    file_path = "quick_verify_video.py"
    origin_video_path = os.path.abspath(file_path)
    origin_video_file_name,  suffix= os.path.splitext(os.path.basename(origin_video_path))
    print(origin_video_file_name)