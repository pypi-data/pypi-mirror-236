from  base_config import BaseConfig

class SCANNETInsConfig(BaseConfig):
    def __init__(
            self,
            debug=False,
            # debug=True,

            num_points=4096,
            size_x=3,
            size_y=3,
            stride=1.0,
            threshold=50,
            exclude_set={},
            sample_points=False,
            compute_normal=False,
            map_label=False,
            trans_xyz=True,

            num_workers=0,
            gpu='0',
            multi_gpu='0,1,2,3',

            train_batch_size=128,  # 128(1) 20(3), 12
            test_batch_size=800,  # 800, 120, 64
            train_split='train',
            test_split='val',
            dataset='scannet',
            train_data_dir='experiment/data/scannet_blocks/3-3_10_4096',
            test_data_dir='experiment/data/scannet_blocks/3-3_10_4096',

            num_classes=41,
            in_channels=9,  # jsis3d: 9; bonet: 12

            model_name=None,
            visual_dir='experiment/pred/visual',
            exclude_ins=[]
    ):
        super(SCANNETInsConfig, self).__init__( \
            size_x=size_x,
            size_y=size_y,
            stride=stride,
            threshold=threshold,
            train_batch_size=train_batch_size,
            test_batch_size=test_batch_size,
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
        )
        if debug==True:
            self.train_split='val'
            self.test_split='val'
            self.multi_gpu='0'
            self.batchsize=2
            self.test_batch_size=16
            self.print_batch=1
            self.validation = True
        self.sample_points = sample_points
        self.compute_normal = compute_normal
        self.trans_xyz = trans_xyz
        self.map_label = map_label
        self.exclude_set=exclude_set
        self.exclude_ins = exclude_ins

# classes = ['cabinet', 'bed', 'chair', 'sofa', 'table', 'door', 'window', 'bookshelf', 'picture', 'counter', 'desk',
#                 'curtain', 'refrigerator', 'shower curtain', 'toilet', 'sink', 'bathtub', 'otherfurniture']
# sem_list = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 24, 28, 33, 34, 36, 39]
class2label = {
    'unknown': 0,
    'wall': 1,
    'floor': 2,
    'cabinet': 3,
    'bed': 4,
    'chair': 5,
    'sofa': 6,
    'table': 7,
    'door': 8,
    'window': 9,
    'bookshelf': 10,
    'picture': 11,
    'counter': 12,
    'blinds': 13,
    'desk': 14,
    'shelves': 15,
    'curtain': 16,
    'dresser': 17,
    'pillow': 18,
    'mirror': 19,
    'floor mat': 20,
    'clothes': 21,
    'ceiling': 22,
    'books': 23,
    'refridgerator': 24,
    'television': 25,
    'paper': 26,
    'towel': 27,
    'shower curtain': 28,
    'box': 29,
    'whiteboard': 30,
    'person': 31,
    'night stand': 32,
    'toilet': 33,
    'sink': 34,
    'lamp': 35,
    'bathtub': 36,
    'bag': 37,
    'otherstructure': 38,
    'otherfurniture': 39,
    'otherprop': 40,
}
sem_map = {sem: i for i, sem in enumerate(class2label.values())}
# class2label = {cls: i for i, cls in enumerate(classes)}
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
    12: [137, 255, 182],  # 机动车
    13: [242, 135, 110],  # 行人
    14: [255, 75, 75],  # 消防栓
    15: [255, 224, 109],  # 信号灯
    16: [231, 183, 255],  # 独立探头
    17: [109, 172, 255],  # 公交站牌
    18: [51, 85, 255],  # 电线
}
