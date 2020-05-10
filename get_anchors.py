#!/usr/bin/env python
# coding: utf-8

import os
import json
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

LABELS_PATH = 'labels raw/'
input_shape = (1920, 1024) # Original image shape
used_shape = (416, 416) # Used shape of image in model
n_anchors = 9


def kmeans_sklearn(X, num_clusters):
    w, h = list(zip(*X))
    x = [w, h]
    x = np.asarray(x)
    x = x.transpose()

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(x)
    centers = kmeans.cluster_centers_
    y_kmeans = kmeans.predict(x)

    return centers, y_kmeans


def IOU(x, centroids):
   '''
    :param x: a ground truth w,h
         :param centroids: collection of anchor w,h[(w,h),(),...], total k
         :return: a set of IoU values ​​for a single ground truth box and all k anchor boxes
    '''
    IoUs = []
    w, h = x  # ground truth's w, h

    for c_w, c_h in centroids:
        if c_w >= w and c_h >= h:  # anchor surrounded by ground truth
            iou = w * h / (c_w * c_h)
        elif c_w >= w and c_h <= h:  # anchor
            iou = w * c_h / (w * h + (c_w - w) * c_h)
        elif c_w <= w and c_h >= h:  # anchor elongated
            iou = c_w * h / (w * h + c_w * (c_h - h))
        else:  # ground truth surrounded by anchor means both w,h are bigger than c_w and c_h respectively
            iou = (c_w * c_h) / (w * h)
        IoUs.append(iou)  # will become (k,) shape
    return np.array(IoUs)


def avg_IOU(X, centroids):
    '''
         :param X: The set of w,h of ground truth[(w,h),(),...]
         :param centroids: collection of anchor w,h[(w,h),(),...], total k
    '''
    n, d = X.shape
    sum = 0.
    for i in range(X.shape[0]):
        sum += max(IOU(X[i], centroids))  # return a ground truth with the maximum value of all anchors in IoU
    return sum / n  # average all ground truth


def kmeans_iou(X, num_clusters):
    N = X.shape[0]

    #     # Take random centers
    #     indices = [random.randrange(N) for i in range(num_clusters)]
    #     centroids = X[indices]

    # Take centroids from L2 K means as initialisation
    centroids, _ = kmeans_sklearn(X, num_clusters)

    k, dim = centroids.shape  # anchor number k and w,h two-dimensional, dim default equal to 2
    prev_assignments = np.ones(N) * (-1)  # Assign the initial label to each ground truth
    # old_D = np.zeros((N, k))  # Initialize each ground truth for each anchor's IoU

    iter = 0
    while True:
        iter += 1
        # Calculate distances from bounding boxes to centroids
        D = np.array([1 - IOU(x, centroids) for x in X])

        # Calculate the value of each iteration and the previous IoU change
        #         print("iter {}: dists = {}".format(iter, np.sum(np.abs(old_D - D))))

        # assign samples to centroids
        assignments = np.argmin(D, axis=1)  # Assign each ground truth to the anchor number with the smallest distance d

        # If the result of the previous assignment is the same as the result of this time, the anchor and the average IoU are output.
        if (assignments == prev_assignments).all():
            print("K means converged")
            return centroids, assignments

        # calculate new centroids
        centroid_sums = np.zeros((k, dim), np.float)  # initialize to sum w and h for each cluster
        for i in range(N):
            centroid_sums[assignments[i]] += X[i]  # accumulate the ground truths w and h in each cluster
        for j in range(k):  # averaging w,h in the cluster
            centroids[j] = centroid_sums[j] / (np.sum(assignments == j) + 1)

        prev_assignments = assignments.copy()
        old_D = D.copy()


def main():
    # Extract widths and heights of the bounding boxes
    city_names = sorted(os.listdir(LABELS_PATH))
    print(f"Found city folders:\n{city_names}")

    annotation_dims = []

    # Save all ground truth boxes (w, h)
    for i in range(len(city_names)):
        for each in sorted(os.listdir(LABELS_PATH + city_names[i])):
            file_name = LABELS_PATH + city_names[i] + '/' + each
            with open(file_name) as json_file:
                data = json.load(json_file)
                for obj in data['children']:
                    width = obj['x1'] - obj['x0']
                    height = obj['y1'] - obj['y0']
                    annotation_dims.append((width, height))

    annotation_dims = np.array(annotation_dims)
    print(f"In total there are {len(annotation_dims)} boxes")

    print("Calculating using approach 1")
    centroids1, assignments1 = kmeans_iou(annotation_dims, n_anchors)  # Approach 1
    print("Calculating using approach 2")
    centroids2, assignments2 = kmeans_sklearn(annotation_dims, n_anchors)  # Approach 2

    plt.figure(figsize=(20, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(annotation_dims[:, 0], annotation_dims[:, 1], c=assignments1, s=2, cmap='viridis')
    plt.scatter(centroids1[:, 0], centroids1[:, 1], c='red', s=50)
    plt.title("K means iou")

    plt.subplot(1, 2, 2)
    plt.scatter(annotation_dims[:, 0], annotation_dims[:, 1], c=assignments2, s=2, cmap='viridis')
    plt.scatter(centroids2[:, 0], centroids2[:, 1], c='red', s=50)
    plt.title("K means L2")
    plt.savefig("Comparison of clusters.png")
    # plt.show()

    # Adapt to model sizes
    centroids1[:, 0] = centroids1[:, 0] * used_shape[0] / input_shape[0]
    centroids1[:, 1] = centroids1[:, 1] * used_shape[1] / input_shape[1]
    centroids1 = np.rint(centroids1)

    centroids2[:, 0] = centroids2[:, 0] * used_shape[0] / input_shape[0]
    centroids2[:, 1] = centroids2[:, 1] * used_shape[1] / input_shape[1]
    centroids2 = np.rint(centroids2)

    for centroids, title in zip([centroids1, centroids2], ["K means IOU", "K means L2"]):
        fig, ax = plt.subplots()
        for ind in range(len(centroids)):
            rectangle = plt.Rectangle((used_shape[0] / 2 - centroids[ind, 0] / 2,
                             used_shape[1] / 2 - centroids[ind, 1] / 2),
                             centroids[ind, 0],
                             centroids[ind, 1],
                             fc='b', edgecolor='b', fill=None)
            ax.add_patch(rectangle)
        ax.set_aspect(1.0)
        plt.title(title)
        plt.axis([0, used_shape[0], 0, used_shape[1]])
        plt.savefig(title + " anchors.png")
        # plt.show()

    # Sort according to width and save
    centroids1 = np.array(sorted(centroids1, key=lambda params: params[0]))
    centroids_str = ", ".join([",".join(list(map(str, centroid))) for centroid in centroids1.astype(int)])
    print(f"Anchors: \n{centroids_str}")

    F = open("anchors_approach1.txt", "w")
    F.write("{}".format(centroids_str))
    F.close()

    centroids2 = np.array(sorted(centroids2, key=lambda params: params[0]))
    centroids_str = ", ".join([",".join(list(map(str, centroid))) for centroid in centroids2.astype(int)])
    print(f"Anchors: \n{centroids_str}")

    F = open("anchors_approach2.txt", "w")
    F.write("{}".format(centroids_str))
    F.close()


if __name__ == "__main__":
    main()
