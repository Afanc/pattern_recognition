#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

def feature_extraction(col):
    """
    input: column of a image
    output: feature vector containing the different feature values of this column

    features:
        number_of_black_pixels
        upper_boundary
        lower_boundary
        black_white_transitions
        ...?
    """
    # update this if you add a feature
    num_of_features = 4

    # number of black pixels
    number_of_black_pixels = np.sum(col == 0)
    #if there are black pixels in this column the other features need to be calculated
    if number_of_black_pixels > 0:
        upper_boundary = np.argwhere(col == 0)[0][0]  # get first index of black pixel
        lower_boundary = np.argwhere(col[::-1, :] == 0)[0][0]   # invert the array and get first index of black pixel
        black_white_transitions = 0
        for row in range(upper_boundary, len(col)-lower_boundary-1):  # iterate from first to last black pixel
            # when there is a transition from black to white, the counter is increased by one
            if col[row, 0] < col[row+1, 0]:
                black_white_transitions += 1
    # if there are no black pixels the features get the following values
    else:
        upper_boundary = len(col)
        lower_boundary = len(col)
        black_white_transitions = 0
    feature_values = np.array([number_of_black_pixels, upper_boundary, lower_boundary, black_white_transitions]).reshape(num_of_features, )
    return feature_values


def get_feature_vectors(img):
    """
    takes an image as input
    computes the feature vectors for the different features
    returns a matrix of the feature vectors (each row corresponds to a feature vector
    """
    feature_matrix = np.zeros(shape = (4, img.shape[1]))
    for col in range(img.shape[1]):
        feature_matrix[:, col] = feature_extraction(img[:,col].reshape(img.shape[0],1))
    return feature_matrix


def normalization(feature_matrix):
    """
    takes a feature matrix as imput: each row corresponds to the feature vector of a image for one particular feature
    returns a normalized feature matrix  (xi-mean)/sd
    """
    for row in range(4):
        feature_matrix[row, :] = (feature_matrix[row, :] - np.mean(feature_matrix[row, :])) / np.std(feature_matrix[row,:])
    return feature_matrix

#short example
#img = plt.imread("src/main/py/kws/data/resized_word_images/270-01-01_s_2.png")
#plt.imshow(img)
#plt.show()
#a=get_feature_vectors(img)
#print(a[:,:20])
#print(a.shape)
#n=normalization(a)
#print(n[:,:20])