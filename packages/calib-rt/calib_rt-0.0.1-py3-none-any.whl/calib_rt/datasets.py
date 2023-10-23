# -*- coding:utf-8 -*-

'''
data sets for calib_rt

.. calib_rt:
    url

'''
import pandas as pd

class RTsets(object):
    """
    """
    info = {
        "distort_left":('fmeierab_T190525_CLL_diaPASEF_04_1979.d.npz',
                        'fmeierab_T190525_CLL_diaPASEF_40_1965.d.npz'),
        "distort_right":('20200505_Evosep_100SPD_SG06-16_MLHeLa_100ng_py8_S2-C1_1_2731.d.npz',
                         '20211103_PRO2_LS_01_MA_HeLa_200_SDC_NS_RE2_1_1418.d.npz'),
        "exp":('SC_HeLa_10min1_Slot1-9_1_807.d.npz',
               'SC_HeLa_15min1_Slot1-7_1_805.d.npz'),
        "linear":('20211101_PRO2_LS_04_MA_HeLaSCS_0.2_ngHS_GE2_1_1408.d.npz',
                  '20220714_10ngK562_ZI_500ul60C3cm5min_P1-C1_1_9675.d.npz'),
        "S":('20200505_Evosep_200SPD_SG06-16_MLHeLa_200ng_py8_S3-A1_1_2737.d.npz',
             'CMs_Subject3_Lvmid_G10_BG11_1_7560.d.npz')
    }
    def __init__(self,) -> None:
        pass

    def get_pandas() -> pd.DataFrame:
        pass