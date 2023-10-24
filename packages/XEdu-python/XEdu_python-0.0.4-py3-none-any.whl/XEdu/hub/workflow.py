# -*- encoding: utf-8 -*-

from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Type, Union
import cv2
import json
import numpy as np
import warnings
if TYPE_CHECKING:
    from matplotlib.backends.backend_agg import FigureCanvasAgg
import onnxruntime as ort
import time
import io
import matplotlib.pyplot as plt
import pprint
from openxlab.model import download
import os
from PIL import Image

task_dict = {
        "pose_body17":"checkpoints/body17.onnx",
        "pose_body26":"checkpoints/body26.onnx",
        "pose_wholebody133":"checkpoints/whole133.onnx",
        "pose_face106":"checkpoints/face106.onnx",
        "pose_hand21":"checkpoints/hand21.onnx",
        "det_body":"checkpoints/bodydetect.onnx",
        "det_coco":"checkpoints/cocodetect.onnx",
        "det_hand":"checkpoints/handdetect.onnx",
        "cls_imagenet":"checkpoints/imagenet1k.onnx",
        "det_face":"...",
        "ocr":"...",
        "mmedu":"...",
        "basenn":"...",
        "baseml":"...",
}
class Workflow:
    @classmethod
    def support_task(cls):
        return list(task_dict.keys())
    @classmethod
    def _task_dict(cls):
        return task_dict
    @classmethod
    def coco_class(cls):
        return coco_class

    def __init__(self, task,checkpoint=None):
        task = task.lower()
        self.task_dict = task_dict
        self.task_nick_name ={
            'body':"pose_body17",
            'body17':"pose_body17",
            'body26':"pose_body26",
            'pose_hand':"pose_hand21",
            'pose_body':"pose_body17",
            "pose_wholebody":"pose_wholebody133",
            "pose_face":"pose_face106",
        }
        if task in self.task_nick_name.keys():
            self.task = self.task_nick_name[task]
        else:
            self.task = task
        self.color_dict = {
            'red':[255,0,0],
            'orange':[255,125,0],
            'yellow':[255,255,0],
            'green':[0,255,0],
            'blue':[0,0,255],
            'purple':[255,0,255],
            'l_red':[128,0,0],
            'l_orange':[128,64,0],
            'l_yellow':[128,128,0],
            'l_green':[0,128,0],
            'l_blue':[0,0,128],
            'l_purple':[128,0,128],
        }
        if checkpoint is None and self.task in['det_body','det_coco','pose_body17','pose_body26','pose_wholebody133','pose_face106','pose_hand21','det_hand','cls_imagenet']: # 若不指定权重文件，则使用对应任务的默认模型
            checkpoint = self.task_dict[self.task]
            if not os.path.exists(checkpoint): # 下载默认模型
                print("本地未检测到{}任务对应模型，云端下载中...".format(self.task))
                path = "checkpoints"
                if not os.path.exists(path):
                    os.mkdir(path)
                model_name_map = {
                    "pose_body17":"17 body keypoints",
                    "pose_body26":"26 body keypoints",
                    "pose_wholebody133":"133 wholebody keypoints",
                    "pose_face106":"106 face keypoints",
                    "pose_hand21":"21 hand keypoints",
                    "det_body":"body detection",
                    "det_coco":"coco detection",
                    "det_hand":"hand detection",
                }
                # download('test12318/bert-english',model_name=model_name,output=path)
                download(model_repo='XEdu123/xedu.hub_onnx_model', model_name=model_name_map[self.task],output=path)
            # download()
            self.model = ort.InferenceSession(checkpoint, None)

        # model_path='rtmpose-ort/rtmpose-s-0b29a8.onnx'
        elif self.task =="det_face":
                self.model = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        elif self.task == "ocr":
                try :
                    from rapidocr_onnxruntime import RapidOCR
                except:
                    os.system("pip install rapidocr_onnxruntime")
                    from rapidocr_onnxruntime import RapidOCR
                self.model = RapidOCR()
        elif self.task.lower() == "mmedu":
            if checkpoint is None:
                print("请先指定通过MMEdu导出的onnx模型路径。")
                return
            from .BaseDeploy import _BaseDeploy as bd
            self.model = bd(checkpoint)
        elif self.task == 'baseml':
            if checkpoint is None:
                print("请先指定通过BaseML导出的pkl模型路径。")
                return
            try:
                import sklearn
                import joblib
            except:
                os.system("pip install scikit-learn")
                import joblib
            self.model = joblib.load(checkpoint)
        else:
            self.model = ort.InferenceSession(checkpoint, None)
        print("模型加载成功！")

    def inference(self,data=None,show=False,img_type=None,thr=0.3,bbox=None,target_class=None,erase=False,preprocess=None, postprocess=None):
        self._get_img = img_type
        self.erase=erase
        if self.task in ["pose_body17","pose_body26","pose_face106","pose_hand21","pose_wholebody133"]:
            return self._pose_infer(data,show,img_type,bbox)
        elif self.task in['det_body','det_coco','det_hand']:
            return self._det_infer(data,show,img_type,thr,target_class)
        elif self.task in ['det_face']:
            return self._face_det_infer(data,show,img_type)
        elif self.task in ['cls_imagenet']:
            return self._cls_infer(data,show, img_type)
        elif self.task in ['ocr']:
            return self._ocr_infer(data,show,img_type)
        elif self.task in ['mmedu']:
            return self._mmedu_infer(data,show,img_type,thr)
        elif self.task in ['basenn']:
            self.ix2word = None
            return self._basenn_infer(data,show,img_type)
        elif self.task in ['baseml']:
            return self._baseml_infer(data,show,img_type)
        elif self.task in ['custom']:
            return self._custom_infer(data, preprocess, postprocess)
    
    def _baseml_infer(self,data=None, show=None, img_type=None):
        self.baseml_res = self.model.predict(data)
        if img_type is not None:
            dummy_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'none.jpg')
            img = cv2.imread(dummy_path)
            self._get_img = img_type
            warnings.warn("BaseML task will not return an image and it is meaningless to set the parameter 'img_type'. ")
            if show:
                self.show(img)
            return self.baseml_res, img
        return self.baseml_res


    def _cls_infer(self,data=None,show=None,img_type=None):
        def preprocess(input_data):
            # convert the input data into the float32 input
            input_data =cv2.resize(input_data,(224,224))
            input_data = np.transpose(input_data,(2,0,1))
            img_data = input_data.astype('float32')
            mean_vec = np.array([123.675,116.28,103.53])/255
            stddev_vec = np.array([58.395,57.12,57.375])/255
            norm_img_data = np.zeros(img_data.shape).astype('float32')
            for i in range(img_data.shape[0]):
                norm_img_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]
            norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')
            return norm_img_data
        
        if isinstance(data, str):
            image = cv2.imread(data) 
            data = preprocess(image)
        elif isinstance(data, np.ndarray):
            if len(data.shape) == 2: # grayscale
                data = cv2.cvtColor(data, cv2.COLOR_GRAY2BGR) 
            image = data
            data = preprocess(data)

        ort_inputs = {'input': data}
        self.class_res = self.model.run(['output'], ort_inputs)[0]
        if img_type:
            # 绘制查看效果
            if img_type =='pil':
                # image = cv2.cvtcolor(image,cv2.BGR2RGB)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            if show:
                self.show(image)
            return self.class_res, image
        return self.class_res 

    def _custom_infer(self,data,preprocess=None, postprocess=None): 
        if preprocess is not None:
            data = preprocess(data)
        ort_inputs = {'input': data}
        self.custom_res = self.model.run(['output'], ort_inputs)
        # print(self.custom_res[0].shape)
        if postprocess is not None:
            self.custom_res = postprocess(self.custom_res,data)
        return self.custom_res 

    def _basenn_infer(self,data=None,show=True, img_type=None):
        ort_session = self.model
        metamap = ort_session.get_modelmeta().custom_metadata_map
        input_size = eval(metamap['input_size'])
        dataset_type = metamap['dataset_type']
        if dataset_type == 'img':
            if isinstance(data,str): # 文件路径
                data = cv2.imread(data)# .transpose(2,0,1)
                if input_size[1] == 1: # 灰度
                    data = cv2.cvtColor(data,cv2.COLOR_BGR2GRAY)
                    data = cv2.resize(data, tuple(input_size[2:]))
                    data = np.expand_dims(data,2) # 增加channel维
                else:
                    data = cv2.resize(data,input_size[2:]) 

                data = np.expand_dims(data,0) # 增加batch维
                data = data.transpose(0,3,1,2) # （batch,channel,w,h）
            data  = data.astype(np.float32) # tab iris
            ort_inputs = {'input': data}
            # res = ort_session.run(['output'], ort_inputs)
        elif dataset_type == 'tab':
            data  = data.astype(np.float32) # tab iris
            ort_inputs = {'input': data}
            # res = ort_session.run(['output'], ort_inputs)
        elif dataset_type == 'npz':
            if isinstance(data, str): # 
                if os.path.splitext(data)[1] == '.npz': # action npz
                    data = np.load(data, allow_pickle=True)['data']
                    data  = data.astype(np.float32) # tab iris
                else: # tang zi
                    word2idx = eval(metamap['word2idx'])
                    self.ix2word = {v:k for k, v in word2idx.items()}

                    data = [[word2idx[i] for i in data]]
                    
            # data  = data.astype(np.float32) # tab iris
        ort_inputs = {'input': data}
        self.basenn_res = ort_session.run(['output'], ort_inputs)
            # 索引映射回词表
            # idx = res[0].argmax()
            # print(ix2word[idx])
        if img_type is not None:
            dummy_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'none.jpg')
            img = cv2.imread(dummy_path)
            self._get_img = img_type
            warnings.warn("BaseNN task will not return an image and it is meaningless to set the parameter 'img_type'. ")
            if show:
                self.show(img)
            return self.basenn_res, img
        return self.basenn_res

    def _mmedu_infer(self,data=None,show=False,img_type=None,thr=None):
        if img_type is None:
            self.result = self.model.inference(data, show=show,get_img=img_type)
            return self.result
        else:
            self.result,img = self.model.inference(data,get_img=img_type,score=thr)
            if show ==True:
                self.show(img)
            return self.result,img

    def _ocr_infer(self,data=None,show=False,img_type=None):

        result, elapse_list = self.model(data)
        if result is None:
            return []
        self.bboxs, self.classes,    self.scores = list(zip(*result))
        result = list(zip(self.classes,self.bboxs))
        if img_type:
            from rapidocr_onnxruntime import VisRes
            path = "font"
            font_file = os.path.join(path,"FZYTK.TTF")
            if not os.path.exists(font_file): # 下载默认模型
                if not os.path.exists(path):
                    os.mkdir(path)
                download(model_repo='XEdu123/xedu.hub_onnx_model', model_name='ocr font',output=path)
            vis = VisRes(font_path=font_file)
            res_img = vis(data, self.bboxs,  self.classes, self.scores)
            if img_type == 'cv2':
                res_img = res_img
            elif img_type =='pil':
                res_img = cv2.cvtColor(res_img ,cv2.COLOR_BGR2RGB)
            if show:
                self.show(res_img)
            return result,res_img

        return result

    def _face_det_infer(self,data=None,show=False,get_img=None):

        if isinstance(data,str):
            image = cv2.imread(data)
        else:
            image = data
        ### 推理
        face_model = self.model
        faces = face_model.detectMultiScale(image,scaleFactor=1.2,minNeighbors=5) # opencv返回的是（x,y,w,h）
        self.bboxs = [] # 转换为（x1,y1,x2,y2）
        for bbox in faces:
            ex_bbox = [bbox[0],bbox[1],(bbox[0]+bbox[2]),(bbox[1]+bbox[3])] 
            self.bboxs.append(ex_bbox)
        self.scores = []
        self.classes = ["face" for i in range(len(self.bboxs))]

        if get_img:
            if get_img =='cv2':
                for [a,b,c,d] in self.bboxs:
                    cv2.rectangle(image, (int(a),int(b)),(int(c),int(d)),(0,0,255),2)
            elif get_img =='pil':
                # image = cv2.cvtcolor(image,cv2.BGR2RGB)
                for [a,b,c,d] in self.bboxs:
                    cv2.rectangle(image, (int(a),int(b)),(int(c),int(d)),(0,0,255),2)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            if show:
                self.show(image)
            return np.array(self.bboxs),image
        return np.array(self.bboxs)
    
    def _det_infer(self,data=None,show=False,get_img=None,threshold=0.5,target_class=None):
        def preprocess(input_data):
            # convert the input data into the float32 input
            img_data = input_data.astype('float32')

            #normalize
            mean_vec = np.array([0.485, 0.456, 0.406])
            stddev_vec = np.array([0.229, 0.224, 0.225])
            norm_img_data = np.zeros(img_data.shape).astype('float32')
            for i in range(img_data.shape[0]):
                norm_img_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]

            #add batch channel
            norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')
            return norm_img_data

        ### 读取模型
        model = self.model
        # session = ort.InferenceSession('rtmdet-acc0de.onnx', None)
        #注 实际根据不同的推理需求例如 TensorRT,CUDA,等需要更多设置，具体参考官网

        ### 准备数据
        # img_path = 'pose2.jpg'
        if isinstance(data,str):
            # image = plt.imread(data)
            # image = Image.open(data)
            image = cv2.imread(data)
        else:
            image = data
            # image = Image.fromarray(data)
        # image = Image.open(img_path).resize((224,224))  # 这里设置的动态数据尺寸，不需要resize
        re_image =cv2.resize(image,(224,224))
        re_image_data = np.array(re_image).transpose(2, 0, 1)
        input_data = preprocess(re_image_data)

        ### 推理
        raw_result = model.run([], {'input': input_data})
        # print(raw_result[1])
        ### 后处理
        h_ratio =  image.shape[0] /224
        w_ratio =  image.shape[1] /224 
        self.bboxs = []
        self.scores = []
        self.classes = []
        for (idx,[a,b,c,d,e]) in enumerate(raw_result[0][0]):#,raw_result[1][0]:
            if target_class is not None:
                if isinstance(target_class,str):    
                    if coco_class[raw_result[1][0][idx]+1] != target_class:
                        continue
                elif isinstance(target_class,List):
                    if coco_class[raw_result[1][0][idx]+1] not in  target_class:
                        continue
            if e> threshold:                    
                bbox = [a*w_ratio,b*h_ratio,c*w_ratio,d*h_ratio]
                self.bboxs.append(bbox)
                self.scores.append(e)
                self.classes.append(coco_class[raw_result[1][0][idx]+1])
        if get_img:
            if get_img =='cv2':
                for i,[a,b,c,d] in enumerate(self.bboxs):
                    if self.task == 'det_coco':
                        cv2.putText(image, str(self.classes[i]), (int(a),int(b)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2)
                    cv2.rectangle(image, (int(a),int(b)),(int(c),int(d)),(0,0,255),2)
            elif get_img =='pil':
                # image = cv2.cvtcolor(image,cv2.BGR2RGB)
                for [a,b,c,d] in self.bboxs:
                    cv2.rectangle(image, (int(a),int(b)),(int(c),int(d)),(0,0,255),2)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            if show:
                self.show(image)
            return np.array(self.bboxs),image
        return np.array(self.bboxs)
        
    def _pose_infer(self,data=None,show=False,get_img=None,bbox=None):
        model = self.model
        self.bbox=bbox
        h, w = model.get_inputs()[0].shape[2:]
        model_input_size = (w, h)
        if isinstance(data,str):
            img = cv2.imread(data)
        else:
            img = data
        # 前处理
        # start_time = time.time()
        self.data = data
        resized_img, center, scale = mmpose_preprocess(img, model_input_size,bbox)
        input_tensor = [resized_img.transpose(2, 0, 1)]
        input_name = model.get_inputs()[0].name
        output_names = [o.name for o in model.get_outputs()]
        # end_time = time.time()
        # print('前处理耗时：',end_time-start_time)
        # 模型推理
        # start_time = time.time()
        outputs = model.run(output_names, {input_name: input_tensor})
        # end_time = time.time()
        # print('推理耗时：',end_time-start_time)
        # 后处理
        # start_time = time.time()
        self.keypoints, self.scores = mmpose_postprocess(outputs, model_input_size, center, scale)
        # end_time = time.time()
        # print('后处理耗时：',end_time-start_time)
        # print('推理结果：')
        # print(keypoints)
        if get_img:
            # 绘制查看效果
            re = self._get_image()
            if show:
                self.show(re)
            return self.keypoints[0], re
        return self.keypoints[0]
    
    def _get_image(self):
        sketch = {}
        if self.task == 'pose_hand21':
            sketch = {
                'red':[[0,1],[1,2],[2,3],[3,4]],
                'orange':[[0,5],[5,6],[6,7],[7,8]],
                'yellow':[[0,9],[9,10],[10,11],[11,12]],
                'green':[[0,13],[13,14],[14,15],[15,16]],
                'blue':[[0,17],[17,18],[18,19],[19,20]]
            }
        elif self.task =='pose_body26':
            sketch = {
                'red':[[0,1],[1,2],[2,0],[2,4],[1,3],[0,17],[0,18]],
                'orange':[[18,6],[8,6],[10,8]],
                'yellow':[[18,19],[19,12],[19,11]],
                'green':[[12,14],[14,16],[16,23],[21,16],[25,16]],
                'blue':[[11,13],[13,15],[15,20],[15,22],[15,24]],
                'purple':[[18,5],[5,7],[7,9]],
            }
        elif self.task =='pose_body17':
            sketch = {
                'red':[[0,1],[1,2],[2,0],[2,4],[1,3],[4,6],[3,5]],
                'orange':[[10,8],[8,6]],
                'yellow':[[5,6],[6,12],[12,11],[11,5]],
                'green':[[12,14],[14,16]],
                'blue':[[11,13],[13,15]],
                'purple':[[5,7],[9,7]],
            }
        elif self.task=='pose_wholebody133':
            sketch = {
                # body
                'red':[[0,1],[1,2],[2,0],[2,4],[1,3],[4,6],[3,5]],
                'orange':[[10,8],[8,6]],
                'yellow':[[5,6],[6,12],[12,11],[11,5]],
                'green':[[12,14],[14,16]],
                'blue':[[11,13],[13,15]],
                'purple':[[5,7],[9,7]],
            }

        if isinstance(self.data,str):
            img = cv2.imread((self.data))
        else:
            img = self.data
        # h,w,c = img.shape
        
        for j in range(self.keypoints.shape[0]):
            for i in range(self.keypoints.shape[1]):
                # plt.scatter(self.keypoints[j][i][0],self.keypoints[j][i][1],c='b',s=10)
                x1,y1 = self.keypoints[j][i]
                if self.bbox is not None and self.erase:
                    sx1,sy1,sx2,sy2 = self.bbox # 
                    if sx1<x1<sx2 and sy1<y1<sy2 :
                        cv2.circle(img,(int(self.keypoints[j][i][0]),int(self.keypoints[j][i][1])),radius=1,color=[0,255,0])
                else:
                    cv2.circle(img,(int(self.keypoints[j][i][0]),int(self.keypoints[j][i][1])),radius=1,color=[0,255,0])

        for color in sketch.keys():
            # print(color,sketch[color])
            for [fx,fy] in sketch[color]:
                # plt.plot([self.keypoints[0][fx][0],self.keypoints[0][fy][0]],[self.keypoints[0][fx][1],self.keypoints[0][fy][1]],color=color)
                cv2.line(img, (int(self.keypoints[0][fx][0]),int(self.keypoints[0][fx][1])),(int(self.keypoints[0][fy][0]),int(self.keypoints[0][fy][1])),color=self.color_dict[color])

        if self._get_img == 'cv2':
            return img
        elif self._get_img.lower() == 'pil':
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def show(self,img): # check
        try:
            if self._get_img.lower() == 'cv2':
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            elif self._get_img.lower() == 'pil':
                img = img
            plt.imshow(img)
            plt.show()
        except:
            print("Error: please inference before show.")
            pass
    
    def save(self,img,save_path): # check
        if self._get_img == 'cv2':
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(save_path,img)
        elif self._get_img.lower() == 'pil':
            img = img
            a = Image.fromarray(img)
            a.save(save_path)
            # plt.imshow(img)
            # plt.axis('off')
            # plt.subplots_adjust(top=1,bottom=0,right=1,left=0,hspace=0,wspace=0)
            # plt.margins(0,0)
            # plt.savefig(save_path)
    
    def format_output(self,lang='zh'): # check
        language = lang
        if self.task in ["pose_body17","pose_body26","pose_face106","pose_hand21","pose_wholebody133"]:
            formalize_keys = {
                "zh":["关键点坐标","分数"],
                "en":["keypoints","scores"],
                "ru":["ключевые точки","баллы"],
                "de":["Schlüsselpunkte","Partituren"],
                "fr":["points clés","partitions"]
            }
            formalize_result = {
                formalize_keys[language][0]:self.keypoints[0].tolist(),
                formalize_keys[language][1]:self.scores[0].tolist(),
            }
            # formalize_result = json.dumps(formalize_result, indent=4,sort_keys=False)
            pprint.pprint(formalize_result,sort_dicts=False)
        elif self.task in['det_body','det_coco','det_hand']:
            formalize_keys = {
                "zh":["检测框","分数","类别"],
                "en":['bounding boxes',"scores","class"],
                "ru":["ограничивающие рамки","баллы","занятия"],
                "de":["Begrenzungsrahmen","Partituren","Klassen"],
                "fr":["cadres de délimitation","partitions","Des classes"]
            }
            if self.task == 'cocodetect' and self.classes is not None:
                formalize_result = {
                    formalize_keys[language][0]:self.bboxs,
                    formalize_keys[language][1]:self.scores,
                    formalize_keys[language][2]:self.classes,
                }
            else:
                formalize_result = {
                    formalize_keys[language][0]:self.bboxs,
                    formalize_keys[language][1]:self.scores,
                }
            pprint.pprint(formalize_result,sort_dicts=False)
        elif self.task in['det_face']:
            formalize_keys = {
                "zh":["检测框","分数","类别"],
                "en":['bounding boxes',"scores","class"],
                "ru":["ограничивающие рамки","баллы","занятия"],
                "de":["Begrenzungsrahmen","Partituren","Klassen"],
                "fr":["cadres de délimitation","partitions","Des classes"]
            }
            if self.classes is not None:
                formalize_result = {
                    formalize_keys[language][0]:self.bboxs,
                    formalize_keys[language][2]:self.classes,
                }
            else:
                formalize_result = {
                    formalize_keys[language][0]:self.bboxs,
                }
            pprint.pprint(formalize_result,sort_dicts=False)
        elif self.task in ['ocr']:
            formalize_keys = {
                "zh":["检测框","分数","文本"],
                "en":['bounding boxes',"scores","text"],
                "ru":["ограничивающие рамки","баллы","текст"],
                "de":["Begrenzungsrahmen","Partituren","Text"],
                "fr":["cadres de délimitation","partitions","texte"]
            }
            formalize_result = {
                formalize_keys[language][0]:list(self.bboxs),
                formalize_keys[language][1]:list(self.scores),
                formalize_keys[language][2]:list(self.classes),
            }
            pprint.pprint(formalize_result,sort_dicts=False)
        elif self.task in ['mmedu']:
            formalize_result = self.model.print_result(self.result)
            pprint.pprint(formalize_result,sort_dicts=False)
        elif self.task in ['basenn']:
            formalize_keys = {
                "zh":["预测值","分数"],
                "en":["prediction","scores"],
                "ru":["прогноз","баллы"],
                "de":["Vorhersage","Partituren"],
                "fr":["prédiction","partitions"]
            }
            res_idx = self.basenn_res[0].argmax(axis=1)
            formalize_result = {}
            for i,idx in enumerate(res_idx):
                try:
                    pred = self.ix2word[idx]
                except:
                    pred = idx
                formalize_result[i] ={formalize_keys[lang][0]:pred,formalize_keys[lang][1]:self.basenn_res[0][i][idx]} 
            pprint.pprint(formalize_result,sort_dicts=False)
        elif self.task in ['baseml']:
            formalize_keys = {
                "zh":["预测结果","分数"],
                "en":["prediction","scores"],
                "ru":["прогноз","баллы"],
                "de":["Vorhersage","Partituren"],
                "fr":["prédiction","partitions"]
            }
            formalize_result = {
                formalize_keys[lang][0]:self.baseml_res
            }
            pprint.pprint(formalize_result,sort_dicts=False)

        elif self.task in ['cls_imagenet']:
            formalize_keys = {
                "zh":["预测值","分数","预测类别"],
                "en":["prediction","scores","category"],
                "ru":["прогноз","баллы","Kategorie"],
                "de":["Vorhersage","Partituren","Kategorie"],
                "fr":["prédiction","partitions","catégorie"]
            }
            res_idx = np.argmax(self.class_res)
            formalize_result = {
                formalize_keys[language][0]:res_idx,
                formalize_keys[language][1]:self.class_res[0][res_idx],
                formalize_keys[language][2]:imagenet_class[res_idx],
            }
            pprint.pprint(formalize_result,sort_dicts=False)
        return formalize_result


def bbox_xyxy2cs(bbox: np.ndarray,
                 padding: float = 1.) -> Tuple[np.ndarray, np.ndarray]:
    """Transform the bbox format from (x,y,w,h) into (center, scale)

    Args:
        bbox (ndarray): Bounding box(es) in shape (4,) or (n, 4), formatted
            as (left, top, right, bottom)
        padding (float): BBox padding factor that will be multilied to scale.
            Default: 1.0

    Returns:
        tuple: A tuple containing center and scale.
        - np.ndarray[float32]: Center (x, y) of the bbox in shape (2,) or
            (n, 2)
        - np.ndarray[float32]: Scale (w, h) of the bbox in shape (2,) or
            (n, 2)
    """
    # convert single bbox from (4, ) to (1, 4)
    dim = bbox.ndim
    if dim == 1:
        bbox = bbox[None, :]

    # get bbox center and scale
    x1, y1, x2, y2 = np.hsplit(bbox, [1, 2, 3])
    center = np.hstack([x1 + x2, y1 + y2]) * 0.5
    scale = np.hstack([x2 - x1, y2 - y1]) * padding

    if dim == 1:
        center = center[0]
        scale = scale[0]

    return center, scale

def value2list(value: Any, valid_type: Union[Type, Tuple[Type, ...]],
               expand_dim: int) -> List[Any]:
    """If the type of ``value`` is ``valid_type``, convert the value to list
    and expand to ``expand_dim``.

    Args:
        value (Any): value.
        valid_type (Union[Type, Tuple[Type, ...]): valid type.
        expand_dim (int): expand dim.

    Returns:
        List[Any]: value.
    """
    if isinstance(value, valid_type):
        value = [value] * expand_dim
    return value


def check_type(name: str, value: Any,
               valid_type: Union[Type, Tuple[Type, ...]]) -> None:
    """Check whether the type of value is in ``valid_type``.

    Args:
        name (str): value name.
        value (Any): value.
        valid_type (Type, Tuple[Type, ...]): expected type.
    """
    if not isinstance(value, valid_type):
        raise TypeError(f'`{name}` should be {valid_type} '
                        f' but got {type(value)}')


def check_length(name: str, value: Any, valid_length: int) -> None:
    """If type of the ``value`` is list, check whether its length is equal with
    or greater than ``valid_length``.

    Args:
        name (str): value name.
        value (Any): value.
        valid_length (int): expected length.
    """
    if isinstance(value, list):
        if len(value) < valid_length:
            raise AssertionError(
                f'The length of {name} must equal with or '
                f'greater than {valid_length}, but got {len(value)}')


def check_type_and_length(name: str, value: Any,
                          valid_type: Union[Type, Tuple[Type, ...]],
                          valid_length: int) -> None:
    """Check whether the type of value is in ``valid_type``. If type of the
    ``value`` is list, check whether its length is equal with or greater than
    ``valid_length``.

    Args:
        value (Any): value.
        legal_type (Type, Tuple[Type, ...]): legal type.
        valid_length (int): expected length.

    Returns:
        List[Any]: value.
    """
    check_type(name, value, valid_type)
    check_length(name, value, valid_length)


def color_val_matplotlib(
    colors: Union[str, tuple, List[Union[str, tuple]]]
) -> Union[str, tuple, List[Union[str, tuple]]]:
    """Convert various input in RGB order to normalized RGB matplotlib color
    tuples,
    Args:
        colors (Union[str, tuple, List[Union[str, tuple]]]): Color inputs
    Returns:
        Union[str, tuple, List[Union[str, tuple]]]: A tuple of 3 normalized
        floats indicating RGB channels.
    """
    if isinstance(colors, str):
        return colors
    elif isinstance(colors, tuple):
        assert len(colors) == 3
        for channel in colors:
            assert 0 <= channel <= 255
        colors = [channel / 255 for channel in colors]
        return tuple(colors)
    elif isinstance(colors, list):
        colors = [
            color_val_matplotlib(color)  # type:ignore
            for color in colors
        ]
        return colors
    else:
        raise TypeError(f'Invalid type for color: {type(colors)}')


def color_str2rgb(color: str) -> tuple:
    """Convert Matplotlib str color to an RGB color which range is 0 to 255,
    silently dropping the alpha channel.

    Args:
        color (str): Matplotlib color.

    Returns:
        tuple: RGB color.
    """
    import matplotlib
    rgb_color: tuple = matplotlib.colors.to_rgb(color)
    rgb_color = tuple(int(c * 255) for c in rgb_color)
    return rgb_color


def convert_overlay_heatmap(feat_map: np.ndarray,
                            img: Optional[np.ndarray] = None,
                            alpha: float = 0.5) -> np.ndarray:
    """Convert feat_map to heatmap and overlay on image, if image is not None.

    Args:
        feat_map (np.ndarray): The feat_map to convert
            with of shape (H, W), where H is the image height and W is
            the image width.
        img (np.ndarray, optional): The origin image. The format
            should be RGB. Defaults to None.
        alpha (float): The transparency of featmap. Defaults to 0.5.

    Returns:
        np.ndarray: heatmap
    """
    assert feat_map.ndim == 2 or (feat_map.ndim == 3
                                  and feat_map.shape[0] in [1, 3])
    if feat_map.ndim == 3:
        feat_map = feat_map.transpose(1, 2, 0)

    norm_img = np.zeros(feat_map.shape)
    norm_img = cv2.normalize(feat_map, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    heat_img = cv2.applyColorMap(norm_img, cv2.COLORMAP_JET)
    heat_img = cv2.cvtColor(heat_img, cv2.COLOR_BGR2RGB)
    if img is not None:
        heat_img = cv2.addWeighted(img, 1 - alpha, heat_img, alpha, 0)
    return heat_img

def wait_continue(figure, timeout: float = 0, continue_key: str = ' ') -> int:
    """Show the image and wait for the user's input.

    This implementation refers to
    https://github.com/matplotlib/matplotlib/blob/v3.5.x/lib/matplotlib/_blocking_input.py

    Args:
        timeout (float): If positive, continue after ``timeout`` seconds.
            Defaults to 0.
        continue_key (str): The key for users to continue. Defaults to
            the space key.

    Returns:
        int: If zero, means time out or the user pressed ``continue_key``,
            and if one, means the user closed the show figure.
    """  # noqa: E501
    import matplotlib.pyplot as plt
    from matplotlib.backend_bases import CloseEvent
    is_inline = 'inline' in plt.get_backend()
    if is_inline:
        # If use inline backend, interactive input and timeout is no use.
        return 0

    if figure.canvas.manager:  # type: ignore
        # Ensure that the figure is shown
        figure.show()  # type: ignore

    while True:

        # Connect the events to the handler function call.
        event = None

        def handler(ev):
            # Set external event variable
            nonlocal event
            # Qt backend may fire two events at the same time,
            # use a condition to avoid missing close event.
            event = ev if not isinstance(event, CloseEvent) else event
            figure.canvas.stop_event_loop()

        cids = [
            figure.canvas.mpl_connect(name, handler)  # type: ignore
            for name in ('key_press_event', 'close_event')
        ]

        try:
            figure.canvas.start_event_loop(timeout)  # type: ignore
        finally:  # Run even on exception like ctrl-c.
            # Disconnect the callbacks.
            for cid in cids:
                figure.canvas.mpl_disconnect(cid)  # type: ignore

        if isinstance(event, CloseEvent):
            return 1  # Quit for close.
        elif event is None or event.key == continue_key:
            return 0  # Quit for continue.

def img_from_canvas(canvas: 'FigureCanvasAgg') -> np.ndarray:
    """Get RGB image from ``FigureCanvasAgg``.

    Args:
        canvas (FigureCanvasAgg): The canvas to get image.

    Returns:
        np.ndarray: the output of image in RGB.
    """
    s, (width, height) = canvas.print_to_buffer()
    buffer = np.frombuffer(s, dtype='uint8')
    img_rgba = buffer.reshape(height, width, 4)
    rgb, alpha = np.split(img_rgba, [3], axis=2)
    return rgb.astype('uint8')

def _fix_aspect_ratio(bbox_scale: np.ndarray,
                      aspect_ratio: float) -> np.ndarray:
    """Extend the scale to match the given aspect ratio.

    Args:
        scale (np.ndarray): The image scale (w, h) in shape (2, )
        aspect_ratio (float): The ratio of ``w/h``

    Returns:
        np.ndarray: The reshaped image scale in (2, )
    """
    w, h = np.hsplit(bbox_scale, [1])
    bbox_scale = np.where(w > h * aspect_ratio,
                          np.hstack([w, w / aspect_ratio]),
                          np.hstack([h * aspect_ratio, h]))
    return bbox_scale

def _rotate_point(pt: np.ndarray, angle_rad: float) -> np.ndarray:
    """Rotate a point by an angle.

    Args:
        pt (np.ndarray): 2D point coordinates (x, y) in shape (2, )
        angle_rad (float): rotation angle in radian

    Returns:
        np.ndarray: Rotated point in shape (2, )
    """
    sn, cs = np.sin(angle_rad), np.cos(angle_rad)
    rot_mat = np.array([[cs, -sn], [sn, cs]])
    return rot_mat @ pt

def _get_3rd_point(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """To calculate the affine matrix, three pairs of points are required. This
    function is used to get the 3rd point, given 2D points a & b.

    The 3rd point is defined by rotating vector `a - b` by 90 degrees
    anticlockwise, using b as the rotation center.

    Args:
        a (np.ndarray): The 1st point (x,y) in shape (2, )
        b (np.ndarray): The 2nd point (x,y) in shape (2, )

    Returns:
        np.ndarray: The 3rd point.
    """
    direction = a - b
    c = b + np.r_[-direction[1], direction[0]]
    return c

def get_warp_matrix(center: np.ndarray,
                    scale: np.ndarray,
                    rot: float,
                    output_size: Tuple[int, int],
                    shift: Tuple[float, float] = (0., 0.),
                    inv: bool = False) -> np.ndarray:
    """Calculate the affine transformation matrix that can warp the bbox area
    in the input image to the output size.

    Args:
        center (np.ndarray[2, ]): Center of the bounding box (x, y).
        scale (np.ndarray[2, ]): Scale of the bounding box
            wrt [width, height].
        rot (float): Rotation angle (degree).
        output_size (np.ndarray[2, ] | list(2,)): Size of the
            destination heatmaps.
        shift (0-100%): Shift translation ratio wrt the width/height.
            Default (0., 0.).
        inv (bool): Option to inverse the affine transform direction.
            (inv=False: src->dst or inv=True: dst->src)

    Returns:
        np.ndarray: A 2x3 transformation matrix
    """
    shift = np.array(shift)
    src_w = scale[0]
    dst_w = output_size[0]
    dst_h = output_size[1]

    # compute transformation matrix
    rot_rad = np.deg2rad(rot)
    src_dir = _rotate_point(np.array([0., src_w * -0.5]), rot_rad)
    dst_dir = np.array([0., dst_w * -0.5])

    # get four corners of the src rectangle in the original image
    src = np.zeros((3, 2), dtype=np.float32)
    src[0, :] = center + scale * shift
    src[1, :] = center + src_dir + scale * shift
    src[2, :] = _get_3rd_point(src[0, :], src[1, :])

    # get four corners of the dst rectangle in the input image
    dst = np.zeros((3, 2), dtype=np.float32)
    dst[0, :] = [dst_w * 0.5, dst_h * 0.5]
    dst[1, :] = np.array([dst_w * 0.5, dst_h * 0.5]) + dst_dir
    dst[2, :] = _get_3rd_point(dst[0, :], dst[1, :])

    if inv:
        warp_mat = cv2.getAffineTransform(np.float32(dst), np.float32(src))
    else:
        warp_mat = cv2.getAffineTransform(np.float32(src), np.float32(dst))

    return warp_mat

def top_down_affine(input_size: dict, bbox_scale: dict, bbox_center: dict,
                    img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Get the bbox image as the model input by affine transform.

    Args:
        input_size (dict): The input size of the model.
        bbox_scale (dict): The bbox scale of the img.
        bbox_center (dict): The bbox center of the img.
        img (np.ndarray): The original image.

    Returns:
        tuple: A tuple containing center and scale.
        - np.ndarray[float32]: img after affine transform.
        - np.ndarray[float32]: bbox scale after affine transform.
    """
    w, h = input_size
    warp_size = (int(w), int(h))

    # reshape bbox to fixed aspect ratio
    bbox_scale = _fix_aspect_ratio(bbox_scale, aspect_ratio=w / h)

    # get the affine matrix
    center = bbox_center
    scale = bbox_scale
    rot = 0
    warp_mat = get_warp_matrix(center, scale, rot, output_size=(w, h))

    # do affine transform
    img = cv2.warpAffine(img, warp_mat, warp_size, flags=cv2.INTER_LINEAR)

    return img, bbox_scale

def mmpose_preprocess(
    img: np.ndarray, input_size: Tuple[int, int] = (192, 256),bbox=None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Do preprocessing for RTMPose model inference.

    Args:
        img (np.ndarray): Input image in shape.
        input_size (tuple): Input image size in shape (w, h).

    Returns:
        tuple:
        - resized_img (np.ndarray): Preprocessed image.
        - center (np.ndarray): Center of image.
        - scale (np.ndarray): Scale of image.
    """
    # get shape of image
    img_shape = img.shape[:2]
    if bbox is None:
        bbox = np.array([0, 0, img_shape[1], img_shape[0]])

    # get center and scale
    center, scale = bbox_xyxy2cs(bbox, padding=1.25)

    # do affine transformation
    resized_img, scale = top_down_affine(input_size, scale, center, img)

    # normalize image
    mean = np.array([123.675, 116.28, 103.53])
    std = np.array([58.395, 57.12, 57.375])
    resized_img = (resized_img - mean) / std

    return resized_img, center, scale

def get_simcc_maximum(simcc_x: np.ndarray,
                      simcc_y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Get maximum response location and value from simcc representations.

    Note:
        instance number: N
        num_keypoints: K
        heatmap height: H
        heatmap width: W

    Args:
        simcc_x (np.ndarray): x-axis SimCC in shape (K, Wx) or (N, K, Wx)
        simcc_y (np.ndarray): y-axis SimCC in shape (K, Wy) or (N, K, Wy)

    Returns:
        tuple:
        - locs (np.ndarray): locations of maximum heatmap responses in shape
            (K, 2) or (N, K, 2)
        - vals (np.ndarray): values of maximum heatmap responses in shape
            (K,) or (N, K)
    """
    N, K, Wx = simcc_x.shape
    simcc_x = simcc_x.reshape(N * K, -1)
    simcc_y = simcc_y.reshape(N * K, -1)

    # get maximum value locations
    x_locs = np.argmax(simcc_x, axis=1)
    y_locs = np.argmax(simcc_y, axis=1)
    locs = np.stack((x_locs, y_locs), axis=-1).astype(np.float32)
    max_val_x = np.amax(simcc_x, axis=1)
    max_val_y = np.amax(simcc_y, axis=1)

    # get maximum value across x and y axis
    mask = max_val_x > max_val_y
    max_val_x[mask] = max_val_y[mask]
    vals = max_val_x
    locs[vals <= 0.] = -1

    # reshape
    locs = locs.reshape(N, K, 2)
    vals = vals.reshape(N, K)

    return locs, vals

def mmpose_decode(simcc_x: np.ndarray, simcc_y: np.ndarray,
           simcc_split_ratio) -> Tuple[np.ndarray, np.ndarray]:
    """Modulate simcc distribution with Gaussian.

    Args:
        simcc_x (np.ndarray[K, Wx]): model predicted simcc in x.
        simcc_y (np.ndarray[K, Wy]): model predicted simcc in y.
        simcc_split_ratio (int): The split ratio of simcc.

    Returns:
        tuple: A tuple containing center and scale.
        - np.ndarray[float32]: keypoints in shape (K, 2) or (n, K, 2)
        - np.ndarray[float32]: scores in shape (K,) or (n, K)
    """
    keypoints, scores = get_simcc_maximum(simcc_x, simcc_y)
    keypoints /= simcc_split_ratio

    return keypoints, scores

def mmpose_postprocess(outputs: List[np.ndarray],
                model_input_size: Tuple[int, int],
                center: Tuple[int, int],
                scale: Tuple[int, int],
                simcc_split_ratio: float = 2.0
                ) -> Tuple[np.ndarray, np.ndarray]:
    """Postprocess for RTMPose model output.

    Args:
        outputs (np.ndarray): Output of RTMPose model.
        model_input_size (tuple): RTMPose model Input image size.
        center (tuple): Center of bbox in shape (x, y).
        scale (tuple): Scale of bbox in shape (w, h).
        simcc_split_ratio (float): Split ratio of simcc.

    Returns:
        tuple:
        - keypoints (np.ndarray): Rescaled keypoints.
        - scores (np.ndarray): Model predict scores.
    """
    # use simcc to decode
    simcc_x, simcc_y = outputs
    keypoints, scores = mmpose_decode(simcc_x, simcc_y, simcc_split_ratio)

    # rescale keypoints
    keypoints = keypoints / model_input_size * scale + center - scale / 2

    return keypoints, scores

coco_class  ={
    1: "person",
    2: "bicycle",
    3:"car",
    4:"motorbike",
    5:"aeroplane",
    6:"bus",
    7:"train",
    8:"truck",
    9:"boat",
    10:"traffic light",
    11:"fire hydrant",
    12:"stop sign",
    13:"parking meter",
    14:"bench",
    15:"bird",
    16:"cat",
    17:"dog",
    18:"horse",
    19:"sheep",
    20:"cow",
    21:"elephant",
    22:"bear",
    23:"zebra",
    24:"giraffe",
    25:"backpack",
    26:"umbrella",
    27:"handbag",
    28:"tie",
    29:"suitcase",
    30:"frisbee",
    31:"skis",
    32:"snowboard",
    33:"sports ball",
    34:"kite",
    35:"baseball bat",
    36:"baseball glove",
    37:"skateboard",
    38:"surfboard",
    39:"tennis racket",
    40:"bottle",
    41:"wine glass",
    42:"cup",
    43:"fork",
    44:"knife",
    45:"spoon",
    46:"bowl",
    47:"banana",
    48:"apple",
    49:"sandwich",
    50:"orange",
    51:"broccoli",
    52:"carrot",
    53:"hot dog",
    54:"pizza",
    55:"donut",
    56:"cake",
    57:"chair",
    58:"sofa",
    59:"pottedplant",
    60:"bed",
    61:"diningtable",
    62:"toilet",
    63:"tvmonitor",
    64:"laptop",
    65:"mouse",
    66:"remote",
    67:"keyboard",
    68:"cell phone",
    69:"microwave",
    70:"oven",
    71:"toaster",
    72:"sink",
    73:"refrigerator",
    74:"book",
    75:"clock",
    76:"vase",
    77:"scissors",
    78:"teddy bear",
    79:"hair drier",
    80:"toothbrush",
}

imagenet_class = {
    0: 'tench, Tinca tinca',
    1: 'goldfish, Carassius auratus',
    2: 'great white shark, white shark, man-eater, man-eating shark, Carcharodon carcharias',
    3: 'tiger shark, Galeocerdo cuvieri',
    4: 'hammerhead, hammerhead shark',
    5: 'electric ray, crampfish, numbfish, torpedo',
    6: 'stingray',
    7: 'cock',
    8: 'hen',
    9: 'ostrich, Struthio camelus',
    10: 'brambling, Fringilla montifringilla',
    11: 'goldfinch, Carduelis carduelis',
    12: 'house finch, linnet, Carpodacus mexicanus',
    13: 'junco, snowbird',
    14: 'indigo bunting, indigo finch, indigo bird, Passerina cyanea',
    15: 'robin, American robin, Turdus migratorius',
    16: 'bulbul',
    17: 'jay',
    18: 'magpie',
    19: 'chickadee',
    20: 'water ouzel, dipper',
    21: 'kite',
    22: 'bald eagle, American eagle, Haliaeetus leucocephalus',
    23: 'vulture',
    24: 'great grey owl, great gray owl, Strix nebulosa',
    25: 'European fire salamander, Salamandra salamandra',
    26: 'common newt, Triturus vulgaris',
    27: 'eft',
    28: 'spotted salamander, Ambystoma maculatum',
    29: 'axolotl, mud puppy, Ambystoma mexicanum',
    30: 'bullfrog, Rana catesbeiana',
    31: 'tree frog, tree-frog',
    32: 'tailed frog, bell toad, ribbed toad, tailed toad, Ascaphus trui',
    33: 'loggerhead, loggerhead turtle, Caretta caretta',
    34: 'leatherback turtle, leatherback, leathery turtle, Dermochelys coriacea',
    35: 'mud turtle',
    36: 'terrapin',
    37: 'box turtle, box tortoise',
    38: 'banded gecko',
    39: 'common iguana, iguana, Iguana iguana',
    40: 'American chameleon, anole, Anolis carolinensis',
    41: 'whiptail, whiptail lizard',
    42: 'agama',
    43: 'frilled lizard, Chlamydosaurus kingi',
    44: 'alligator lizard',
    45: 'Gila monster, Heloderma suspectum',
    46: 'green lizard, Lacerta viridis',
    47: 'African chameleon, Chamaeleo chamaeleon',
    48: 'Komodo dragon, Komodo lizard, dragon lizard, giant lizard, Varanus komodoensis',
    49: 'African crocodile, Nile crocodile, Crocodylus niloticus',
    50: 'American alligator, Alligator mississipiensis',
    51: 'triceratops',
    52: 'thunder snake, worm snake, Carphophis amoenus',
    53: 'ringneck snake, ring-necked snake, ring snake',
    54: 'hognose snake, puff adder, sand viper',
    55: 'green snake, grass snake',
    56: 'king snake, kingsnake',
    57: 'garter snake, grass snake',
    58: 'water snake',
    59: 'vine snake',
    60: 'night snake, Hypsiglena torquata',
    61: 'boa constrictor, Constrictor constrictor',
    62: 'rock python, rock snake, Python sebae',
    63: 'Indian cobra, Naja naja',
    64: 'green mamba',
    65: 'sea snake',
    66: 'horned viper, cerastes, sand viper, horned asp, Cerastes cornutus',
    67: 'diamondback, diamondback rattlesnake, Crotalus adamanteus',
    68: 'sidewinder, horned rattlesnake, Crotalus cerastes',
    69: 'trilobite',
    70: 'harvestman, daddy longlegs, Phalangium opilio',
    71: 'scorpion',
    72: 'black and gold garden spider, Argiope aurantia',
    73: 'barn spider, Araneus cavaticus',
    74: 'garden spider, Aranea diademata',
    75: 'black widow, Latrodectus mactans',
    76: 'tarantula',
    77: 'wolf spider, hunting spider',
    78: 'tick',
    79: 'centipede',
    80: 'black grouse',
    81: 'ptarmigan',
    82: 'ruffed grouse, partridge, Bonasa umbellus',
    83: 'prairie chicken, prairie grouse, prairie fowl',
    84: 'peacock',
    85: 'quail',
    86: 'partridge',
    87: 'African grey, African gray, Psittacus erithacus',
    88: 'macaw',
    89: 'sulphur-crested cockatoo, Kakatoe galerita, Cacatua galerita',
    90: 'lorikeet',
    91: 'coucal',
    92: 'bee eater',
    93: 'hornbill',
    94: 'hummingbird',
    95: 'jacamar',
    96: 'toucan',
    97: 'drake',
    98: 'red-breasted merganser, Mergus serrator',
    99: 'goose',
    100: 'black swan, Cygnus atratus',
    101: 'tusker',
    102: 'echidna, spiny anteater, anteater',
    103: 'platypus, duckbill, duckbilled platypus, duck-billed platypus, Ornithorhynchus anatinus',
    104: 'wallaby, brush kangaroo',
    105: 'koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus',
    106: 'wombat',
    107: 'jellyfish',
    108: 'sea anemone, anemone',
    109: 'brain coral',
    110: 'flatworm, platyhelminth',
    111: 'nematode, nematode worm, roundworm',
    112: 'conch',
    113: 'snail',
    114: 'slug',
    115: 'sea slug, nudibranch',
    116: 'chiton, coat-of-mail shell, sea cradle, polyplacophore',
    117: 'chambered nautilus, pearly nautilus, nautilus',
    118: 'Dungeness crab, Cancer magister',
    119: 'rock crab, Cancer irroratus',
    120: 'fiddler crab',
    121: 'king crab, Alaska crab, Alaskan king crab, Alaska king crab, Paralithodes camtschatica',
    122: 'American lobster, Northern lobster, Maine lobster, Homarus americanus',
    123: 'spiny lobster, langouste, rock lobster, crawfish, crayfish, sea crawfish',
    124: 'crayfish, crawfish, crawdad, crawdaddy',
    125: 'hermit crab',
    126: 'isopod',
    127: 'white stork, Ciconia ciconia',
    128: 'black stork, Ciconia nigra',
    129: 'spoonbill',
    130: 'flamingo',
    131: 'little blue heron, Egretta caerulea',
    132: 'American egret, great white heron, Egretta albus',
    133: 'bittern',
    134: 'crane',
    135: 'limpkin, Aramus pictus',
    136: 'European gallinule, Porphyrio porphyrio',
    137: 'American coot, marsh hen, mud hen, water hen, Fulica americana',
    138: 'bustard',
    139: 'ruddy turnstone, Arenaria interpres',
    140: 'red-backed sandpiper, dunlin, Erolia alpina',
    141: 'redshank, Tringa totanus',
    142: 'dowitcher',
    143: 'oystercatcher, oyster catcher',
    144: 'pelican',
    145: 'king penguin, Aptenodytes patagonica',
    146: 'albatross, mollymawk',
    147: 'grey whale, gray whale, devilfish, Eschrichtius gibbosus, Eschrichtius robustus',
    148: 'killer whale, killer, orca, grampus, sea wolf, Orcinus orca',
    149: 'dugong, Dugong dugon',
    150: 'sea lion',
    151: 'Chihuahua',
    152: 'Japanese spaniel',
    153: 'Maltese dog, Maltese terrier, Maltese',
    154: 'Pekinese, Pekingese, Peke',
    155: 'Shih-Tzu',
    156: 'Blenheim spaniel',
    157: 'papillon',
    158: 'toy terrier',
    159: 'Rhodesian ridgeback',
    160: 'Afghan hound, Afghan',
    161: 'basset, basset hound',
    162: 'beagle',
    163: 'bloodhound, sleuthhound',
    164: 'bluetick',
    165: 'black-and-tan coonhound',
    166: 'Walker hound, Walker foxhound',
    167: 'English foxhound',
    168: 'redbone',
    169: 'borzoi, Russian wolfhound',
    170: 'Irish wolfhound',
    171: 'Italian greyhound',
    172: 'whippet',
    173: 'Ibizan hound, Ibizan Podenco',
    174: 'Norwegian elkhound, elkhound',
    175: 'otterhound, otter hound',
    176: 'Saluki, gazelle hound',
    177: 'Scottish deerhound, deerhound',
    178: 'Weimaraner',
    179: 'Staffordshire bullterrier, Staffordshire bull terrier',
    180: 'American Staffordshire terrier, Staffordshire terrier, American pit bull terrier, pit bull terrier',
    181: 'Bedlington terrier',
    182: 'Border terrier',
    183: 'Kerry blue terrier',
    184: 'Irish terrier',
    185: 'Norfolk terrier',
    186: 'Norwich terrier',
    187: 'Yorkshire terrier',
    188: 'wire-haired fox terrier',
    189: 'Lakeland terrier',
    190: 'Sealyham terrier, Sealyham',
    191: 'Airedale, Airedale terrier',
    192: 'cairn, cairn terrier',
    193: 'Australian terrier',
    194: 'Dandie Dinmont, Dandie Dinmont terrier',
    195: 'Boston bull, Boston terrier',
    196: 'miniature schnauzer',
    197: 'giant schnauzer',
    198: 'standard schnauzer',
    199: 'Scotch terrier, Scottish terrier, Scottie',
    200: 'Tibetan terrier, chrysanthemum dog',
    201: 'silky terrier, Sydney silky',
    202: 'soft-coated wheaten terrier',
    203: 'West Highland white terrier',
    204: 'Lhasa, Lhasa apso',
    205: 'flat-coated retriever',
    206: 'curly-coated retriever',
    207: 'golden retriever',
    208: 'Labrador retriever',
    209: 'Chesapeake Bay retriever',
    210: 'German short-haired pointer',
    211: 'vizsla, Hungarian pointer',
    212: 'English setter',
    213: 'Irish setter, red setter',
    214: 'Gordon setter',
    215: 'Brittany spaniel',
    216: 'clumber, clumber spaniel',
    217: 'English springer, English springer spaniel',
    218: 'Welsh springer spaniel',
    219: 'cocker spaniel, English cocker spaniel, cocker',
    220: 'Sussex spaniel',
    221: 'Irish water spaniel',
    222: 'kuvasz',
    223: 'schipperke',
    224: 'groenendael',
    225: 'malinois',
    226: 'briard',
    227: 'kelpie',
    228: 'komondor',
    229: 'Old English sheepdog, bobtail',
    230: 'Shetland sheepdog, Shetland sheep dog, Shetland',
    231: 'collie',
    232: 'Border collie',
    233: 'Bouvier des Flandres, Bouviers des Flandres',
    234: 'Rottweiler',
    235: 'German shepherd, German shepherd dog, German police dog, alsatian',
    236: 'Doberman, Doberman pinscher',
    237: 'miniature pinscher',
    238: 'Greater Swiss Mountain dog',
    239: 'Bernese mountain dog',
    240: 'Appenzeller',
    241: 'EntleBucher',
    242: 'boxer',
    243: 'bull mastiff',
    244: 'Tibetan mastiff',
    245: 'French bulldog',
    246: 'Great Dane',
    247: 'Saint Bernard, St Bernard',
    248: 'Eskimo dog, husky',
    249: 'malamute, malemute, Alaskan malamute',
    250: 'Siberian husky',
    251: 'dalmatian, coach dog, carriage dog',
    252: 'affenpinscher, monkey pinscher, monkey dog',
    253: 'basenji',
    254: 'pug, pug-dog',
    255: 'Leonberg',
    256: 'Newfoundland, Newfoundland dog',
    257: 'Great Pyrenees',
    258: 'Samoyed, Samoyede',
    259: 'Pomeranian',
    260: 'chow, chow chow',
    261: 'keeshond',
    262: 'Brabancon griffon',
    263: 'Pembroke, Pembroke Welsh corgi',
    264: 'Cardigan, Cardigan Welsh corgi',
    265: 'toy poodle',
    266: 'miniature poodle',
    267: 'standard poodle',
    268: 'Mexican hairless',
    269: 'timber wolf, grey wolf, gray wolf, Canis lupus',
    270: 'white wolf, Arctic wolf, Canis lupus tundrarum',
    271: 'red wolf, maned wolf, Canis rufus, Canis niger',
    272: 'coyote, prairie wolf, brush wolf, Canis latrans',
    273: 'dingo, warrigal, warragal, Canis dingo',
    274: 'dhole, Cuon alpinus',
    275: 'African hunting dog, hyena dog, Cape hunting dog, Lycaon pictus',
    276: 'hyena, hyaena',
    277: 'red fox, Vulpes vulpes',
    278: 'kit fox, Vulpes macrotis',
    279: 'Arctic fox, white fox, Alopex lagopus',
    280: 'grey fox, gray fox, Urocyon cinereoargenteus',
    281: 'tabby, tabby cat',
    282: 'tiger cat',
    283: 'Persian cat',
    284: 'Siamese cat, Siamese',
    285: 'Egyptian cat',
    286: 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor',
    287: 'lynx, catamount',
    288: 'leopard, Panthera pardus',
    289: 'snow leopard, ounce, Panthera uncia',
    290: 'jaguar, panther, Panthera onca, Felis onca',
    291: 'lion, king of beasts, Panthera leo',
    292: 'tiger, Panthera tigris',
    293: 'cheetah, chetah, Acinonyx jubatus',
    294: 'brown bear, bruin, Ursus arctos',
    295: 'American black bear, black bear, Ursus americanus, Euarctos americanus',
    296: 'ice bear, polar bear, Ursus Maritimus, Thalarctos maritimus',
    297: 'sloth bear, Melursus ursinus, Ursus ursinus',
    298: 'mongoose',
    299: 'meerkat, mierkat',
    300: 'tiger beetle',
    301: 'ladybug, ladybeetle, lady beetle, ladybird, ladybird beetle',
    302: 'ground beetle, carabid beetle',
    303: 'long-horned beetle, longicorn, longicorn beetle',
    304: 'leaf beetle, chrysomelid',
    305: 'dung beetle',
    306: 'rhinoceros beetle',
    307: 'weevil',
    308: 'fly',
    309: 'bee',
    310: 'ant, emmet, pismire',
    311: 'grasshopper, hopper',
    312: 'cricket',
    313: 'walking stick, walkingstick, stick insect',
    314: 'cockroach, roach',
    315: 'mantis, mantid',
    316: 'cicada, cicala',
    317: 'leafhopper',
    318: 'lacewing, lacewing fly',
    319: "dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk",
    320: 'damselfly',
    321: 'admiral',
    322: 'ringlet, ringlet butterfly',
    323: 'monarch, monarch butterfly, milkweed butterfly, Danaus plexippus',
    324: 'cabbage butterfly',
    325: 'sulphur butterfly, sulfur butterfly',
    326: 'lycaenid, lycaenid butterfly',
    327: 'starfish, sea star',
    328: 'sea urchin',
    329: 'sea cucumber, holothurian',
    330: 'wood rabbit, cottontail, cottontail rabbit',
    331: 'hare',
    332: 'Angora, Angora rabbit',
    333: 'hamster',
    334: 'porcupine, hedgehog',
    335: 'fox squirrel, eastern fox squirrel, Sciurus niger',
    336: 'marmot',
    337: 'beaver',
    338: 'guinea pig, Cavia cobaya',
    339: 'sorrel',
    340: 'zebra',
    341: 'hog, pig, grunter, squealer, Sus scrofa',
    342: 'wild boar, boar, Sus scrofa',
    343: 'warthog',
    344: 'hippopotamus, hippo, river horse, Hippopotamus amphibius',
    345: 'ox',
    346: 'water buffalo, water ox, Asiatic buffalo, Bubalus bubalis',
    347: 'bison',
    348: 'ram, tup',
    349: 'bighorn, bighorn sheep, cimarron, Rocky Mountain bighorn, Rocky Mountain sheep, Ovis canadensis',
    350: 'ibex, Capra ibex',
    351: 'hartebeest',
    352: 'impala, Aepyceros melampus',
    353: 'gazelle',
    354: 'Arabian camel, dromedary, Camelus dromedarius',
    355: 'llama',
    356: 'weasel',
    357: 'mink',
    358: 'polecat, fitch, foulmart, foumart, Mustela putorius',
    359: 'black-footed ferret, ferret, Mustela nigripes',
    360: 'otter',
    361: 'skunk, polecat, wood pussy',
    362: 'badger',
    363: 'armadillo',
    364: 'three-toed sloth, ai, Bradypus tridactylus',
    365: 'orangutan, orang, orangutang, Pongo pygmaeus',
    366: 'gorilla, Gorilla gorilla',
    367: 'chimpanzee, chimp, Pan troglodytes',
    368: 'gibbon, Hylobates lar',
    369: 'siamang, Hylobates syndactylus, Symphalangus syndactylus',
    370: 'guenon, guenon monkey',
    371: 'patas, hussar monkey, Erythrocebus patas',
    372: 'baboon',
    373: 'macaque',
    374: 'langur',
    375: 'colobus, colobus monkey',
    376: 'proboscis monkey, Nasalis larvatus',
    377: 'marmoset',
    378: 'capuchin, ringtail, Cebus capucinus',
    379: 'howler monkey, howler',
    380: 'titi, titi monkey',
    381: 'spider monkey, Ateles geoffroyi',
    382: 'squirrel monkey, Saimiri sciureus',
    383: 'Madagascar cat, ring-tailed lemur, Lemur catta',
    384: 'indri, indris, Indri indri, Indri brevicaudatus',
    385: 'Indian elephant, Elephas maximus',
    386: 'African elephant, Loxodonta africana',
    387: 'lesser panda, red panda, panda, bear cat, cat bear, Ailurus fulgens',
    388: 'giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca',
    389: 'barracouta, snoek',
    390: 'eel',
    391: 'coho, cohoe, coho salmon, blue jack, silver salmon, Oncorhynchus kisutch',
    392: 'rock beauty, Holocanthus tricolor',
    393: 'anemone fish',
    394: 'sturgeon',
    395: 'gar, garfish, garpike, billfish, Lepisosteus osseus',
    396: 'lionfish',
    397: 'puffer, pufferfish, blowfish, globefish',
    398: 'abacus',
    399: 'abaya',
    400: "academic gown, academic robe, judge's robe",
    401: 'accordion, piano accordion, squeeze box',
    402: 'acoustic guitar',
    403: 'aircraft carrier, carrier, flattop, attack aircraft carrier',
    404: 'airliner',
    405: 'airship, dirigible',
    406: 'altar',
    407: 'ambulance',
    408: 'amphibian, amphibious vehicle',
    409: 'analog clock',
    410: 'apiary, bee house',
    411: 'apron',
    412: 'ashcan, trash can, garbage can, wastebin, ash bin, ash-bin, ashbin, dustbin, trash barrel, trash bin',
    413: 'assault rifle, assault gun',
    414: 'backpack, back pack, knapsack, packsack, rucksack, haversack',
    415: 'bakery, bakeshop, bakehouse',
    416: 'balance beam, beam',
    417: 'balloon',
    418: 'ballpoint, ballpoint pen, ballpen, Biro',
    419: 'Band Aid',
    420: 'banjo',
    421: 'bannister, banister, balustrade, balusters, handrail',
    422: 'barbell',
    423: 'barber chair',
    424: 'barbershop',
    425: 'barn',
    426: 'barometer',
    427: 'barrel, cask',
    428: 'barrow, garden cart, lawn cart, wheelbarrow',
    429: 'baseball',
    430: 'basketball',
    431: 'bassinet',
    432: 'bassoon',
    433: 'bathing cap, swimming cap',
    434: 'bath towel',
    435: 'bathtub, bathing tub, bath, tub',
    436: 'beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon',
    437: 'beacon, lighthouse, beacon light, pharos',
    438: 'beaker',
    439: 'bearskin, busby, shako',
    440: 'beer bottle',
    441: 'beer glass',
    442: 'bell cote, bell cot',
    443: 'bib',
    444: 'bicycle-built-for-two, tandem bicycle, tandem',
    445: 'bikini, two-piece',
    446: 'binder, ring-binder',
    447: 'binoculars, field glasses, opera glasses',
    448: 'birdhouse',
    449: 'boathouse',
    450: 'bobsled, bobsleigh, bob',
    451: 'bolo tie, bolo, bola tie, bola',
    452: 'bonnet, poke bonnet',
    453: 'bookcase',
    454: 'bookshop, bookstore, bookstall',
    455: 'bottlecap',
    456: 'bow',
    457: 'bow tie, bow-tie, bowtie',
    458: 'brass, memorial tablet, plaque',
    459: 'brassiere, bra, bandeau',
    460: 'breakwater, groin, groyne, mole, bulwark, seawall, jetty',
    461: 'breastplate, aegis, egis',
    462: 'broom',
    463: 'bucket, pail',
    464: 'buckle',
    465: 'bulletproof vest',
    466: 'bullet train, bullet',
    467: 'butcher shop, meat market',
    468: 'cab, hack, taxi, taxicab',
    469: 'caldron, cauldron',
    470: 'candle, taper, wax light',
    471: 'cannon',
    472: 'canoe',
    473: 'can opener, tin opener',
    474: 'cardigan',
    475: 'car mirror',
    476: 'carousel, carrousel, merry-go-round, roundabout, whirligig',
    477: "carpenter's kit, tool kit",
    478: 'carton',
    479: 'car wheel',
    480: 'cash machine, cash dispenser, automated teller machine, automatic teller machine, automated teller, automatic teller, ATM',
    481: 'cassette',
    482: 'cassette player',
    483: 'castle',
    484: 'catamaran',
    485: 'CD player',
    486: 'cello, violoncello',
    487: 'cellular telephone, cellular phone, cellphone, cell, mobile phone',
    488: 'chain',
    489: 'chainlink fence',
    490: 'chain mail, ring mail, mail, chain armor, chain armour, ring armor, ring armour',
    491: 'chain saw, chainsaw',
    492: 'chest',
    493: 'chiffonier, commode',
    494: 'chime, bell, gong',
    495: 'china cabinet, china closet',
    496: 'Christmas stocking',
    497: 'church, church building',
    498: 'cinema, movie theater, movie theatre, movie house, picture palace',
    499: 'cleaver, meat cleaver, chopper',
    500: 'cliff dwelling',
    501: 'cloak',
    502: 'clog, geta, patten, sabot',
    503: 'cocktail shaker',
    504: 'coffee mug',
    505: 'coffeepot',
    506: 'coil, spiral, volute, whorl, helix',
    507: 'combination lock',
    508: 'computer keyboard, keypad',
    509: 'confectionery, confectionary, candy store',
    510: 'container ship, containership, container vessel',
    511: 'convertible',
    512: 'corkscrew, bottle screw',
    513: 'cornet, horn, trumpet, trump',
    514: 'cowboy boot',
    515: 'cowboy hat, ten-gallon hat',
    516: 'cradle',
    517: 'crane',
    518: 'crash helmet',
    519: 'crate',
    520: 'crib, cot',
    521: 'Crock Pot',
    522: 'croquet ball',
    523: 'crutch',
    524: 'cuirass',
    525: 'dam, dike, dyke',
    526: 'desk',
    527: 'desktop computer',
    528: 'dial telephone, dial phone',
    529: 'diaper, nappy, napkin',
    530: 'digital clock',
    531: 'digital watch',
    532: 'dining table, board',
    533: 'dishrag, dishcloth',
    534: 'dishwasher, dish washer, dishwashing machine',
    535: 'disk brake, disc brake',
    536: 'dock, dockage, docking facility',
    537: 'dogsled, dog sled, dog sleigh',
    538: 'dome',
    539: 'doormat, welcome mat',
    540: 'drilling platform, offshore rig',
    541: 'drum, membranophone, tympan',
    542: 'drumstick',
    543: 'dumbbell',
    544: 'Dutch oven',
    545: 'electric fan, blower',
    546: 'electric guitar',
    547: 'electric locomotive',
    548: 'entertainment center',
    549: 'envelope',
    550: 'espresso maker',
    551: 'face powder',
    552: 'feather boa, boa',
    553: 'file, file cabinet, filing cabinet',
    554: 'fireboat',
    555: 'fire engine, fire truck',
    556: 'fire screen, fireguard',
    557: 'flagpole, flagstaff',
    558: 'flute, transverse flute',
    559: 'folding chair',
    560: 'football helmet',
    561: 'forklift',
    562: 'fountain',
    563: 'fountain pen',
    564: 'four-poster',
    565: 'freight car',
    566: 'French horn, horn',
    567: 'frying pan, frypan, skillet',
    568: 'fur coat',
    569: 'garbage truck, dustcart',
    570: 'gasmask, respirator, gas helmet',
    571: 'gas pump, gasoline pump, petrol pump, island dispenser',
    572: 'goblet',
    573: 'go-kart',
    574: 'golf ball',
    575: 'golfcart, golf cart',
    576: 'gondola',
    577: 'gong, tam-tam',
    578: 'gown',
    579: 'grand piano, grand',
    580: 'greenhouse, nursery, glasshouse',
    581: 'grille, radiator grille',
    582: 'grocery store, grocery, food market, market',
    583: 'guillotine',
    584: 'hair slide',
    585: 'hair spray',
    586: 'half track',
    587: 'hammer',
    588: 'hamper',
    589: 'hand blower, blow dryer, blow drier, hair dryer, hair drier',
    590: 'hand-held computer, hand-held microcomputer',
    591: 'handkerchief, hankie, hanky, hankey',
    592: 'hard disc, hard disk, fixed disk',
    593: 'harmonica, mouth organ, harp, mouth harp',
    594: 'harp',
    595: 'harvester, reaper',
    596: 'hatchet',
    597: 'holster',
    598: 'home theater, home theatre',
    599: 'honeycomb',
    600: 'hook, claw',
    601: 'hoopskirt, crinoline',
    602: 'horizontal bar, high bar',
    603: 'horse cart, horse-cart',
    604: 'hourglass',
    605: 'iPod',
    606: 'iron, smoothing iron',
    607: "jack-o'-lantern",
    608: 'jean, blue jean, denim',
    609: 'jeep, landrover',
    610: 'jersey, T-shirt, tee shirt',
    611: 'jigsaw puzzle',
    612: 'jinrikisha, ricksha, rickshaw',
    613: 'joystick',
    614: 'kimono',
    615: 'knee pad',
    616: 'knot',
    617: 'lab coat, laboratory coat',
    618: 'ladle',
    619: 'lampshade, lamp shade',
    620: 'laptop, laptop computer',
    621: 'lawn mower, mower',
    622: 'lens cap, lens cover',
    623: 'letter opener, paper knife, paperknife',
    624: 'library',
    625: 'lifeboat',
    626: 'lighter, light, igniter, ignitor',
    627: 'limousine, limo',
    628: 'liner, ocean liner',
    629: 'lipstick, lip rouge',
    630: 'Loafer',
    631: 'lotion',
    632: 'loudspeaker, speaker, speaker unit, loudspeaker system, speaker system',
    633: "loupe, jeweler's loupe",
    634: 'lumbermill, sawmill',
    635: 'magnetic compass',
    636: 'mailbag, postbag',
    637: 'mailbox, letter box',
    638: 'maillot',
    639: 'maillot, tank suit',
    640: 'manhole cover',
    641: 'maraca',
    642: 'marimba, xylophone',
    643: 'mask',
    644: 'matchstick',
    645: 'maypole',
    646: 'maze, labyrinth',
    647: 'measuring cup',
    648: 'medicine chest, medicine cabinet',
    649: 'megalith, megalithic structure',
    650: 'microphone, mike',
    651: 'microwave, microwave oven',
    652: 'military uniform',
    653: 'milk can',
    654: 'minibus',
    655: 'miniskirt, mini',
    656: 'minivan',
    657: 'missile',
    658: 'mitten',
    659: 'mixing bowl',
    660: 'mobile home, manufactured home',
    661: 'Model T',
    662: 'modem',
    663: 'monastery',
    664: 'monitor',
    665: 'moped',
    666: 'mortar',
    667: 'mortarboard',
    668: 'mosque',
    669: 'mosquito net',
    670: 'motor scooter, scooter',
    671: 'mountain bike, all-terrain bike, off-roader',
    672: 'mountain tent',
    673: 'mouse, computer mouse',
    674: 'mousetrap',
    675: 'moving van',
    676: 'muzzle',
    677: 'nail',
    678: 'neck brace',
    679: 'necklace',
    680: 'nipple',
    681: 'notebook, notebook computer',
    682: 'obelisk',
    683: 'oboe, hautboy, hautbois',
    684: 'ocarina, sweet potato',
    685: 'odometer, hodometer, mileometer, milometer',
    686: 'oil filter',
    687: 'organ, pipe organ',
    688: 'oscilloscope, scope, cathode-ray oscilloscope, CRO',
    689: 'overskirt',
    690: 'oxcart',
    691: 'oxygen mask',
    692: 'packet',
    693: 'paddle, boat paddle',
    694: 'paddlewheel, paddle wheel',
    695: 'padlock',
    696: 'paintbrush',
    697: "pajama, pyjama, pj's, jammies",
    698: 'palace',
    699: 'panpipe, pandean pipe, syrinx',
    700: 'paper towel',
    701: 'parachute, chute',
    702: 'parallel bars, bars',
    703: 'park bench',
    704: 'parking meter',
    705: 'passenger car, coach, carriage',
    706: 'patio, terrace',
    707: 'pay-phone, pay-station',
    708: 'pedestal, plinth, footstall',
    709: 'pencil box, pencil case',
    710: 'pencil sharpener',
    711: 'perfume, essence',
    712: 'Petri dish',
    713: 'photocopier',
    714: 'pick, plectrum, plectron',
    715: 'pickelhaube',
    716: 'picket fence, paling',
    717: 'pickup, pickup truck',
    718: 'pier',
    719: 'piggy bank, penny bank',
    720: 'pill bottle',
    721: 'pillow',
    722: 'ping-pong ball',
    723: 'pinwheel',
    724: 'pirate, pirate ship',
    725: 'pitcher, ewer',
    726: "plane, carpenter's plane, woodworking plane",
    727: 'planetarium',
    728: 'plastic bag',
    729: 'plate rack',
    730: 'plow, plough',
    731: "plunger, plumber's helper",
    732: 'Polaroid camera, Polaroid Land camera',
    733: 'pole',
    734: 'police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria',
    735: 'poncho',
    736: 'pool table, billiard table, snooker table',
    737: 'pop bottle, soda bottle',
    738: 'pot, flowerpot',
    739: "potter's wheel",
    740: 'power drill',
    741: 'prayer rug, prayer mat',
    742: 'printer',
    743: 'prison, prison house',
    744: 'projectile, missile',
    745: 'projector',
    746: 'puck, hockey puck',
    747: 'punching bag, punch bag, punching ball, punchball',
    748: 'purse',
    749: 'quill, quill pen',
    750: 'quilt, comforter, comfort, puff',
    751: 'racer, race car, racing car',
    752: 'racket, racquet',
    753: 'radiator',
    754: 'radio, wireless',
    755: 'radio telescope, radio reflector',
    756: 'rain barrel',
    757: 'recreational vehicle, RV, R.V.',
    758: 'reel',
    759: 'reflex camera',
    760: 'refrigerator, icebox',
    761: 'remote control, remote',
    762: 'restaurant, eating house, eating place, eatery',
    763: 'revolver, six-gun, six-shooter',
    764: 'rifle',
    765: 'rocking chair, rocker',
    766: 'rotisserie',
    767: 'rubber eraser, rubber, pencil eraser',
    768: 'rugby ball',
    769: 'rule, ruler',
    770: 'running shoe',
    771: 'safe',
    772: 'safety pin',
    773: 'saltshaker, salt shaker',
    774: 'sandal',
    775: 'sarong',
    776: 'sax, saxophone',
    777: 'scabbard',
    778: 'scale, weighing machine',
    779: 'school bus',
    780: 'schooner',
    781: 'scoreboard',
    782: 'screen, CRT screen',
    783: 'screw',
    784: 'screwdriver',
    785: 'seat belt, seatbelt',
    786: 'sewing machine',
    787: 'shield, buckler',
    788: 'shoe shop, shoe-shop, shoe store',
    789: 'shoji',
    790: 'shopping basket',
    791: 'shopping cart',
    792: 'shovel',
    793: 'shower cap',
    794: 'shower curtain',
    795: 'ski',
    796: 'ski mask',
    797: 'sleeping bag',
    798: 'slide rule, slipstick',
    799: 'sliding door',
    800: 'slot, one-armed bandit',
    801: 'snorkel',
    802: 'snowmobile',
    803: 'snowplow, snowplough',
    804: 'soap dispenser',
    805: 'soccer ball',
    806: 'sock',
    807: 'solar dish, solar collector, solar furnace',
    808: 'sombrero',
    809: 'soup bowl',
    810: 'space bar',
    811: 'space heater',
    812: 'space shuttle',
    813: 'spatula',
    814: 'speedboat',
    815: "spider web, spider's web",
    816: 'spindle',
    817: 'sports car, sport car',
    818: 'spotlight, spot',
    819: 'stage',
    820: 'steam locomotive',
    821: 'steel arch bridge',
    822: 'steel drum',
    823: 'stethoscope',
    824: 'stole',
    825: 'stone wall',
    826: 'stopwatch, stop watch',
    827: 'stove',
    828: 'strainer',
    829: 'streetcar, tram, tramcar, trolley, trolley car',
    830: 'stretcher',
    831: 'studio couch, day bed',
    832: 'stupa, tope',
    833: 'submarine, pigboat, sub, U-boat',
    834: 'suit, suit of clothes',
    835: 'sundial',
    836: 'sunglass',
    837: 'sunglasses, dark glasses, shades',
    838: 'sunscreen, sunblock, sun blocker',
    839: 'suspension bridge',
    840: 'swab, swob, mop',
    841: 'sweatshirt',
    842: 'swimming trunks, bathing trunks',
    843: 'swing',
    844: 'switch, electric switch, electrical switch',
    845: 'syringe',
    846: 'table lamp',
    847: 'tank, army tank, armored combat vehicle, armoured combat vehicle',
    848: 'tape player',
    849: 'teapot',
    850: 'teddy, teddy bear',
    851: 'television, television system',
    852: 'tennis ball',
    853: 'thatch, thatched roof',
    854: 'theater curtain, theatre curtain',
    855: 'thimble',
    856: 'thresher, thrasher, threshing machine',
    857: 'throne',
    858: 'tile roof',
    859: 'toaster',
    860: 'tobacco shop, tobacconist shop, tobacconist',
    861: 'toilet seat',
    862: 'torch',
    863: 'totem pole',
    864: 'tow truck, tow car, wrecker',
    865: 'toyshop',
    866: 'tractor',
    867: 'trailer truck, tractor trailer, trucking rig, rig, articulated lorry, semi',
    868: 'tray',
    869: 'trench coat',
    870: 'tricycle, trike, velocipede',
    871: 'trimaran',
    872: 'tripod',
    873: 'triumphal arch',
    874: 'trolleybus, trolley coach, trackless trolley',
    875: 'trombone',
    876: 'tub, vat',
    877: 'turnstile',
    878: 'typewriter keyboard',
    879: 'umbrella',
    880: 'unicycle, monocycle',
    881: 'upright, upright piano',
    882: 'vacuum, vacuum cleaner',
    883: 'vase',
    884: 'vault',
    885: 'velvet',
    886: 'vending machine',
    887: 'vestment',
    888: 'viaduct',
    889: 'violin, fiddle',
    890: 'volleyball',
    891: 'waffle iron',
    892: 'wall clock',
    893: 'wallet, billfold, notecase, pocketbook',
    894: 'wardrobe, closet, press',
    895: 'warplane, military plane',
    896: 'washbasin, handbasin, washbowl, lavabo, wash-hand basin',
    897: 'washer, automatic washer, washing machine',
    898: 'water bottle',
    899: 'water jug',
    900: 'water tower',
    901: 'whiskey jug',
    902: 'whistle',
    903: 'wig',
    904: 'window screen',
    905: 'window shade',
    906: 'Windsor tie',
    907: 'wine bottle',
    908: 'wing',
    909: 'wok',
    910: 'wooden spoon',
    911: 'wool, woolen, woollen',
    912: 'worm fence, snake fence, snake-rail fence, Virginia fence',
    913: 'wreck',
    914: 'yawl',
    915: 'yurt',
    916: 'web site, website, internet site, site',
    917: 'comic book',
    918: 'crossword puzzle, crossword',
    919: 'street sign',
    920: 'traffic light, traffic signal, stoplight',
    921: 'book jacket, dust cover, dust jacket, dust wrapper',
    922: 'menu',
    923: 'plate',
    924: 'guacamole',
    925: 'consomme',
    926: 'hot pot, hotpot',
    927: 'trifle',
    928: 'ice cream, icecream',
    929: 'ice lolly, lolly, lollipop, popsicle',
    930: 'French loaf',
    931: 'bagel, beigel',
    932: 'pretzel',
    933: 'cheeseburger',
    934: 'hotdog, hot dog, red hot',
    935: 'mashed potato',
    936: 'head cabbage',
    937: 'broccoli',
    938: 'cauliflower',
    939: 'zucchini, courgette',
    940: 'spaghetti squash',
    941: 'acorn squash',
    942: 'butternut squash',
    943: 'cucumber, cuke',
    944: 'artichoke, globe artichoke',
    945: 'bell pepper',
    946: 'cardoon',
    947: 'mushroom',
    948: 'Granny Smith',
    949: 'strawberry',
    950: 'orange',
    951: 'lemon',
    952: 'fig',
    953: 'pineapple, ananas',
    954: 'banana',
    955: 'jackfruit, jak, jack',
    956: 'custard apple',
    957: 'pomegranate',
    958: 'hay',
    959: 'carbonara',
    960: 'chocolate sauce, chocolate syrup',
    961: 'dough',
    962: 'meat loaf, meatloaf',
    963: 'pizza, pizza pie',
    964: 'potpie',
    965: 'burrito',
    966: 'red wine',
    967: 'espresso',
    968: 'cup',
    969: 'eggnog',
    970: 'alp',
    971: 'bubble',
    972: 'cliff, drop, drop-off',
    973: 'coral reef',
    974: 'geyser',
    975: 'lakeside, lakeshore',
    976: 'promontory, headland, head, foreland',
    977: 'sandbar, sand bar',
    978: 'seashore, coast, seacoast, sea-coast',
    979: 'valley, vale',
    980: 'volcano',
    981: 'ballplayer, baseball player',
    982: 'groom, bridegroom',
    983: 'scuba diver',
    984: 'rapeseed',
    985: 'daisy',
    986: "yellow lady's slipper, yellow lady-slipper, Cypripedium calceolus, Cypripedium parviflorum",
    987: 'corn',
    988: 'acorn',
    989: 'hip, rose hip, rosehip',
    990: 'buckeye, horse chestnut, conker',
    991: 'coral fungus',
    992: 'agaric',
    993: 'gyromitra',
    994: 'stinkhorn, carrion fungus',
    995: 'earthstar',
    996: 'hen-of-the-woods, hen of the woods, Polyporus frondosus, Grifola frondosa',
    997: 'bolete',
    998: 'ear, spike, capitulum',
    999: 'toilet tissue, toilet paper, bathroom tissue'}
