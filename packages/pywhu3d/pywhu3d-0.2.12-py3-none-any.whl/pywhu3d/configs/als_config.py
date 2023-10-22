from pywhu3d.configs.base_config import BaseConfig

class ALSInsConfig(BaseConfig):
    def __init__(
            self,
            # debug=False,
            debug=True,

            num_points=40960,
            size_x=40,
            size_y=40,
            stride=30,
            threshold=1000,
            grid_size=0.05,
            normal_radius=0.8,
            exclude_set={},
            sample_points=True,
            compute_normal=True,
            map_label=True,
            trans_xyz=True,

            num_workers=1,
            gpu='0',
            multi_gpu='0, 1, 2, 3',

            train_batch_size=12,
            test_batch_size=48,
            train_split='train',
            test_split='test',
            dataset='als',
            train_data_dir='experiment/data/als_blocks/40-40_200_40960_8_box',
            test_data_dir='experiment/data/als_blocks/40-40_300_40960_8_box',

            num_classes=8,
            in_channels=9,  # jsis3d: 9; bonet: 12

            model_name = 'als[0.672]_061_0.5324',
            visual_dir = 'experiment/pred/visual',
            exclude_ins = [],
            compute_cat_list=[1, 2, 3, 4, 5, 6, 7],
            compute_ins_list=[2,3]
    ):
        super(ALSInsConfig, self).__init__(
            size_x = size_x,
            size_y = size_y,
            stride = stride,
            threshold = threshold,
            grid_size = grid_size,
            normal_radius = normal_radius,
            train_batch_size = train_batch_size,
            test_batch_size = test_batch_size,
            num_points = num_points,
            num_workers = num_workers,
            gpu = gpu,
            multi_gpu = multi_gpu,
            train_split = train_split,
            test_split = test_split,
            debug = debug,
            dataset = dataset,
            train_data_dir = train_data_dir,
            test_data_dir = test_data_dir,
            num_classes = num_classes,
            in_channels = in_channels,
            visual_dir = visual_dir,
            model_name = model_name
        )
        if debug==True:
            self.train_split='val'
            self.test_split='val'
            self.multi_gpu='0'
            self.train_batch_size=2
            self.test_batch_size=4
            self.print_batch=1
            self.validation = True
        self.exclude_set = exclude_set
        self.exclude_ins = exclude_ins
        self.sample_points = sample_points
        self.compute_normal = compute_normal
        self.trans_xyz = trans_xyz
        self.map_label = map_label
        self.compute_cat_list = compute_cat_list
        self.compute_ins_list = compute_ins_list

class2label = {
    '未知': 0,
    '道路面': 1,
    '房屋建筑类': 2,
    '行道树': 3,
    '树丛': 4,
    '低矮植被': 5,
    '路灯': 6,
    '电力线': 7,
}

class2label_en = {
    'other': 0,
    'ground': 1,
    'buildings': 2,
    'trees': 3,
    'tree': 4,
    'low_veg': 5,
    'lights': 6,
    'wire': 7,
}

sem_map = {
    200900: 0,  #其它
    200200: 0,  # 水体
    0: 0,  # 未知
    200800: 1,  # 道路面
    200000: 1,  # 桥
    200101: 2,  # 房屋建筑类
    200301: 3,  # 行道树
    200400: 4,  # 树丛
    200500: 5,  # 低矮植被
    200601: 6,  # 路灯
    100500: 0, #汽车
    100600: 0, #che
    200700: 7,  # 电力线
}

sem_list_no_ins = [
    200200,  # 水体
    # 200400,  # 树丛
    200500,  # 低矮植被
    200700,  # 电力线
    200800,  # 道路面
    200000,  # 桥
    200900,  #
    0
]

# class_weights = [
#     0.0119779614491877,  # 0, 房屋建筑类
#     0.314668747039018,  # 1, 水体
#     0.0260794516826316,  # 2, 行道树
#     0.0156580261458067,  # 3, 树丛
#     0.0184572604748969,  # 4, 低矮植被
#     0.414290457952274,  # 5, 路灯
#     0.159484337980277,  # 6, 电力线
#     0.0120969382494486,  # 7, 道路面
#     0.027286819026459,  # 8, 其它
# ]

class_weights = [
    0,  # 0, 未知
    0.0199345313845615,  # 1, 道路面
    0.0195447974157289,  # 2, 房屋建筑类
    0.0434312408459997,  # 3, 行道树
    0.0232099513497019,  # 4, 树丛
    0.0312888144801394,  # 5, 低矮植被
    0.696583647384844,  # 6, 路灯
    0.166007017139025,  # 7, 电力线
]


sem_color_map = {
    0: [255,51,104],  # 建筑
    1: [155,194,230],  # 水体
    2: [168,255,63],  # 行道树
    3: [56,255,139],  # 树丛
    4: [61,172,0],  # 低矮植被
    5: [29,250,255],  # 路灯
    6: [51,85,255],  # 电线
    7: [255,199,137],  # 地面
    8: [252,116,197],  # 其它
}

raw_class_label = {
    'bridge': 200000,
    'building': 200101,
    'water': 200200,
    'tree': 200301,
    'veg': 200400,
    'low veg': 200500,
    'light': 200601,
    'electric': 200700,
    'ground': 200800,
    'others': 200900,
    'others2': 0,
    'vehicle': 100500,
    'non vehicle': 100600
}

raw_label_class = {raw_class_label[cls]: cls for cls in raw_class_label.keys()}

seg_label_to_cat = {class2label[i]:i for i in class2label.keys()}
seg_label_to_cat_en = {class2label_en[i]:i for i in class2label_en.keys()}

compute_ins_list = [2, 3, 6]

train_split = ['0040', '0050', '0070', '0080', '0090', '0721', '0814', '0923', '1109', '1205', '1207', '1209', '1225', '1318', '1515', '1519', '1520', '1523', '1615', '1721', '1824', '1917', '2123', '2127', '2321', '2322', '2323', '2325', '2327', '2320', '2421', '2428', '2519', '2525', '2707', '2828', '2911', '2914', '2916', '2919', '2950', '3016', '3024', '3116', '3217', '3724', '3727', '3729', '3730', '3830', '3917', '3922', '4119', '4314', '4315', '4316', '4317', '4929', '4930', '4933']

val_split = []
test_split = ['0020', '0030', '0060', '0813', '1116', '1622', '2222', '2318', '2409', '5033', '2518', '2523', '3322', '3529', '3722', '3728', '4032', '4324', '4725', '5232']


