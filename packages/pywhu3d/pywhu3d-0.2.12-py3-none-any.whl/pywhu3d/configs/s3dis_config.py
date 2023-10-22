from pywhu3d.configs.base_config import BaseConfig
import argparse

parser = argparse.ArgumentParser(description="SSTNet for Point Cloud Instance Segmentation")
parser.add_argument("--debug", action='store_true', help='debug or not')
parser.add_argument("--gpu", default='0', help='gpu')

args_cfg = parser.parse_args()

class S3DISInsConfig(BaseConfig):
    def __init__(
            self,
            info='reduce_gpu',
            debug=False,
            # debug=True,

            num_points=40000,
            size_x=3,
            size_y=3,
            stride=1.5,
            threshold=500,
            exclude_set={},
            sample_points=True,
            compute_normal=False,
            map_label=False,
            trans_xyz=True,

            num_workers=0,
            gpu='0',
            multi_gpu=args_cfg.gpu,

            train_batch_size=6,  # 128(1) 20(3), 12
            test_batch_size=36,  # 800, 120, 64
            train_split='train',
            test_split='test',
            dataset='s3dis',
            train_data_dir='experiment/data/s3dis_blocks/3-3_15_40000_13_bbox_02',
            test_data_dir='experiment/data/s3dis_blocks/3-3_15_40000_13_bbox_02',
            # pretrain='e2e-s3dis[0.458]_051_0.4880.pth',
            pretrain=None,
            ifClustering=True,
            # train_data_dir='experiment/data/s3dis_blocks/old/3_10_no_box',
            # test_data_dir='experiment/data/s3dis_blocks/old/3_15_no_box',

            num_classes=13,
            in_channels=9,  # jsis3d: 9; bonet: 12

            model_name='S3DISIns[0.876]_075_0.6174.pth',
            visual_dir='experiment/pred/visual',
            exclude_ins=[],
            compute_cat_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            compute_ins_list=range(13),
    ):
        super(S3DISInsConfig, self).__init__( \
            size_x=size_x,
            size_y=size_y,
            stride=stride,
            threshold=threshold,
            train_batch_size=train_batch_size*len(multi_gpu.split(',')),
            test_batch_size=test_batch_size*len(multi_gpu.split(',')),
            num_points=num_points,
            num_workers=num_workers,
            gpu=gpu,
            multi_gpu=multi_gpu,
            train_split=train_split,
            test_split=test_split,
            debug=debug,
            dataset=dataset,
            train_data_dir=train_data_dir,
            test_data_dir=test_data_dir,
            num_classes=num_classes,
            in_channels=in_channels,
            visual_dir=visual_dir,
            model_name=model_name,
            pretrain=pretrain,
            info=info
        )
        if args_cfg.debug:
            self.train_split = 'val'
            self.test_split = 'val'
            # self.multi_gpu='0'
            self.multi_gpu = '0'
            self.train_batch_size = 2
            self.test_batch_size = 16
            self.print_batch = 1
            self.validation = True
        else:
            from rich.traceback import install
            install(extra_lines=1)
        self.sample_points = sample_points
        self.compute_normal = compute_normal
        self.trans_xyz = trans_xyz
        self.map_label = map_label
        self.exclude_set = exclude_set
        self.exclude_ins = exclude_ins
        self.compute_cat_list = compute_cat_list
        self.compute_ins_list = compute_ins_list
        self.ifClustering = ifClustering


classes = ['ceil.', 'floor', 'wall', 'beam', 'col', 'window', 'door', 'table', 'chair', 'sofa', 'bkcase', 'board', 'clttr']
class2label = {cls: i for i, cls in enumerate(classes)}
sem_map = {i: i for i, cls in enumerate(classes)}
sem_list_no_ins = []

sem_color_map = {
    0: [255, 199, 137],  # 地面(非道路)
    1: [168, 255, 63],  # 树木1
    2: [56, 255, 139],  # 其它街道家具
    3: [255, 51, 104],  # 房屋建筑类
    4: [180, 167, 255],  # 箱状地物
    5: [29, 250, 255],  # 路灯
    6: [252, 116, 197],  # 电线杆
    7: [242, 239, 103],  # 市政立杆
    8: [61, 172, 0],  # 低矮植被
    9: [55, 227, 236],  # 附属提示牌
    10: [255, 143, 51],  # 独立提示牌
    11: [255, 255, 0],  # 道路标线
    12: [137, 255, 182]  # 机动车
}

class_weights = [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1
]

seg_label_to_cat = {class2label[i]: i for i in class2label.keys()}
