import argparse
import json
import logging
import os
from typing import List
import natsort

import cv2
import numpy as np
import pandas as pd

try:
    import rasterio
except ImportError:
    rasterio = None

from crx_ism_pack.quality_metrics import metric_functions
logger = logging.getLogger(__name__)


def read_image(path: str):
    logger.info(f"Reading image {os.path.basename(path)}")
    if rasterio and (path.endswith(".tif") or path.endswith(".tiff")):
        return np.rollaxis(rasterio.open(path).read(), 0, 3)
    return cv2.imread(path)


def dataset_path(data_path, data_type):
    filelist = None
    if data_type == "AP":
        filelist = natsort.natsorted(os.listdir(f'{data_path}'))
    elif data_type == "LL":
        filelist = natsort.natsorted(os.listdir(f'{data_path}'))
    elif data_type == "single_img":
        return filelist
    else:
        print("please enter --data_type parameter")
    return filelist


def evaluation(org_img_path: str, pred_img_path: str, metrics: List[str]):
    output_dict = {}

    org_img = read_image(org_img_path)
    pred_img = read_image(pred_img_path)

    # org to pred image's resize
    org_pix = org_img.shape[0] + org_img.shape[1]
    pred_pix = pred_img.shape[0] + pred_img.shape[1]
    if org_pix < pred_pix:
        pred_img = cv2.resize(pred_img, (org_img.shape[1], org_img.shape[0]))
    else:
        org_img = cv2.resize(org_img, (pred_img.shape[1], pred_img.shape[0]))

    for metric in metrics:
        metric_func = metric_functions[metric]
        out_value = float(metric_func(org_img, pred_img))
        logger.info(f"{metric.upper()} value is: {out_value}")
        output_dict[metric] = out_value

    return output_dict


def evaluation2(metrics: List[str], data_type: str, level: str, 비교군: str):
    path = f"../example/V5"

    output_df = pd.DataFrame(columns=metrics)
    pred_img = read_image(f"{path}/{비교군}/Warp{data_type}_{level}.png")
    data_path = f"{path}/{비교군}/{data_type}_{level}"
    img_list = dataset_path(data_path, data_type)
    if img_list is not None:
        for idx, org_img_path in enumerate(img_list):
            org_img = read_image(f"{data_path}/{org_img_path}")
            print(f"{data_path}/{org_img_path}")

            # org to pred image's resize
            org_pix = org_img.shape[0] + org_img.shape[1]
            pred_pix = pred_img.shape[0] + pred_img.shape[1]

            if org_pix < pred_pix:
                pred_img = cv2.resize(pred_img, (org_img.shape[1], org_img.shape[0]))
            else:
                org_img = cv2.resize(org_img, (pred_img.shape[1], pred_img.shape[0]))
            output = []
            for metric in metrics:
                metric_func = metric_functions[metric]
                out_value = float(metric_func(org_img, pred_img))
                logger.info(f"{metric.upper()} value is: {out_value}")
                output.append(out_value)
            add_df = pd.DataFrame([output], columns=output_df.columns)
            add_df = add_df.set_index([pd.Index([org_img_path[:-4]])])
            output_df = pd.concat([output_df, add_df], axis=0)

        output_df.to_csv(f"{path}/{비교군}_{data_type}_{level}_Registration_Result_v5.csv", sep=',', header=True,
                         index=True)


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    all_metrics = sorted(metric_functions.keys())
    parser = argparse.ArgumentParser(
        description="Evaluates an Image Super Resolution Model"
    )
    parser.add_argument(
        "--org_img_path",
        help="Path to original input image",
        # required=True,
        metavar="FILE",
    )
    parser.add_argument(
        "--pred_img_path", help="Path to predicted image", required=True, metavar="FILE"
    )
    parser.add_argument(
        "--metric",
        dest="metrics",
        action="append",
        choices=all_metrics + ["all"],
        metavar="METRIC",
        help="select an evaluation metric (%(choices)s) (can be repeated)",
    )
    args = parser.parse_args()
    if not args.metrics:
        args.metrics = ["psnr"]
    if "all" in args.metrics:
        args.metrics = all_metrics

    metric_values = evaluation(
        org_img_path=args.org_img_path,
        pred_img_path=args.pred_img_path,
        metrics=args.metrics,
    )
    result_dict = {
        "image1": args.org_img_path,
        "image2": args.pred_img_path,
        "metrics": metric_values,
    }
    print(json.dumps(result_dict, sort_keys=True))


def main2():
    metrics = ["uiq", "ssim", "fsim"]
    levels = ["6th_T7", "6th_T8", "6th_T9"]
    for level in levels:
        evaluation2(metrics=metrics, data_type="AP", level=level, 비교군="BODY")
        evaluation2(metrics=metrics, data_type="LL", level=level, 비교군="BODY")
    levels = ["6th_L2", "7th_L2", "8th_L2"]
    for level in levels:
        evaluation2(metrics=metrics, data_type="AP", level=level, 비교군="PATIENT")
        evaluation2(metrics=metrics, data_type="LL", level=level, 비교군="PATIENT")


def main3():
    val = None
    val = evaluation(org_img_path="D:\\test\\org_image.jpg",
                     pred_img_path="D:\\test\\pred_image.jpg",
                     metrics=["uiq", "fsim"])
    return val


if __name__ == "__main__":
    result = None
    result = main3()
