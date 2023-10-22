from pywhu3d.configs.base_config import BaseConfig

class ParisInsConfig(BaseConfig):
    def __init__(
            self,
            debug=False,
            # debug=True,

            num_points=60000,
            size_x=20,
            size_y=20,
            stride=10,
            threshold=500,
            grid_size=0.05,
            normal_radius=0.8,
            exclude_set={}, #{1, 2, 7, 8, 10 ,11, 12, 15, 18},
            sample_points=True,
            compute_normal=True,
            map_label=False,
            trans_xyz=True,
            compute_bbox=True,

            num_workers=0,
            gpu='0',
            multi_gpu='0, 1, 2, 3',

            train_batch_size=8,
            test_batch_size=32,
            train_split='train',
            test_split='test',
            dataset='paris',
            train_data_dir='experiment/data/paris_blocks/20-20_100_60000_10_sem',
            test_data_dir='experiment/data/paris_blocks/20-20_100_60000_10_sem',
            num_classes=10,
            in_channels=10,  # jsis3d: 9; bonet: 12

            model_name='paris[0.641]_061_0.5202.pth',
            # model_name = 'mls[0.808]_050_0.4286.pth',
            # model_name='temp_49.pth',# 'mls[0.808]_050_0.4286.pth',
            visual_dir='experiment/pred/visual',
            exclude_ins=[],
            voxel_size = [0.01, 0.002, 0.01],
            # compute_cat_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            compute_cat_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ):
        super(ParisInsConfig, self).__init__(
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
            visual_dir=visual_dir,
            model_name=model_name
        )
        if debug==True:
            self.train_split='test'
            self.test_split='test'
            self.multi_gpu='0'
            self.train_batch_size=2
            self.test_batch_size=16
            self.print_batch=1
            self.validation = True
        self.exclude_set = exclude_set
        self.exclude_ins = exclude_ins
        self.sample_points = sample_points
        self.compute_normal = compute_normal
        self.trans_xyz = trans_xyz
        self.map_label = map_label
        self.voxel_size = voxel_size
        self.compute_cat_list = compute_cat_list
        self.compute_bbox = compute_bbox

# class2label = {
#     'uncified': 0,
#     'other': 1,
#     'vegetation': 2,
#     'road': 3,
#     'building': 4,
#     'punctual object': 5,
#     'extended': 6,
#     'pedestrian': 7,
#     '4+ wheelers': 8,
#     'natural': 9,
#     'potted plant': 10,
#     'sidewalk': 11,
#     'linear': 12,
#     'furniture': 13,
#     'tree': 14,
#     'island': 15,
#     '2 wheelers': 16,
# }  # 17

class2label = {
    'others': 0,
    'gournd': 1,
    'building': 2,
    'pole': 3,
    'bollard': 4,
    'trash cna': 5,
    'barrier': 6,
    'pedestrian': 7,
    'car': 8,
    'natural': 9,
}

class2label_en = class2label

sem_map = {
    0: 0,  # uncified
    100000000: 1,  # other
    202060000: 2,  # vegetation
    202020000: 3,  # road
    203000000: 4,  # building
    302020000: 5,  # punctual object
    302040000: 6,  # extended
    303020000: 7,  # pedestrian
    303040000: 8,  # 4+ wheelers
    304000000: 9,  # natural
    304040000: 10,  # potted plant
    202030000: 11,  # sidewalk
    302030000: 12,  # linear
    303050000: 13,  # furniture
    304020000: 14,  # tree
    202050000: 15,  # island
    303030000: 16,  # 2 wheelers
}  # 17

sem_map_10 = {
    0: 0,  # other
    100000000: 0,  # other
    202020000: 1,  # ground
    202030000: 1,  # ground
    202050000: 1,  # ground
    202060000: 1,  # ground
    203000000: 2,  # building
    302020200: 3,  # signage
    302020300: 4,  # bollard
    302020400: 3,  # signage
    302020500: 3,  # signage
    302020600: 3,  # signage
    302020700: 0,  # signboard
    302020800: 0,  # mailbox
    302020900: 5,  # trash can
    302021000: 0,  # other
    302021100: 0,  # other
    302021200: 0,  # other
    302021300: 0,  # other
    302030200: 6,  # barrier
    302030300: 6,  # barrier
    302030600: 0,  # wire/other
    302030700: 6,  # barrier
    302040200: 0,  # other
    302040500: 0,  # bench/other
    302040600: 0,  # other
    302040700: 2,  # building
    302040800: 0,  # other
    303020000: 7,  # pedestrian
    303030204: 0,  # bicycle/other
    303030302: 0,  # other
    303030304: 0,  # other
    303030502: 0,  # other
    303030504: 0,  # other
    303040202: 8,  # car
    303040203: 8,  # car
    303040204: 8,  # car
    303040302: 8,  # car
    303040304: 8,  # car
    303040403: 0,  # truck/other
    303040404: 0,  # truck/other
    303040503: 0,  # bus/other
    303040504: 0,  # bus/other
    303050200: 0,  # furniture/other
    303050300: 0,  # furniture/other
    303050500: 5,  # trash can/furniture
    303050600: 0,  # other
    304000000: 9,  # natural
    304020000: 9,  # natural
    304040000: 0,  # potted plant/other
}


sem_list_no_ins = [
    100000000,
    302020700,
    302020800,
    302021000,
    302021100,
    302021200,
    302021300,
    302030600,
    302040200,
    302040500,
    302040600,
    302040800,
    303030204,
    303030302,
    303030304,
    303030502,
    303030504,
    303040403,
    303040404,
    303040503,
    303040504,
    303050200,
    303050300,
    303050600,
    304040000,
    202020000,
    202030000,
    202050000,
    202060000,
]


seg_label_to_cat = {class2label[i]:i for i in class2label.keys()}
seg_label_to_cat_en = {class2label_en[i]:i for i in class2label_en.keys()}

class_weights_sqrt = [
    0,  #others
    0.276827129106778,  #gournd
    0.295996424455306,  #building
    0.0338078951685493,  #pole
    0.00950751184780346,  #bollard
    0.0222120704153731,  #trash cna
    0.0765159283278342,  #barrier
    0.0145225887199216,  #pedestrian
    0.0714482167077008,  #car
    0.199162235250733,  #natural
]


class_weights_equal = [
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    # 1,
    # 1,
    # 1,
    # 1,
    # 1,
    # 1,
    # 1,
]

sem_color_map = {
    0: [220, 220, 220],  # others
    1: [168, 255, 63],  # tree
    2: [255, 199, 137],  # non-roadway
    3: [255, 51, 104],  # building
    4: [180, 167, 255],  # box
    5: [29, 250, 255],  # light
    6: [252, 116, 197],  # tel. pole
    7: [242, 239, 103],  # small pole
    8: [61, 172, 0],  # low veg.
    9: [255, 143, 51],  # board
    # 10: [155, 194, 230],  # road way
    # 11: [255, 255, 0],  # road mark
    # 12: [137, 255, 182],  # car
    # 13: [242, 135, 110],  # person
    # 14: [255, 75, 75],  # signal light
    # 15: [255, 224, 109],  # detector
    # 16: [228, 93, 255],  # fence
    # 17: [109, 172, 255],  # wire
}

