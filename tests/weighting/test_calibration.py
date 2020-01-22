import numpy as np
import pandas as pd

import samplics
from samplics.weighting import SampleWeight

# All categorical
sample_cat = pd.DataFrame(
    [
        ["A1", "B1", 2, 8],
        ["A1", "B2", 4, 4],
        ["A1", "B3", 4, 5.5],
        ["A2", "B1", 5, 6],
        ["A2", "B2", 14, 15],
        ["A2", "B3", 31, 34],
        ["A3", "B1", 10, 17],
        ["A3", "B2", 5, 6],
        ["A3", "B3", 5, 20],
        ["A4", "B1", 3, 5.5],
        ["A4", "B2", 10, 16.5],
        ["A4", "B3", 7, 12.5],
    ]
)
sample_cat.rename(columns={0: "A", 1: "B", 2: "wgt", 3: "benchmark"}, inplace=True)
sample_cat = pd.concat([sample_cat] * 10, ignore_index=True)
sample_cat.sort_values(by=["A", "B"], inplace=True)
domain = np.tile(["D1", "D2"], 60)
sample_cat.insert(0, "Domain", domain)
aux_array, aux_dict = SampleWeight().calib_covariates(sample_cat, ["A", "B"])

aux_dict["A1_&_B1"] = 80
aux_dict["A1_&_B2"] = 40
aux_dict["A1_&_B3"] = 55
aux_dict["A2_&_B1"] = 60
aux_dict["A2_&_B2"] = 150
aux_dict["A2_&_B3"] = 340
aux_dict["A3_&_B1"] = 170
aux_dict["A3_&_B2"] = 60
aux_dict["A3_&_B3"] = 200
aux_dict["A4_&_B1"] = 55
aux_dict["A4_&_B2"] = 165
aux_dict["A4_&_B3"] = 125

sample_cat["_calib_wgt"] = SampleWeight().calibrate(sample_cat["wgt"], aux_array, control=aux_dict)
sample_cat["_calib_adjust_fct"] = sample_cat["_calib_wgt"] / sample_cat["wgt"]
# print(sample_cat.drop_duplicates())


def test_calibration_cat():
    sample_cat.drop_duplicates(["A", "B"], inplace=True)
    sample_cat.sort_values(by=["A", "B"], inplace=True)
    assert np.isclose(
        sample_cat["_calib_adjust_fct"].values,
        np.array(
            [
                4.000000,
                1.000000,
                1.375000,
                1.200000,
                1.071429,
                1.096774,
                1.700000,
                1.200000,
                4.000000,
                1.833333,
                1.650000,
                1.785714,
            ]
        ),
    ).all()


aux_array, aux_dict = SampleWeight().calib_covariates(sample_cat, ["A", "B"], domain="Domain")
print(aux_array)

aux_dict["D1"]["A1_&_B1"] = 20
aux_dict["D1"]["A1_&_B2"] = 20
aux_dict["D1"]["A1_&_B3"] = 27.5
aux_dict["D1"]["A2_&_B1"] = 30
aux_dict["D1"]["A2_&_B2"] = 75
aux_dict["D1"]["A2_&_B3"] = 170
aux_dict["D1"]["A3_&_B1"] = 85
aux_dict["D1"]["A3_&_B2"] = 30
aux_dict["D1"]["A3_&_B3"] = 100
aux_dict["D1"]["A4_&_B1"] = 27.5
aux_dict["D1"]["A4_&_B2"] = 82.5
aux_dict["D1"]["A4_&_B3"] = 62.5

aux_dict["D2"]["A1_&_B1"] = 40
aux_dict["D2"]["A1_&_B2"] = 20
aux_dict["D2"]["A1_&_B3"] = 27.5
aux_dict["D2"]["A2_&_B1"] = 30
aux_dict["D2"]["A2_&_B2"] = 75
aux_dict["D2"]["A2_&_B3"] = 170
aux_dict["D2"]["A3_&_B1"] = 85
aux_dict["D2"]["A3_&_B2"] = 30
aux_dict["D2"]["A3_&_B3"] = 100
aux_dict["D2"]["A4_&_B1"] = 27.5
aux_dict["D2"]["A4_&_B2"] = 82.5
aux_dict["D2"]["A4_&_B3"] = 62.5

# print(aux_dict)
# print(sample_cat.groupby(["Domain", "A", "B"]).sum())

sample_cat["_calib_wgt"] = SampleWeight().calibrate(
    sample_cat["wgt"], aux_array, control=aux_dict, domain="Domain"
)
sample_cat["_calib_adjust_fct"] = sample_cat["_calib_wgt"] / sample_cat["wgt"]
print(sample_cat.drop_duplicates())

exit()

# All non-categorical
sample_num = pd.DataFrame(
    [
        [1, 1, 2, 8],
        [1, 2, 4, 4],
        [1, 3, 4, 5.5],
        [2, 1, 5, 6],
        [2, 2, 14, 15],
        [2, 3, 31, 34],
        [3, 1, 10, 17],
        [3, 2, 5, 6],
        [3, 3, 5, 20],
        [4, 1, 3, 5.5],
        [4, 2, 10, 16.5],
        [4, 3, 7, 12.5],
    ]
)
sample_num.rename(columns={0: "A", 1: "B", 2: "wgt", 3: "benchmark"}, inplace=True)
sample_num = pd.concat([sample_num] * 10, ignore_index=True)
sample_num.sort_values(by=["A", "B"], inplace=True)
domain = np.tile(["D1", "D2"], 60)
sample_num.insert(0, "Domain", domain)
# print(sample_num)

aux_dict = {}
aux_dict["A"] = 3945
aux_dict["B"] = 3355

# print((sum(sample_num["A"] * sample_num["benchmark"]), sum(sample_num["A"] * sample_num["wgt"])))
# print((sum(sample_num["B"] * sample_num["benchmark"]), sum(sample_num["B"] * sample_num["wgt"])))

aux_array_num = sample_num[["A", "B"]]
# print(aux_array_num.shape)

sample_num["_calib_wgt"] = SampleWeight().calibrate(
    sample_num["wgt"], aux_array_num, control=aux_dict
)
sample_num["_calib_adjust_fct"] = sample_num["_calib_wgt"] / sample_num["wgt"]
# print(sample_num.drop_duplicates())


def test_calibration_num():
    sample_num.drop_duplicates(["A", "B"], inplace=True)
    sample_num.sort_values(by=["A", "B"], inplace=True)
    assert np.isclose(
        sample_num["_calib_adjust_fct"].values,
        np.array(
            [
                1.196633,
                1.165079,
                1.133525,
                1.424819,
                1.393265,
                1.361711,
                1.653006,
                1.621452,
                1.589898,
                1.881192,
                1.849638,
                1.818084,
            ]
        ),
    ).all()


# Mixed (categorical andnon-vategorical)
sample_mix = pd.DataFrame(
    [
        ["A1", 1, 2, 8],
        ["A1", 2, 4, 4],
        ["A1", 3, 4, 5.5],
        ["A2", 1, 5, 6],
        ["A2", 2, 14, 15],
        ["A2", 3, 31, 34],
        ["A3", 1, 10, 17],
        ["A3", 2, 5, 6],
        ["A3", 3, 5, 20],
        ["A4", 1, 3, 5.5],
        ["A4", 2, 10, 16.5],
        ["A4", 3, 7, 12.5],
    ]
)
sample_mix.rename(columns={0: "A", 1: "B", 2: "wgt", 3: "benchmark"}, inplace=True)
sample_mix = pd.concat([sample_mix] * 10, ignore_index=True)
sample_mix.sort_values(by=["A", "B"], inplace=True)
domain = np.tile(["D1", "D2"], 60)
sample_mix.insert(0, "Domain", domain)
# print(sample_mix.head(25))

aux_array, aux_dict = SampleWeight().calib_covariates(sample_mix, ["A"], ["B"])
# print(aux_array)

aux_dict["A1"] = 175
aux_dict["A2"] = 550
aux_dict["A3"] = 430
aux_dict["A4"] = 345
aux_dict["B"] = 3355


sample_mix["_calib_wgt"] = SampleWeight().calibrate(sample_mix["wgt"], aux_array, control=aux_dict)
sample_mix["_calib_adjust_fct"] = sample_mix["_calib_wgt"] / sample_mix["wgt"]

# print(sample_mix.drop_duplicates())

sum_by_mix = sample_mix.groupby("A").sum()
sum_by_mix.reset_index(inplace=True)
# print(sum_by_mix[["A", "wgt", "benchmark", "_calib_wgt"]])
# print((sum(sample_mix["B"] * sample_mix["benchmark"]), sum(sample_mix["B"] * sample_mix["wgt"])))


def test_calibration_mix():
    sample_mix.drop_duplicates(["A", "B"], inplace=True)
    sample_mix.sort_values(by=["A", "B"], inplace=True)
    assert np.isclose(
        sample_mix["_calib_adjust_fct"].values,
        np.array(
            [
                1.579512,
                1.721585,
                1.863659,
                0.884049,
                1.026122,
                1.168195,
                2.043445,
                2.185518,
                2.327592,
                1.554512,
                1.696585,
                1.838659,
            ]
        ),
    ).all()
