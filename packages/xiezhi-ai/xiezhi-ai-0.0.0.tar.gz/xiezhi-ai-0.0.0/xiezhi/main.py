import numpy as np
def xiezhi_detect(data,beta,alpha):

    len_data=len(data)
    data_med = np.median(data)
    #dis_median = [np.log(abs(data[i] - data_med)) if abs(data[i] - data_med) != 0 else abs(data[i] - data_med) for i in range(len_data)]
    dis_median = [np.log(abs(data[i] - data_med)) for i in range(len_data)]
    dis = sorted(dis_median)

    delta=[dis[i] - dis[i - 1] for i in range(len_data) if i!=0]
    len_delta=len(delta)

    # The stopping criteria
    max_dis = max(delta[int(len_data*beta):int(len_data*alpha)])

    for i in range(len(delta[int(len_delta*alpha):])):
        if delta[int(len_delta*alpha):][i] > max_dis:
            stop_point = dis[i + int(len_delta*alpha)]
            #print('The key point is', stop_point)
            break
        else:
            stop_point = dis[-1]

    outliers=[data[dis_median.index(i)] for i in dis_median if i > stop_point]

    return [i for i in data if i not in outliers]