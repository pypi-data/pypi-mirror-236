from pywhu3d.configs.base_config import BaseConfig

class TorontoConfig(BaseConfig):
    def __init__(
            self,
            debug=False,
            # debug=True,

            num_points=20000,
            size_x=10,
            size_y=10,
            stride=3,
            threshold=500,
            grid_size=0.05,
            normal_radius=0.8,
            exclude_set={}, #{1, 2, 7, 8, 10 ,11, 12, 15, 18},
            sample_points=True,
            compute_normal=True,
            map_label=False,
            trans_xyz=True,

            num_workers=1,
            gpu='0',
            multi_gpu='0, 1, 2, 3',

            train_batch_size=28,
            test_batch_size=128,
            train_split='train',
            test_split='test',
            dataset='toronto',
            train_data_dir='experiment/data/toronto_blocks/10-10_30_20000_9_rot',
            test_data_dir='experiment/data/toronto_blocks/10-10_50_20000_9_rot',
            num_classes=9,
            in_channels=13,  # jsis3d: 9; bonet: 12
            learning_rate=0.001,

            model_name='toronto[0.804]_065_0.7071.pth',# 'mls[0.808]_050_0.4286.pth',
            visual_dir='experiment/pred/visual',
            exclude_ins=[],
            voxel_size = [0.01, 0.002, 0.01],
            compute_cat_list = [1, 2, 3, 4, 5, 6, 7, 8]
    ):
        super(TorontoConfig, self).__init__(
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
            model_name=model_name,
            learning_rate=learning_rate
        )
        if debug==True:
            self.train_split='train'
            self.test_split='test'
            self.multi_gpu='0'
            self.train_batch_size=6
            self.test_batch_size=12
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

class2label_en = {
    "Unclassified": 0,
    "Ground": 1,
    "Road_markings": 2,
    "Natural": 3,
    "Building": 4,
    "Utility_line": 5,
    "Pole": 6,
    "Car": 7,
    "Fence": 8,
}

sem_map = {i:i for i in range(9)}

pred_map = {
    0: 0,  # mean
    1: 3,  # tree
    2: 1,  # nd.way
    3: 4,  # building
    4: 0,  # box
    5: 6,  # light
    6: 6,  # tel.pole
    7: 6,  # mun.pole
    8: 3,  # low veg.
    9: 6,  # board
    10: 1,  # drveway
    11: 2,  # roadmark
    12: 7,  # car
    13: 0,  # person
    14: 6,  # sig.light
    15: 6,  # detector
    16: 8,  # fence
    17: 5,  # wire
}


sem_list_no_ins = []

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
    10: [155, 194, 230],  # road way
    11: [255, 255, 0],  # road mark
    12: [137, 255, 182],  # car
    13: [242, 135, 110],  # person
    14: [255, 75, 75],  # signal light
    15: [255, 224, 109],  # detector
    16: [228, 93, 255],  # fence
    17: [109, 172, 255],  # wire
}

seg_label_to_cat_en = {class2label_en[i]:i for i in class2label_en.keys()}

class_weights_equal = [
    0,  # 0, others
    1,  # 1, tree
    1,  # 2, non-drive
    1,  # 3, building
    1,  # 4, box
    1,  # 5, light
    1,  # 6, ele. pole
    1,  # 7, mul. Pole
    1,  # 8, low veg.
]

class_weights_sqrt = [
    0,  # Unclassified, 0
    0.0414102524819797,  # Ground, 1
    0.225873553474242,  # Road_markings, 2
    0.0410840483452024,  # Natural, 3
    0.0400506907790686,  # Building, 4
    0.218114771419714,  # Utility_line, 5
    0.163884410294735,  # Pole, 6
    0.10460111670147,  # Car, 7
    0.164981156503588,  # Fence, 8
]
