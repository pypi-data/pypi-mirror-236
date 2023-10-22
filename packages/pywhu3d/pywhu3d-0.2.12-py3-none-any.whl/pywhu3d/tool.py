import ntpath

import numpy as np
import os, h5py, sys
import open3d as o3d
from laspy.file import File
import plyfile as ply

from rich.console import Console
console = Console(soft_wrap=True)
print = console.print
input = console.input
rule = Console(soft_wrap=True, width=100).rule
from rich.progress import track
from rich.table import Column, Table
from rich.text import Text
import json
from rich.progress import Progress
pprint = Progress().console.print
# from configs.mls_config_pole import MLSInsConfig as Config, sem_list_no_ins, sem_map, class2label, raw_class_label, sem_color_map


def newpath(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        yn = input('[red][italic]%s[/] folder already exists, still process (\[y]/n)?' % path)
        if yn == 'n':
            return False
        else:
            return True

def sample_cloud(cloud, num_samples):
    n = cloud.shape[0]
    if n >= num_samples:
        indices = np.random.choice(n, num_samples, replace=False)
    else:
        indices = np.random.choice(n, num_samples - n, replace=True)
        indices = list(range(n)) + list(indices)
    sampled = cloud[indices, :]
    return sampled

def save_h5_blocks(fname, cloud, num_points, size_x=10, size_y=10, stride=5, threshold=100, show_points=False, config=None):
    # input: x, y, z, n1, n2, n3, intn, sem, ins
    # cloud[:, 0:3] *= 200
    # cloud[:, 3:6] /= 255.0
    xyz = cloud['xyz']
    features = cloud['features']
    labels = cloud['labels']
    limit = np.amax(xyz, axis=0)
    # width = int(np.ceil((limit[0] - size_x) / stride)) + 1
    # depth = int(np.ceil((limit[1] - size_y) / stride)) + 1
    width = max(int(np.ceil((limit[0] - size_x) / stride)), 0) + 1
    depth = max(int(np.ceil((limit[1] - size_y) / stride)), 0) + 1
    cells = [(x * stride, y * stride) for x in range(width) for y in range(depth)]
    blocks = []

    ########################################
    # compute_bounding_box
    bbox = np.zeros((xyz.shape[0], 6))
    ins = labels[..., 1]
    xyz_l = xyz / limit
    for i in list(set(ins)):
        bbox[ins == i, :3] = xyz_l[ins == i].mean(axis=0)
        bbox[ins == i, 3:6] = xyz_l[ins == i].max(axis=0) - xyz_l[ins == i].min(axis=0)
    ##################################

    points = np.concatenate([xyz, labels, bbox, features], axis=-1)


    for (x, y) in cells:
        xcond = (xyz[:, 0] <= x + size_x) & (xyz[:, 0] >= x)
        ycond = (xyz[:, 1] <= y + size_y) & (xyz[:, 1] >= y)
        cond = xcond & ycond
        sem_list = set(labels[cond, 0])
        if np.sum(cond) < threshold:
            # pcd = o3d.geometry.PointCloud()
            # pcd.points = o3d.utility.Vector3dVector(cloud[cond, :3])
            # o3d.visualization.draw_geometries([pcd])
            continue
        if sem_list.issubset(config.exclude_set):
            print(sem_list)
            # num_exclude = num_exclude + 1
            continue
        block = sample_cloud(points[cond, :], num_points)
        blocks.append(block)
    blocks = np.stack(blocks, axis=0)
    xyz = blocks[..., :3]
    labels = blocks[..., 3:5]
    bbox = blocks[..., 5:11]
    features = blocks[..., 11:]
    num_blocks = blocks.shape[0]
    batch = np.zeros((num_blocks, num_points, 6))

    bbox_in = np.zeros((num_blocks, num_points, 6))
    bbox_norm = np.zeros((num_blocks, num_points, 6))

    for b in range(num_blocks):
        minx = min(xyz[b, :, 0])
        miny = min(xyz[b, :, 1])
        batch[b, :, 0] = xyz[b, :, 0] - (minx + size_x * 0.5)
        batch[b, :, 1] = xyz[b, :, 1] - (miny + size_y * 0.5)
        batch[b, :, 2] = xyz[b, :, 2]
        batch[b, :, 3] = xyz[b, :, 0] / limit[0]
        batch[b, :, 4] = xyz[b, :, 1] / limit[1]
        batch[b, :, 5] = xyz[b, :, 2] / limit[2]

        ########################################
        # compute_bounding_box
        ins = labels[b, :, 1]
        for i in list(set(ins)):
            bbox_norm[b, ins==i, :3] = batch[b, ins == i, 3:6].mean(axis=0)
            bbox_norm[b, ins==i, 3:6] = batch[b, ins == i, 3:6].max(axis=0) - batch[b, ins == i, 3:6].min(axis=0)
            bbox_in[b, ins==i, :3] = batch[b, ins == i, :3].mean(axis=0)
            bbox_in[b, ins==i, 3:6] = batch[b, ins == i, :3].max(axis=0) - batch[b, ins == i, :3].min(axis=0)
        ##################################


    points = np.concatenate([batch, features], axis=-1)

    if show_points:
        pcd = o3d.geometry.PointCloud()
        num_cloud = batch.shape[0]
        pcd.points = o3d.utility.Vector3dVector(batch[int(num_cloud / 5), :, :3])
        o3d.visualization.draw_geometries([pcd])
        pcd.points = o3d.utility.Vector3dVector(batch[int(num_cloud / 2), :, :3])
        o3d.visualization.draw_geometries([pcd])

    # points:
    # 0,1,2: block centered xy & z
    # 3,4,5: room normalized xyz
    #6, ...: features
    fp = h5py.File(fname, 'w')
    fp.create_dataset('coords', data=xyz, compression='gzip', dtype='float32')
    fp.create_dataset('points', data=points, compression='gzip', dtype='float32')
    fp.create_dataset('bbox', data=bbox, compression='gzip', dtype='float32')
    fp.create_dataset('bbox_norm', data=bbox_norm, compression='gzip', dtype='float32')
    fp.create_dataset('bbox_in', data=bbox_in, compression='gzip', dtype='float32')
    fp.create_dataset('labels', data=labels, compression='gzip', dtype='int64')
    fp.close()

    if True in np.isnan(points):
        ss = 'wrong'
    else:
        ss = 'right'
    print('%s: %f %f %s' % (fname, points[..., 0:2].min(), points[..., 0:2].max(), ss))


def save_ply(path, points, dtype):
    '''
    points: (N, C)
    dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('scalar_sem', 'u4'), ('scalar_pred', 'u4')]
    '''
    vertex = np.array([tuple(points[i]) for i in range(points.shape[0])], dtype=dtype)
    el = ply.PlyElement.describe(vertex, 'vertex')
    data = ply.PlyData([el], text=False)
    data.write(path)


import numpy as np
from scipy import stats
def block_merge(coords, pred, shape):
    stride = 1 / shape
    semantic = np.ones(shape + 1) * -1
    instance = np.ones(shape + 1) * -1
    semantic = semantic.astype(np.int32)
    instance = instance.astype(np.int32)

    batch_size = coords.shape[0]
    npoints = coords.shape[1]
    coords = coords / stride

    merge_map = {'label': [], 'modes': []}
    for b in range(batch_size):
        xyz, labels = coords[b, ...].astype(np.float32), pred[b, ...].astype(np.int32)
        xyz = xyz.astype(np.int32)
        num_points = xyz.shape[0]

        k = np.amax(labels[:, 1]) + 1
        overlap = np.zeros([k, 1000])
        # find label for each group
        modes = {}
        sizes = {}
        for gid in range(k):
            indices = (labels[:, 1] == gid)
            mode = stats.mode(labels[indices, 0])[0]
            try:
                modes[gid] = int(mode)
            except:
                breakpoint()
            sizes[gid] = np.sum(indices)
        for i in range(num_points):
            x, y, z = xyz[i]
            gid = labels[i, 1]
            if instance[x, y, z] >= 0 and semantic[x, y, z] == modes[gid]:
                overlap[gid, instance[x, y, z]] += 1
        label = np.argmax(overlap, axis=1)
        n = np.amax(instance)
        for gid in range(k):
            count = np.amax(overlap[gid])
            if count < 7 and sizes[gid] > 30:
                n += 1
                label[gid] = n
        for i in range(num_points):
            x, y, z = xyz[i]
            gid = labels[i, 1]
            if gid >= 0 and instance[x, y, z] < 0:
                instance[x, y, z] = label[gid]
                semantic[x, y, z] = modes[gid]
        merge_map['label'].append({i: l for i, l in enumerate(label)})
        merge_map['modes'].append(modes)

    coords = coords.astype(np.int32)
    for b in range(batch_size):
        for i in range(npoints):
            x, y, z = coords[b, i]
            pred[b, i, 0] = semantic[x, y, z]
            pred[b, i, 1] = instance[x, y, z]
            # pred[b, i, 1] = x * 100 + y * 10 + z
    return pred


class WHU3D:
    def __init__(self,  data_root, data_type, format, scenes=[]):
        '''
        data_root: where is the data
        data_type: als, mls, image
        format: txt, ply, npy, h5, pickle
        [optional] scenes: a list of scenes
        '''
        self.data_root = data_root
        self.data_path = os.path.join(data_root, data_type)
        self.data_type = data_type
        self.format = format
        self.scenes = scenes
        self.data = {}
        self.labels = {}
        self.gt = {}
        try:
            if format == 'txt':
                self.load_txt(os.path.join(data_root, data_type, 'txt'))
            elif format == 'h5':
                self.load_h5(os.path.join(data_root, data_type, 'h5'))
        except:
            print('[red]Unknown Loading Error!')

        if data_type == 'mls':
            from pywhu3d.configs.mls_config_pole import sem_list_no_ins, sem_map, raw_label_class, seg_label_to_cat_en, compute_ins_list, train_split, test_split, val_split, MLSInsConfig
            self.config = MLSInsConfig()
        elif data_type == 'mls-w':
            from pywhu3d.configs.mls_w_config import sem_list_no_ins, sem_map, raw_label_class, seg_label_to_cat_en, compute_ins_list, train_split, test_split, val_split, MLSInsConfig
            self.config = MLSInsConfig()
        elif data_type == 'als':
            from pywhu3d.configs.als_config import sem_list_no_ins, sem_map, raw_label_class, seg_label_to_cat_en, compute_ins_list, train_split, val_split, test_split, ALSInsConfig
            self.config = ALSInsConfig()

        self.sem_list_no_ins = sem_list_no_ins
        self.sem_map = sem_map
        self.label2cat = raw_label_class
        self.gt2cat = seg_label_to_cat_en
        self.num_classes = len(self.gt2cat)
        self.compute_ins_list = compute_ins_list
        self.train_split = train_split
        self.test_split = test_split
        self.val_split = val_split

        self.interpreted = False
        self.with_normal = False
        self.normed = False
        self.divided = False
        self.sampled = False

        print('Num of scenes: %d' % len(self.scenes))

    def load_txt(self, input):
        flist = [f for f in os.listdir(input) if not f.startswith('.')]
        load_scenes = [scene.split('.')[0] for scene in flist] if len(self.scenes) == 0 else self.scenes
        self.scenes = []
        for scene in track(load_scenes, description='[cyan]loading txt data...'):
            pprint('processing %s...' % scene)
            points = np.loadtxt(os.path.join(input, scene + '.txt'), delimiter=' ')
            if self.data_type == 'mls':
                if points.shape[-1] == 11:
                    x, y, z, aa, bb, intensity, sem, ins, r, g, b = np.split(points, points.shape[1], axis=1)
                    return_num = aa if aa.max() == 3 else bb
                    # pprint('[grey]#return: %.1f, time: %.1f, intensity: %.1f' % (return_num.max(), pts_time.max(), intensity.max()))
                elif points.shape[-1] == 12:
                    x, y, z, edge, return_num, pts_time, intensity, sem, ins, r, g, b = np.split(points, points.shape[1], axis=1)
                    # pprint('[grey]#edge: %.1f, #return: %.1f, time: %.1f, intensity: %.1f' % (edge.max(), return_num.max(), pts_time.max(), intensity.max()))
                else:
                    pprint('[orange1][Warning: loaded features number wrong!] passing %s' % scene)
                    continue
                pprint('[bright_black]#return: %.1f, intensity: %.1f' % (return_num.max(), intensity.max()))
                self.data[scene] = {}
                self.labels[scene] = {}
                self.data[scene]['number_returns'] = return_num.squeeze()
                self.data[scene]['intensity'] = intensity.squeeze()
            elif self.data_type == 'mls-w':
                x, y, z, intensity, return_num, sem, ins = np.split(points, points.shape[1], axis=1)
                self.data[scene] = {}
                self.labels[scene] = {}
                self.data[scene]['number_returns'] = return_num.squeeze()
                self.data[scene]['intensity'] = intensity.squeeze()
            elif self.data_type == 'als':
                x, y, z, sem, ins, r, g, b = np.split(points, points.shape[1], axis=1)
                self.data[scene] = {}
                self.labels[scene] = {}
            self.data[scene]['coords'] = np.concatenate([x, y, z], axis=-1)
            self.labels[scene]['semantics'] = sem.squeeze()
            self.labels[scene]['instances'] = ins.squeeze()
            self.scenes.append(scene)

    def load_h5(self, input):
        flist = [f for f in os.listdir(input) if not f.startswith('.')]
        if len(self.scenes) == 0:
            self.scenes = [scene.split('.')[0] for scene in flist]
        feature_keys = None
        ignore_feats = ['coords', 'semantics', 'instances']
        for scene in track(self.scenes, description='[cyan]loading h5 data...'):
            pprint('processing %s...' % scene)
            fin = h5py.File(os.path.join(input, scene + '.h5'), 'r')
            if feature_keys is None:
                feature_keys = list(fin)
                for feat in ignore_feats:
                    feature_keys.remove(feat)
            ignore_feats = []
            self.data[scene] = {}
            self.labels[scene] = {}
            self.data[scene]['coords'] = fin['coords'][:]
            self.labels[scene]['semantics'] = fin['semantics'][:]
            self.labels[scene]['instances'] = fin['instances'][:]
            for at in feature_keys:
                if at not in list(fin):
                    print('[orange1]Warning1: it seems that the files have different features!')
                    print('[orange1]Warning2: there is no %s in %s' % (at, scene))
                    print('[orange1]Warning3: \'%s\' of the first scene and the following scenes will be removed automatically' % at)
                    self.data[self.scenes[0]].pop(at)
                    ignore_feats.append(at)
                    continue
                self.data[scene][at] = fin[at][:]
            # self.data[scene]['number_returns'] = fin['number_returns'][:]
            # self.data[scene]['edge_flight_line'] = fin['edge_flight_line'][:]
            # self.data[scene]['intensity'] = fin['intensity'][:]

            for feat in ignore_feats:
                feature_keys.remove(feat)
            ignore_feats = []

    def export_las(self):
        pass

    def export_label(self):
        pass

    def export_ply(self, output_dir='', scenes=[]):
        if output_dir == '':
            output_dir = os.path.join(self.data_path, 'ply')
        if len(scenes) == 0:
            scenes = self.scenes

        if not newpath(output_dir):
            print('Exit processing...')
            return

        attrs_v = self.return_feature_keys()

        dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4'), ('scalar_sem', 'u4'), ('scalar_ins', 'u4')]

        for at in attrs_v:
            dtype.append(('scalar_'+at, 'f4'))

        self.interprete_labels()

        for scene in track(scenes, description='[cyan]export ply to %s...' % output_dir):
            pprint('processing %s...' % scene)
            fname = os.path.join(output_dir, scene + '.ply')
            coords = self.data[scene]['coords']
            sem = self.gt[scene]['semantics'][:,None]
            ins = self.gt[scene]['instances'][:,None]
            points = [coords, sem, ins]
            for at in attrs_v:
                points.append(self.data[scene][at][:,None])
            save_ply(fname, np.concatenate(points, 1), dtype)

        print('\n[green]Exported all %d files.' % len(self.scenes))

    def return_feature_keys(self):
        '''
        :return: a list of feature keys.
        '''
        attrs = self.list_attributes(False)
        attrs_v = [at.split('/')[-1] for at in attrs if at.split('/')[0] == 'data']
        attrs_v.remove('coords')
        return attrs_v


    def export_h5(self, output_dir='', scenes=[]):
        if output_dir == '':
            output_dir = os.path.join(self.data_path, 'h5')
        if len(scenes) == 0:
            scenes = self.scenes

        if not newpath(output_dir):
            print('Exit processing...')
            return

        attrs_v = self.return_feature_keys()

        for scene in track(scenes, description='[cyan]export h5 to %s...' % output_dir):
            pprint('processing %s...' % scene)
            fname = os.path.join(output_dir, scene + '.h5')
            fp = h5py.File(fname, 'w')
            fp.create_dataset('coords', data=self.data[scene]['coords'], compression='gzip', dtype='float64')
            for at in attrs_v:
                fp.create_dataset(at, data=self.data[scene][at], compression='gzip', dtype='float64')
            fp.create_dataset('semantics', data=self.labels[scene]['semantics'], compression='gzip', dtype='int64')
            fp.create_dataset('instances', data=self.labels[scene]['instances'], compression='gzip', dtype='int64')
        print('\n[green]Exported all %d files.' % len(self.scenes))

    def load_label(self):
        pass

    def load_full_mls(self):
        pass

    def load_full_als(self):
        pass

    def vis(self, scene, type, color=None, sample_ratio=0.01):
        if type == 'pc':
            xyz = self.data[scene]['coords']
            num_points = xyz.shape[0]
            idx = np.random.choice(num_points, int(num_points * sample_ratio), replace=False)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(xyz[idx])
            o3d.visualization.draw_geometries([pcd])

    def remote_vis(self):
        pass

    def evaluation(self):
        pass

    def sample_points(self, sample_ratio):
        if self.sampled:
            print('[orange1][warning]Points have been sampled and it will be passed')
            return
        attrs = self.list_attributes(False)
        attrs_v = {at.split('/')[0]: {} for at in attrs}
        for k, at_v in attrs_v.items():
            attrs_v[k] = {scene: {} for scene in self.scenes}
        for scene in track(self.scenes, description='[cyan]sampling points...'):
            xyz = self.data[scene]['coords']
            num_points = xyz.shape[0]
            idx = np.random.choice(num_points, int(num_points * sample_ratio), replace=False)
            for at in attrs:
                at1, at2 = at.split('/')
                at_v = getattr(self, at1)[scene][at2]
                assert at_v.shape[0] == num_points
                attrs_v[at1][scene][at2] = at_v[idx]
            pprint('%s is sampled: %d -> %d' %(scene, num_points, num_points*sample_ratio))

        for k, at_v in attrs_v.items():
            setattr(self, k, at_v)

        self.sampled = True



    def compute_normals(self, radius=0.8):
        if self.with_normal:
            print('[orange1][warning]Normals have been computed and it will be passed')
            return
        for scene in track(self.scenes, description='[cyan]computing normals...'):
            pprint('processing %s...' % scene)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(self.data[scene]['coords'])

            pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=radius, max_nn=50))
            nx, ny, nz = np.split(np.asarray(pcd.normals), 3, 1)
            self.data[scene]['nx'] = nx.squeeze()
            self.data[scene]['ny'] = ny.squeeze()
            self.data[scene]['nz'] = nz.squeeze()

        self.with_normal = True


    def norm_coords(self):
        if self.normed:
            print('[orange1][warning]Coords have been normed and it will be passed')
            return
        for scene in track(self.scenes, description='[cyan]translating points...'):
            xyz = self.data[scene]['coords']
            x = xyz[:, 0]
            y = xyz[:, 1]
            z = xyz[:, 2]

            xyz[:, 0] = x - x.min()
            xyz[:, 1] = y - y.min()
            xyz[:, 2] = z - z.min()
            self.data[scene]['coords'] = xyz

        self.normed = True

    def compute_statistics(self):
        pass

    def evaluator(self):
        pass

    def list_attributes(self, show=True):
        table = Table()
        table.add_column("groups", justify="center")
        table.add_column("attribute", justify="center")
        data = list(self.data[self.scenes[0]].keys()) if len(self.data) != 0 else []
        labels = list(self.labels[self.scenes[0]].keys()) if len(self.labels) != 0 else []
        gt = list(self.gt[self.scenes[0]].keys()) if len(self.gt) != 0 else []
        for row in data:
            table.add_row('data', row)
        for row in labels:
            table.add_row('label', row)
        for row in gt:
            table.add_row('gt', row)
        if show:
            print(table)
        attrs = ['data/' + at for at in data]
        attrs.extend(['labels/' + at for at in labels])
        attrs.extend(['gt/' + at for at in gt])
        return attrs

    def get_data_attribute(self, attribute, group='data'):
        attr = []
        group_data = getattr(self, group)
        if attribute not in list(group_data[self.scenes[0]].keys()):
            print('[red]This attribute does not exist, please check again using \'[yellow]whu3d.list_attribute()[/]\'')
        else:
            for scene in self.scenes:
                attr.append(group_data[scene][attribute])
        return attr

    def interprete_labels(self):
        if self.interpreted:
            print('[orange1][warning]Labels have been interpreted and it will be passed')
            return
        invalid = []
        for scene in track(self.scenes, description='[cyan]interpreting labels...'):
            pprint('processing %s...' % scene)
            ins = self.labels[scene]['instances']
            sem = self.labels[scene]['semantics']
            sem_map = self.sem_map

            sem_list = list(sem_map.keys())
            NUM_CLASSES = len(sem_list)

            sem_list.extend(list(set(sem)))
            sem_extend_set = set(sem_list)
            # print(sem_extend_set - set(list(sem_map.keys())))
            try:
                assert (len(sem_extend_set) == NUM_CLASSES)
            except:
                pprint('[red][Error: label] passing %s...' % scene)
                yn = pprint('[red]Do you want to delete scene: %s (\[y]/n)?' % scene)
                if yn != 'n':
                    invalid.append(scene)
                continue

            for k in self.sem_list_no_ins:
                ins[sem == k] = k
            ins[ins == 102600] = 102400

            ins_list = list(set(ins))
            ins_map = {ins_id: i for i, ins_id in enumerate(ins_list)}


            new_sem = np.zeros(sem.shape) - 1
            new_ins = np.zeros(ins.shape) - 1
            for i in sem_map.keys():
                new_sem[sem == i] = sem_map[i]
            for i in ins_map.keys():
                new_ins[ins == i] = ins_map[i]

            self.gt[scene] = {}

            self.gt[scene]['semantics'] = new_sem
            self.gt[scene]['instances'] = new_ins

        for scene in invalid:
            self.scenes.remove(scene)
            print('%s is removed!' % scene)

        self.interpreted = True

    def get_download(self, full=False, src='google'):
        file = json.load('download_links.json')
        data = file[src][self.data_type][self.format] if not full else file[src]['full'][self.format]
        download_link = data['link']
        passwd = data['passwd']
        print('download link: %s \npassword: %s' %(download_link, passwd))

    def get_label_map(self):
        table = Table()
        table.add_column("label", justify="center")
        table.add_column("class", justify="center")
        table.add_column("", justify="center")
        table.add_column("gt", justify="center")
        table.add_column("class", justify="center")
        for label, gt in self.sem_map.items():
            label_cls = self.label2cat[label]
            gt_cls = self.gt2cat[gt]
            row = (str(label), label_cls, ' ', str(gt), gt_cls)
            table.add_row(*row)
        print(table)

    def save_divided_blocks(self, out_dir='', num_points=4096, size=(10, 10), stride=5, threshold=100, show_points=False):
        if not self.interpreted or not self.normed:
            print('[red][error]Please interprete labels and norm the coords!')
            return
        if out_dir == '':
            out_dir = os.path.join(self.data_path, 'blocks')
        if not newpath(out_dir):
            print('Exit processing...')
            return
        for scene in track(self.scenes, description='[cyan]dividing blocks...'):
            wfname = os.path.join(out_dir, scene + '.h5')
            points = {}
            points['xyz'] = self.data[scene]['coords']
            attrs_v = self.return_feature_keys()
            feats = []
            for at in attrs_v:
                feats.append(self.data[scene][at])
            points['features'] = np.stack(feats, -1)
            points['labels'] = np.stack([self.gt[scene]['semantics'], self.gt[scene]['instances']], -1)

            save_h5_blocks(wfname, points, num_points, size_x=size[0], size_y=size[1], stride=stride, threshold=threshold, show_points=show_points, config=self.config)

    def get_num_features(self):
        return len(self.return_feature_keys())


    def preprocess(self):
        whu3d.norm_coords()
        # self.compute_normals()
        whu3d.interprete_labels()
        whu3d.compute_normals(radius=0.8)
        whu3d.save_divided_blocks(out_dir='', num_points=600000, size=(20, 20), stride=10, threshold=100,
                                  show_points=False)

    def trans_coords(self, translation):
        '''
        :param translation: [delta_x, delta_y, delta_z]
        :return:
        '''
        for scene in track(self.scenes, description='[cyan]translating points...'):
            xyz = self.data[scene]['coords']
            x = xyz[:, 0]
            y = xyz[:, 1]
            z = xyz[:, 2]

            xyz[:, 0] = x + translation[0]
            xyz[:, 1] = y + translation[1]
            xyz[:, 2] = z + translation[2]
            self.data[scene]['coords'] = xyz



if __name__ == '__main__':
    data_root = '/Users/hanxu/data/whu3d-dataset'
    # scenes = ['0404', '0940']
    whu3d = WHU3D(data_root=data_root, data_type='mls', format='txt')
    # whu3d.vis('0404', 'pc')
    whu3d.export_h5()
    whu3d.get_label_map()
    attr = whu3d.get_data_attribute('coords')
    whu3d.list_attributes()
    whu3d.interprete_labels()
    whu3d.list_attributes()
    whu3d.sample_points(0.1)
    whu3d.sample_points(0.1)