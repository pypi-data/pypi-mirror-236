from pywhu3d.configs.base_config import BaseConfig

class MLSInsConfig(BaseConfig):
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
            map_label=True,
            trans_xyz=True,
            compute_bbox=True,

            num_workers=0,
            gpu='0',
            multi_gpu='0, 1, 2, 3',

            train_batch_size=8,
            test_batch_size=32,
            train_split='train',
            test_split='test',
            dataset='mls',
            train_data_dir='experiment/data/mls_blocks/20-20_100_60000_18_box',
            test_data_dir='experiment/data/mls_blocks/20-20_100_60000_18_box',
            num_classes=18,
            in_channels=10,  # jsis3d: 9; bonet: 12

            model_name='mls[0.669]_079_0.5296.pth',
            # model_name = 'mls[0.808]_050_0.4286.pth',
            # model_name='temp_49.pth',# 'mls[0.808]_050_0.4286.pth',
            visual_dir='experiment/pred/visual',
            exclude_ins=[],
            voxel_size = [0.01, 0.002, 0.01],
            compute_cat_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    ):
        super(MLSInsConfig, self).__init__(
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
            self.train_split='val'
            self.test_split='val'
            self.multi_gpu='0'
            self.train_batch_size=6
            self.test_batch_size=50
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

class2label = {
    '其它': 0,  # '其它街道家具',
    '树木': 1,  # '树木1',
    '非机动道': 2,  # '地面(非道路)',
    '房屋建筑': 3,  # '房屋建筑类',
    '箱状地物': 4,  # '箱状地物',
    '路灯': 5,  # '路灯',
    '电线杆': 6,  # '电线杆',
    '市政立杆': 7,  # '市政立杆',
    '低矮植被': 8,  # '低矮植被',
    '提示牌': 9,  # '附属提示牌',
    '机动车道': 10,
    '道路标线': 11,  # '道路标线',
    '机动车': 12,  # '机动车',
    '行人': 13,  # '行人',
    '信号灯': 14,  # '信号灯',
    '独立探头': 15,  # '独立探头',
    '围栏': 16,  # '围墙/栅栏',
    '电线': 17,  # '电线',
} # 23t

class2label_en = {
    'others': 0,  # '其它街道家具',
    'tree': 1,  # '树木1',
    'nd.way': 2,  # '地面(非道路)',
    'building': 3,  # '房屋建筑类',
    'box': 4,  # '箱状地物',
    'light': 5,  # '路灯',
    'tel.pole': 6,  # '电线杆',
    'mun.pole': 7,  # '市政立杆',
    'low veg.': 8,  # '低矮植被',
    'board': 9,  # '附属提示牌',
    'drveway': 10,
    'roadmark': 11,  # '道路标线',
    'car': 12,  # '机动车',
    'person': 13,  # '行人',
    'sig.light': 14,  # '信号灯',
    'detector': 15,  # '独立探头',
    'fence': 16,  # '围墙/栅栏',
    'wire': 17,  # '电线',
} # 23

sem_map = {
    101801: 0,  # '其它街道家具',
    100901: 0,  # '消防栓',
    100200: 0,  # '景观建筑类',
    100951: 0,  # '接头座椅', few
    101701: 0,  # '独立棚子', few
    100700: 0,  # '石墩', few
    100851: 0,  # '邮筒', few
    105600: 0,  # '公交站台', few
    105500: 0,  # '公交站牌',
    100300: 1,  # '树木1',
    102000: 1,  # '树木2',
    106100: 2,  # '地面(非道路)'
    102600: 2,  # '非机动车道',
    200000: 2,  # '立交桥', few
    104002: 2,  # '井盖',
    100100: 3,  # '房屋建筑类',
    105400: 4,  # '箱状地物',
    100801: 4,  # '垃圾桶'
    101100: 5,  # '路灯',
    101300: 5,  # '路灯附属物', none
    101200: 6,  # '电线杆',
    101400: 6,  # '电线杆附属物', few
    105200: 7,  # '市政立杆',
    106200: 8,  # '低矮植被',
    101600: 8,  # '花坛',
    101500: 9,  # '附属提示牌',
    100400: 9,  # '独立提示牌',
    102400: 10,  # '机动车道',
    104202: 11,  # '道路标线',
    100500: 12,  # '机动车',
    100600: 13,  # '行人',
    105100: 14,  # '信号灯',
    105300: 15,  # '独立探头',
    105800: 16,  # '围墙/栅栏',
    102800: 16,  # '道路隔离结构',
    105700: 17,  # '电线',
    102200: 17,  # '输电线', none
}  # 23 map0+22

pred_map = {
    0: 0,  # mean
    1: 3,  # tree
    2: 5,  # nd.way
    3: 4,  # building
    4: 6,  # box
    5: 2,  # light
    6: 2,  # tel.pole
    7: 2,  # mun.pole
    8: 3,  # low veg.
    9: 2,  # board
    10: 5,  # drveway
    11: 5,  # roadmark
    12: 1,  # car
    13: 1,  # person
    14: 2,  # sig.light
    15: 2,  # detector
    16: 4,  # fence
    17: 6,  # wire
}

sem_list_no_ins = [
    106100,  # '地面(非道路)'
    102400,  # '机动车道',
    102600,  # '非机动车道',
    200000,  # '立交桥', few
    102000,  # '树木2',
    106200,  # '低矮植被',104202
    102800,  # '道路隔离结构',
    105700,  # '电线',
    102200,  # '输电线', none
    105800,  # '围墙/栅栏',
    104202,  # '道路标线'
]  # 10

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

seg_label_to_cat = {class2label[i]:i for i in class2label.keys()}
seg_label_to_cat_en = {class2label_en[i]:i for i in class2label_en.keys()}

class_weights_sqrt = [
    0,  # 0, others
    0.00442042603746903,  # 1, tree
    0.00788553815197419,  # 2, non-drive
    0.00795507663390606,  # 3, building
    0.0904974283300982,  # 4, box
    0.0522849910726537,  # 5, light
    0.0632030143491199,  # 6, ele. pole
    0.317510566025372,  # 7, mul. Pole
    0.0085867841797682,  # 8, low veg.
    0.0580646171674088,  # 9, board
    0.00527579991344002,  # 10, drive way
    0.0239440421864183,  # 11, road mark
    0.0185819803136484,  # 12, car
    0.038379671009933,  # 13, person
    0.0774300654685609,  # 14, signal light
    0.111380036086574,  # 15, detector
    0.00913314160871165,  # 16, fence
    0.105466821464944,  # 17, wire
]

class_weights_self = [
    0,  # 0, others
    0.000129107225941079,  # 1, tree
    0.000410851585842462,  # 2, non-drive
    0.000418129711198501,  # 3, building
    0.0541121474197982,  # 4, box
    0.0180624380038002,  # 5, light
    0.0263935541607813,  # 6, ele. pole
    0.666098809491873,  # 7, mul. Pole
    0.000487173198665358,  # 8, low veg.
    0.0222764215152827,  # 9, board
    0.000183907281987896,  # 10, drive way
    0.00378806333008921,  # 11, road mark
    0.00228142546262147,  # 12, car
    0.0097325084253582,  # 13, person
    0.03961334770691,  # 14, signal light
    0.0819666152487537,  # 15, detector
    0.000551140944144272,  # 16, fence
    0.0734943592869527,  # 17, wire
]

class_weights_log = [
    0,  # 0, others
    0.0451401595365353,  # 1, tree
    0.0482054207110109,  # 2, non-drive
    0.0482551267896083,  # 3, building
    0.0675429958914057,  # 4, box
    0.0619555880078412,  # 5, light
    0.0637794045416749,  # 6, ele. pole
    0.0851027012602898,  # 7, mul. Pole
    0.0486921043754787,  # 8, low veg.
    0.0629508160124659,  # 9, board
    0.0460347972409256,  # 10, drive way
    0.055428181071744,  # 11, road mark
    0.0535951700233719,  # 12, car
    0.0591958408835442,  # 13, person
    0.065854784240188,  # 14, signal light
    0.0699297611349296,  # 15, detector
    0.049050671390639,  # 16, fence
    0.0692864768883472,  # 17, wire
]

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
    1,  # 9, board
    1,  # 10, drive way
    1,  # 11, road mark
    1,  # 12, car
    1,  # 13, person
    1,  # 14, signal light
    1,  # 15, detector
    1,  # 16, fence
    1,  # 17, wire
]

class_weights_sqrt_propotion = [
    0.11163367694025,  # 0, 非机动道
    0.205226076586278,  # 1, 树木
    0,  # 2, 其它
    0.110445434724751,  # 3, 房屋建筑
    0.00885023144574412,  # 4, 箱状地物
    0.0163114630151858,  # 5, 路灯
    0.0148931072128632,  # 6, 电线杆
    0.00285262410543068,  # 7, 市政立杆
    0.0996754197605567,  # 8, 低矮植被
    0.0117359227284106,  # 9, 提示牌
    0.171013074983018,  # 10, 机动车道
    0.0437117719660744,  # 11, 道路标线
    0.0444194097200408,  # 12, 机动车
    0.0318959992302314,  # 13, 行人
    0.0112090342398216,  # 14, 信号灯
    0.00570612974844045,  # 15, 独立探头
    0.00216479033196609,  # 16, 公交站牌
    0.0100222457645885,  # 17, 电线
    0.0982335874963487,  # 18, 围栏
]

raw_label_class = {
    101801: '其它街道家具',
    100901: '消防栓',
    100200: '景观建筑类',
    100951: '接头座椅', 
    101701: '独立棚子', 
    100700: '石墩', 
    100851: '邮筒', 
    105600: '公交站台', 
    105500: '公交站牌',
    100300: '树木1',
    102000: '树木2',
    106100: '地面(非道路)',
    102600: '非机动车道',
    200000: '立交桥', 
    104002: '井盖',
    100100: '房屋建筑类',
    105400: '箱状地物',
    100801: '垃圾桶',
    101100: '路灯',
    101300: '路灯附属物', 
    101200: '电线杆',
    101400: '电线杆附属物', 
    105200: '市政立杆',
    106200: '低矮植被',
    101600: '花坛',
    101500: '附属提示牌',
    100400: '独立提示牌',
    102400: '机动车道',
    104202: '道路标线',
    100500: '机动车',
    100600: '行人',
    105100: '信号灯',
    105300: '独立探头',
    105800: '围墙/栅栏',
    102800: '道路隔离结构',
    105700: '电线',
    102200: '输电线', 
}

raw_class_label = {raw_label_class[label]: label for label in raw_label_class.keys()}


