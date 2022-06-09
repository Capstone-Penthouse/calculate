# 공과금 계산
# 동계 : 11~4, 하계 5~10
import pandas as pd
import math
import numpy as np


# 연간 데이터_전기
data_year_e = pd.read_csv('elec.csv', header=None)
data_year_e.columns = ['month', 'usage', 'fee']

month_year_e = data_year_e[['month']]
usage_year_e = data_year_e[['usage']]
fee_year_e = data_year_e[['fee']]

fee_year_e = fee_year_e.values.ravel()

# 하절기 데이터_전기
data_summer_e = pd.read_csv('elec_summer.csv', header=None)
data_summer_e.columns = ['month', 'usage', 'fee']

month_summer_e = data_summer_e[['month']]
usage_summer_e = data_summer_e[['usage']]
fee_summer_e = data_summer_e[['fee']]

fee_summer_e = fee_summer_e.values.ravel()

# 동절기 데이터_전기
data_winter_e = pd.read_csv('elec_winter.csv', header=None)
data_winter_e.columns = ['month', 'usage', 'fee']

month_winter_e = data_winter_e[['month']]
usage_winter_e = data_winter_e[['usage']]
fee_winter_e = data_winter_e[['fee']]

fee_winter_e = fee_winter_e.values.ravel()

# 연간 데이터_가스
data_year_g = pd.read_csv('gas.csv', header=None)
data_year_g.columns = ['month', 'usage', 'fee']

month_year_g = data_year_g[['month']]
usage_year_g = data_year_g[['usage']]
fee_year_g = data_year_g[['fee']]

fee_year_g = fee_year_g.values.ravel()

# 하절기 데이터_가스
data_summer_g = pd.read_csv('gas_summer.csv', header=None)
data_summer_g.columns = ['month', 'usage', 'fee']

month_summer_g = data_summer_g[['month']]
usage_summer_g = data_summer_g[['usage']]
fee_summer_g = data_summer_g[['fee']]

fee_summer_g = fee_summer_g.values.ravel()

# 동절기 데이터_가스
data_winter_g = pd.read_csv('gas_winter.csv', header=None)
data_winter_g.columns = ['month', 'usage', 'fee']

month_winter_g = data_winter_g[['month']]
usage_winter_g = data_winter_g[['usage']]
fee_winter_g = data_winter_g[['fee']]

fee_winter_g = fee_winter_g.values.ravel()


def calculate(fee, data):

    new_fee = sorted(fee)
    fee_mean = sum(new_fee) / len(new_fee)

    sd = 0
    for i in new_fee:
        sd += (i - fee_mean) ** 2
    sd = math.sqrt(sd / len(data))
    var = sd ** 2

    y = []
    for i in new_fee:
        y.append((1 / math.sqrt(2 * np.pi * (sd ** 2))) * np.exp((-(i - fee_mean) ** 2) / (2 * (sd ** 2))))

    under = fee_mean-sd
    avg = fee_mean
    over = fee_mean + sd

    return sd, under, avg, over

sd_ey, under_ey, avg_ey, over_ey = calculate(fee_year_e, data_year_e)
sd_es, under_es, avg_es, over_es = calculate(fee_summer_e, data_summer_e)
sd_ew, under_ew, avg_ew, over_ew = calculate(fee_winter_e, data_winter_e)
sd_gy, under_gy, avg_gy, over_gy = calculate(fee_year_g, data_year_g)
sd_gs, under_gs, avg_gs, over_gs = calculate(fee_summer_g, data_summer_g)
sd_gw, under_gw, avg_gw, over_gw = calculate(fee_winter_g, data_winter_g)


def calculate_new(my_data, new_mean, sd_y, sd_s, sd_w, avg_y, avg_s, avg_w):

    new_sd = sd_y * new_mean / avg_y
    predicted_fee = new_mean + ((my_data - avg_y) / sd_y) * new_sd

    avg_ns = avg_s * new_mean/avg_y
    sd_ns = sd_s * new_sd/sd_y
    predicted_summer = sd_ns * (predicted_fee - new_mean)/new_sd + avg_ns

    avg_nw = avg_w * new_mean/avg_y
    sd_nw = sd_w * new_sd/sd_y
    predicted_winter = sd_nw * (predicted_fee - new_mean)/new_sd + avg_nw

    return predicted_fee, predicted_summer, predicted_winter


# print(avg_ey, avg_es, avg_ew)
# print(avg_gy, avg_gs, avg_gw)
# print(sd_ey, sd_es, sd_ew, sd_gy, sd_gs, sd_gw)

