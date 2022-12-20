################################################################################
# File: train_production_validation.py                                         #
# Project: Spindle                                                             #
# Created Date: Wednesday, 14th December 2022 5:11:14 pm                       #
# Author: Viraj Bagal (viraj.bagal@synapsica.com)                              #
# -----                                                                        #
# Last Modified: Monday, 19th December 2022 5:36:40 pm                         #
# Modified By: Viraj Bagal (viraj.bagal@synapsica.com)                         #
# -----                                                                        #
# Copyright (c) 2022 Synapsica                                                 #
################################################################################
import os
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

from deepchecks.vision import VisionData
from deepchecks.vision.suites import train_test_validation

CURRENT_DIR = os.getcwd()

PATH_TO_TRAIN_DATA = os.path.join(CURRENT_DIR, "train_images/tiny-imagenet-200/train")
PATH_TO_PROD_DATA = os.path.join(CURRENT_DIR, "downloaded_minio_images")


class ImagesData(VisionData):
    """Implement a VisionData class for PIL images."""

    def batch_to_images(self, batch):
        """Convert a batch of images to a list of PIL images.

        Parameters
        ----------
        batch : torch.Tensor
            The batch of images to convert.

        Returns
        -------
        list
            A list of PIL images.
        """

        # Assuming batch[0] is a batch of (N, C, H, W) images, we convert it to (N, H, W, C)/
        imgs = batch[0].detach().numpy().transpose((0, 2, 3, 1))

        # The images are normalized to [0, 1] range based on the mean and std of the ImageNet dataset, so we need to
        # convert them back to [0, 255] range.
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        imgs = std * imgs + mean
        imgs = np.clip(imgs, 0, 1)
        imgs *= 255
        return imgs

    def batch_to_labels(self, batch):
        return batch[1]

    def get_classes(self, batch_labels):
        """Get a labels batch and return classes inside it."""
        return batch_labels.reshape(-1, 1).tolist()


transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
train_dataset = torchvision.datasets.ImageFolder(PATH_TO_TRAIN_DATA, transform=transform)
test_dataset = torchvision.datasets.ImageFolder(PATH_TO_PROD_DATA, transform=transform)

# split the data
train_dataset, val_data, test_data = torch.utils.data.random_split(train_dataset, [5000, 85000, 10000])

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

train_ds = ImagesData(train_loader)
test_ds = ImagesData(test_loader)
# Checks the following properties. Taken from: https://github.com/deepchecks/deepchecks/blob/main/deepchecks/vision/suites/default_suites.py
"""
Suite(
        'Train Test Validation Suite',
        NewLabels(**kwargs).add_condition_new_label_ratio_less_or_equal(),
        HeatmapComparison(**kwargs),
        TrainTestLabelDrift(**kwargs).add_condition_drift_score_less_than(),
        ImagePropertyDrift(**kwargs).add_condition_drift_score_less_than(),
        ImageDatasetDrift(**kwargs),
        PropertyLabelCorrelationChange(**kwargs).add_condition_property_pps_difference_less_than(),
    )
"""
suite = train_test_validation(min_samples=10)
result = suite.run(train_dataset=train_ds, test_dataset=test_ds)
result.save_as_html()
