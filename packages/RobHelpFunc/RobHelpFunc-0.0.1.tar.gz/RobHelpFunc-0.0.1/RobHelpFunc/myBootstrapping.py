def myBootstrapping(data1, data2, N):
    '''Function to bootstrap data1 and data2 N times and return the difference in means of the bootstrapped data.'''
    import numpy as np

    # length of data1, data2
    n0 = data1.shape[0]
    n1 = data2.shape[0]

    # calculate mean difference
    mean_diff = np.mean(data1) - np.mean(data2)

    # concatenate data1 and data2
    data = np.concatenate((data1, data2))

    # randomly choose a value from data1 n0 times with replacement
    # randomly choose a value from data2 n1 times with replacement
    # calculate the difference in means
    # repeat N times
    # store the differences in means in an array
    diff_means_boot = np.zeros(N)
    p = np.zeros(N)

    for i in range(N):
        data1_boot = np.random.choice(data, n0, replace=True)
        data2_boot = np.random.choice(data, n1, replace=True)
        diff_means_boot[i] = np.mean(data1_boot) - np.mean(data2_boot)

        # compare the mean_diff and diff_mean[i]
        # if diff_mean[i] is greater than mean_diff, add 1 to p
        if diff_means_boot[i] > mean_diff:
            p[i] = 1

    # calculate the p-value
    p_value = np.sum(p)/N

    return p_value