import matplotlib.pyplot as plt
import pandas as pd
from numpy import object


def update_plot_params():
    params = {'legend.fontsize': 'x-large',
              'figure.figsize': (10, 8),
              'axes.labelsize': 'x-large',
              'axes.titlesize': 'x-large',
              'xtick.labelsize': 'x-large',
              'ytick.labelsize': 'x-large'}
    plt.rcParams.update(params)


def cv2df(cv_score, calculate_mean=False, col_idx=None):
    """
    Convert cross validation scores to pandas.DataFrame
    """
    df = pd.DataFrame(cv_score)
    df = df.append(df.mean(axis=0), ignore_index=True)
    df.index.name = 'n_folds'
    df.index = df.index + 1
    if calculate_mean:
        assert type(col_idx) == int
        df = df.rename(index={col_idx: 'Mean'})
    return df


def numeric2bool(df, inplace=False):
    """
    Convert columns with numerical dtypes to boolean
    """
    if not inplace:
        df = df.copy()
    num_cols = df.select_dtypes(float).columns
    df.loc[:, num_cols] = df.loc[:, num_cols].astype(bool).astype(int)
    return df


def object2str(df, inplace=False, str_to_bool=False):
    """
    Convert columns with objects dtypes to str (or bool)
    """
    if not inplace:
        df = df.copy()
    if not str_to_bool:
        def lmbd(x): return x.str.decode('utf-8')
    else:
        def lmbd(x): return x.str.decode("utf-8").astype(int)
    obj_cols = df.select_dtypes([object]).columns
    df.loc[:, obj_cols] = df.loc[:, obj_cols].apply(lmbd)
    return df


def str2cat(df, inplace=False, save_code_labels=True):
    """
    Convert str columns to categorical 
    """
    if not inplace:
        df = df.copy()
    if save_code_labels:
        code_labels = []

        def get_code_labels(series, storage_list):
            codes, labels = series.factorize()
            storage_list.append((series.name, dict(zip(set(codes), labels))))
            return codes

        def lmbd(x): return get_code_labels(x, code_labels)
    else:
        def lmbd(x): return x.astype('categorical').cat.codes
    obj_cols = df.select_dtypes([object]).columns
    df.loc[:, obj_cols] = df.loc[:, obj_cols].apply(lmbd)
    return df if not save_code_labels else df, code_labels

