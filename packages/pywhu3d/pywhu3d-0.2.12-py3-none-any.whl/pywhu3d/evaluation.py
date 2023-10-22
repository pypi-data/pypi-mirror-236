import numpy as np
from collections import Counter
import time
from rich.console import Console

console = Console(soft_wrap=True)
print = console.print
input = console.input
rule = Console(soft_wrap=True, width=100).rule
from rich import box
from rich.progress import track
from rich.table import Column, Table
from prettytable import PrettyTable as PT
import xlwt
from scipy import stats

class Evaluator:
    def __init__(self, whu3d, pred):
        assert len(pred[0][-1])==2, 'pred format wrong!'
        self.truth = []
        self.pred = []
        assert len(pred) == len(whu3d.scenes)
        for scene in whu3d.scenes:
            ins = whu3d.gt[scene]['semantics'].astype('int32')
            sem = whu3d.gt[scene]['instances'].astype('int32')
            self.truth.append(np.stack([ins, sem], axis=1))
        for pr in pred:
            self.pred.append(pr.astype('int32'))
        self.num_scenes = len(whu3d.gt)
        self.num_classes = whu3d.num_classes
        self.label2cat = whu3d.gt2cat
        self.compute_ins_list = whu3d.compute_ins_list
        self.workbook = None
        self.eval_list = None
        self.info = None
        self.eval_table = None

    def set_gt(self, truth):
        assert len(truth[0][-1]) == 2, 'gt format wrong!'
        self.truth = []
        for gt in truth:
            self.truth.append(gt.astype('int32'))

    def compute_metrics(self):
        seg_label_to_cat = self.label2cat
        compute_ins_list = self.compute_ins_list

        pred_time = 0
        cluster_time = 0
        merge_time = 0
        eval_time = 0

        num_classes = self.num_classes

        total_true = 0
        total_seen = 0
        true_positive_classes = np.zeros(num_classes)
        inters = np.zeros(num_classes)
        unions = np.zeros(num_classes)
        Ts = np.zeros(num_classes)
        Ps = np.zeros(num_classes)
        positive_classes = np.zeros(num_classes)
        gt_classes = np.zeros(num_classes)
        # precision & recall
        total_gt_ins = np.zeros(num_classes)
        at = 0.5
        tpsins = [[] for itmp in range(num_classes)]
        fpsins = [[] for itmp in range(num_classes)]
        # mucov and mwcov
        all_mean_cov = [[] for itmp in range(num_classes)]
        all_mean_weighted_cov = [[] for itmp in range(num_classes)]

        sem_pred_map = np.zeros([num_classes, num_classes], dtype=np.int32)

        for i in track(range(self.num_scenes), description='[cyan]Evaluating...'):

            estart = time.time()
            pred = self.pred[i]
            # step = coords.shape[0]
            truth = self.truth[i]

            pred_ins = pred[..., 1]
            pred_sem = pred[..., 0]
            gt_ins = truth[..., 1]
            gt_sem = truth[..., 0]

            # semantic acc
            total_true += np.sum(pred_sem == gt_sem)
            total_seen += pred_sem.shape[0]

            for sem in range(num_classes):
                gt_classes[sem] += np.sum(gt_sem == sem)
                positive_classes[sem] += np.sum(pred_sem == sem)
                true_positive_classes[sem] += np.sum((gt_sem == sem) & (pred_sem == sem))

            #############################################

            for cat in range(num_classes):
                # intersection = np.sum((batch_target == cat) & (batch_choice == cat))
                # union = float(np.sum((batch_target == cat) | (batch_choice == cat)))
                # iou = intersection/union if not union ==0 else 1
                I = np.sum(np.logical_and(pred_sem == cat, gt_sem == cat))
                U = np.sum(np.logical_or(pred_sem == cat, gt_sem == cat))
                P = np.sum(pred_sem == cat)
                T = np.sum(gt_sem == cat)
                inters[cat] += I
                unions[cat] += U
                Ps[cat] += P
                Ts[cat] += T
                cat_counter = Counter(pred_sem[gt_sem == cat])
                for pred_cat in cat_counter.keys():
                    sem_pred_map[cat, pred_cat] += cat_counter[pred_cat]

            # instance
            un = np.unique(pred_ins)
            pts_in_pred = [[] for itmp in range(num_classes)]
            for ig, g in enumerate(un):  # each object in prediction
                if g == -1:
                    continue
                tmp = (pred_ins == g)
                sem_seg_i = int(stats.mode(pred_sem[tmp])[0])
                pts_in_pred[sem_seg_i] += [tmp]

            un = np.unique(gt_ins)
            pts_in_gt = [[] for itmp in range(num_classes)]
            for ig, g in enumerate(un):
                tmp = (gt_ins == g)
                sem_seg_i = int(stats.mode(gt_sem[tmp])[0])
                pts_in_gt[sem_seg_i] += [tmp]

            # instance mucov & mwcov
            for i_sem in range(num_classes):
                sum_cov = 0
                mean_weighted_cov = 0
                num_gt_point = 0
                for ig, ins_gt in enumerate(pts_in_gt[i_sem]):
                    ovmax = 0.
                    num_ins_gt_point = np.sum(ins_gt)
                    num_gt_point += num_ins_gt_point
                    for ip, ins_pred in enumerate(pts_in_pred[i_sem]):
                        union = (ins_pred | ins_gt)
                        intersect = (ins_pred & ins_gt)
                        iou = float(np.sum(intersect)) / np.sum(union)

                        if iou > ovmax:
                            ovmax = iou

                    sum_cov += ovmax
                    mean_weighted_cov += ovmax * num_ins_gt_point

                if len(pts_in_gt[i_sem]) != 0:
                    mean_cov = sum_cov / len(pts_in_gt[i_sem])
                    all_mean_cov[i_sem].append(mean_cov)

                    mean_weighted_cov /= num_gt_point
                    all_mean_weighted_cov[i_sem].append(mean_weighted_cov)

            # instance precision & recall
            for i_sem in range(num_classes):
                tp = [0.] * len(pts_in_pred[i_sem])
                fp = [0.] * len(pts_in_pred[i_sem])
                gtflag = np.zeros(len(pts_in_gt[i_sem]))
                total_gt_ins[i_sem] += len(pts_in_gt[i_sem])

                for ip, ins_pred in enumerate(pts_in_pred[i_sem]):
                    ovmax = -1.

                    for ig, ins_gt in enumerate(pts_in_gt[i_sem]):
                        union = (ins_pred | ins_gt)
                        intersect = (ins_pred & ins_gt)
                        iou = float(np.sum(intersect)) / np.sum(union)

                        if iou > ovmax:
                            ovmax = iou
                            igmax = ig

                    if ovmax >= at:
                        tp[ip] = 1  # true
                    else:
                        fp[ip] = 1  # false positive

                tpsins[i_sem] += tp
                fpsins[i_sem] += fp

            eval_time += time.time() - estart

        estart = time.time()

        MUCov = np.zeros(num_classes)
        MWCov = np.zeros(num_classes)

        precision = np.zeros(num_classes)
        recall = np.zeros(num_classes)
        f1 = np.zeros(num_classes)

        workbook = xlwt.Workbook(encoding='ascii')
        evalsheet = workbook.add_sheet('eval info')
        inssheet = workbook.add_sheet('ins info')
        semsheet = workbook.add_sheet('sem info')

        ins_info = PT()
        col_name = ' '
        col_data = ['True Total', 'Pred Total', 'True Positive', 'False Positive', 'Precision', 'Recall']
        ins_info.add_column(col_name, col_data)
        col_list = [col_name] + col_data
        for row, val in enumerate(col_list):
            inssheet.write(row, 0, val)
        for i_sem in range(num_classes):
            tp = np.asarray(tpsins[i_sem]).astype(np.float64)
            fp = np.asarray(fpsins[i_sem]).astype(np.float64)
            tp = np.sum(tp)
            fp = np.sum(fp)
            rec = tp / total_gt_ins[i_sem]
            prec = tp / (tp + fp) if (tp + fp) != 0 else 0
            MUCov[i_sem] = np.nanmean(all_mean_cov[i_sem])
            MWCov[i_sem] = np.nanmean(all_mean_weighted_cov[i_sem])
            if i_sem not in compute_ins_list:
                rec = np.nan
                prec = np.nan
                MUCov[i_sem] = np.nan
                MWCov[i_sem] = np.nan
            precision[i_sem] = prec
            recall[i_sem] = rec
            if prec + rec != 0:
                f1[i_sem] = 2 * prec * rec / (prec + rec)
            else:
                f1[i_sem] = 0
            L = [total_gt_ins[i_sem], tp + fp, tp, fp]
            col_name = seg_label_to_cat[i_sem]
            col_data = [format(l, '.0f') for l in L] + [format(prec, '.3f'), format(rec, '.3f')]
            col_list = [col_name] + col_data
            ins_info.add_column(col_name, col_data)
            for row, val in enumerate(col_list):
                inssheet.write(row, i_sem + 1, val)

        iou_list = list(inters / unions)

        row_list = [' ', 'Truth'] + list(seg_label_to_cat.values())
        sem_info = PT(row_list)
        for col, val in enumerate(row_list):
            semsheet.write(0, col, val)
        for i, cls in enumerate(sem_pred_map):
            row_list = [seg_label_to_cat[i], format(gt_classes[i], '.0f')] + [format(cl, '.0f') for cl in list(cls)]
            sem_info.add_row(row_list)
            for col, val in enumerate(row_list):
                semsheet.write(i + 1, col, val)

        eval_info = PT()
        cols = []
        col_name = ' '
        col_data = ['MUCov', 'MWCov', 'Pre', 'Rec', 'F1', 'oAcc', 'mAcc', 'mIoU']
        col_list = [col_name] + col_data
        cols.append(col_list)
        eval_info.add_column(col_name, col_data, align='l')
        for row, val in enumerate(col_list):
            evalsheet.write(row, 0, val)
        eval_list = [np.nanmean(MUCov), np.nanmean(MWCov), np.nanmean(precision), np.nanmean(recall), np.nanmean(f1), \
                     sum(true_positive_classes) / float(sum(positive_classes)), \
                     np.nanmean(true_positive_classes / gt_classes), np.nanmean(iou_list)]
        column_list = ['{:.3f}'.format(i) for i in eval_list]
        col_list = ['mean'] + column_list
        cols.append(col_list)
        eval_info.add_column('mean', column_list)
        for row, val in enumerate(col_list):
            evalsheet.write(row, 1, val)
        for i in range(num_classes):
            column_list = [MUCov[i], MWCov[i], precision[i], recall[i], f1[i],
                           true_positive_classes[i] / positive_classes[i], true_positive_classes[i] / gt_classes[i],
                           iou_list[i]]
            column_list = ['{:.3f}'.format(i) for i in column_list]
            eval_info.add_column(seg_label_to_cat[i], column_list)
            col_list = [seg_label_to_cat[i]] + column_list
            cols.append(col_list)
            for row, val in enumerate(col_list):
                evalsheet.write(row, i + 2, val)

        cols = list(np.stack(cols).transpose([1, 0]))
        eval_table = Table(title='Evaluation', box=box.HORIZONTALS, padding=(0, 0))
        for cat in cols[0]:
            if cat == ' ':
                eval_table.add_column('[green]-', justify='center', style='bright_magenta b')
            elif cat == 'mean':
                eval_table.add_column('[green]' + cat.ljust(6), justify='center', style='bright_cyan b')
            else:
                eval_table.add_column('[bright_yellow]' + cat.ljust(6), justify='center')
        for row in cols[1:]:
            eval_table.add_row(*row)
        # console.print(eval_table, soft_wrap=True)

        eval_time += time.time() - estart
        info = {'ins info': ins_info, 'sem info': sem_info, 'eval info': eval_info,
                'time': [pred_time, cluster_time, merge_time, eval_time]}
        self.workbook = workbook
        self.eval_list = eval_list
        self.info = info
        self.eval_table = eval_table

    def export(self, output_dir):
        if not self.workbook:
            print('[red]Please run \'compute_metrics\' function first!')
        else:
            self.workbook.save(output_dir + '/eval.xls')


if __name__ == '__main__':
    from pywhu3d.tool import WHU3D

    data_root = '/Users/hanxu/data/whu'
    scenes = ['0404', '0940']
    whu3d = WHU3D(data_root=data_root, data_type='mls', format='h5', scenes=scenes)
    whu3d.interprete_labels()
    gts = []
    for scene in whu3d.scenes:
        ins = whu3d.gt[scene]['semantics']
        sem = whu3d.gt[scene]['instances']
        gts.append(np.stack([ins, sem], axis=1))

    eval = Evaluator(whu3d, gts)
    eval.compute_metrics()
    eval.export('/Users/hanxu/Downloads/')
    print(eval.eval_table)
    print(eval.info)

