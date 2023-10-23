import os
import shutil
import xml.etree.ElementTree as ET
from tqdm import tqdm

type_arg = {
    "origin_file_lab": './training/image_3/',
    "target_file_lab": "./training/image_2/",
    "origin_file_img": "./training/label_3/",
    "target_file_img": "./training/label_2/",
    "data_size": 1000,
    "img_type": "jpg",
}


class OSOperate:
    
    def __init__(self, type_arg):
        self.origin_file_lab = type_arg.origin_file_lab
        self.target_file_lab = type_arg.target_file_lab
        self.origin_file_img = type_arg.origin_file_img
        self.target_file_img = type_arg.target_file_img
        self.data_size = type_arg.data_size
        self.img_type = type_arg.img_type
        self.ls_images = []

    def copy_img(self):
        ls_images = os.listdir(self.origin_file_img)
        if self.data_size < 0:
            ls_images = ls_images[self.data_size:]
        elif self.data_size > 0:
            ls_images = ls_images[:self.data_size]
        self.ls_images = ls_images
        
        shutil.rmtree(self.target_file_img)
        if not os.path.exists(self.target_file_img):
            os.mkdir(self.target_file_img)
        for img in ls_images:
            shutil.copyfile(self.origin_file_img + img, self.target_file_img + img)

    def copy_label(self):
        shutil.rmtree(self.target_file_lab)

        if not os.path.exists(self.target_file_lab):
            os.mkdir(self.target_file_lab)

        for img in self.ls_images:
            img = img.replace(self.img_type, "txt")
            shutil.copyfile(self.origin_file_lab + img, self.target_file_lab + img)

    def copy_file(self):
        self.copy_img()
        self.copy_label()

    def rename_allfile_type(self, path_file='./testing/image_2/', str_type="jpg"):
        ls_images = os.listdir(path_file)
        for img in ls_images:
            file_name = img.split(".")[0]
            os.rename(path_file + img, path_file + file_name + "." + self.img_type)


class XMLtoDeepstreamFormat:
    def __init__(self, base_xml_dir, kitti_saved_dir):
        self.base_xml_dir = base_xml_dir
        self.kitti_saved_dir = kitti_saved_dir
        
    def convert_annotation(self, file_name):
        in_file = open(self.base_xml_dir + file_name)
        tree = ET.parse(in_file)
        root = tree.getroot()

        with open(self.kitti_saved_dir + file_name[:-4] + '.txt', 'w') as f:
            for obj in root.iter('object'):
                cls = obj.find('name').text
                xmlbox = obj.find('bndbox')
                """
                    第5～8这4个数：物体的2维边界框
                    xmin，ymin，xmax，ymax
                """
                xmin, ymin, xmax, ymax = xmlbox.find('xmin').text, xmlbox.find('ymin').text, xmlbox.find('xmax').text, xmlbox.find('ymax').text
                # if cls == 'trafficsignal' or 'trafficlight':
                #     cls = 'road_sign'
                # elif cls == 'car' or 'bus':
                #     cls = 'vehicle'
                # elif cls == 'bicycle' or 'motorbike':
                #     cls = 'bicycle'
                # elif cls == 'person':
                #     cls = 'pedestrain'
                # else:
                #     pass

                f.write(cls + " " + '0.00' + " " + '0' + " " + '0.0' + " " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " " +
                        '0.0' + " " + '0.0' + " " + '0.0' + " " + '0.0' + " " + '0.0' + " " + '0.0' + " " + '0.0' + '\n')
    
    def run(self):
        xml_list = os.listdir(self.base_xml_dir)
        for i in tqdm(range(len(xml_list))):
            self.convert_annotation(xml_list[i])


if __name__ == "__main__":
    # 格式轉換
    base_xml_dir = "/workspace/tlt-experiments/data/training/label_3/"
    kitti_saved_dir = "/workspace/tlt-experiments/data/training/label_2/"
    xmltodp = XMLtoDeepstreamFormat(base_xml_dir, kitti_saved_dir)
    xmltodp.run()
    # ====================================================================
    osop = OSOperate(type_arg)
    osop.copy_file()

    osop.rename_allfile_type(path_file='./testing/image_2/', str_type="jpg")

