import gzip
import os
from io import BytesIO
from zipfile import ZipFile

from filelock import FileLock
from os.path import exists

from cameo_claw.cameo_claw_reuse import bytesio_to_gzip, requests_get_write, \
    pl_read_csv_distinct, groupby_write_gzip, it_f, condition_filter_sort, distinct_filter_sort, \
    bytesio_filename, write_gzip, df_write_gzip, condition, df_write_csv
import polars as pl

from cameo_claw.file import mkdir
from cameo_claw.functional import it_mp_f
from cameo_claw.net import requests_get_bytes, url_to_filename
from glob import glob
from functools import lru_cache


def a_download(url, target_directory):
    def write(bytes1):
        filename = os.path.basename(url)
        path = f'{target_directory}{filename}'
        with open(path, 'wb') as f:
            f.write(bytes1)
        return url

    return requests_get_write(write, target_directory, url)


def it_download(lst_url, target_directory):
    return it_mp_f(a_download, [tuple([url, target_directory]) for url in lst_url])


def a_distinct(url, target_directory, lst_distinct_column):
    def write(bytes1):
        df = pl_read_csv_distinct(bytes1, lst_distinct_column)
        return bytesio_to_gzip(df, url, target_directory)

    return requests_get_write(write, target_directory, url)


def it_distinct(lst_url, target_directory, lst_distinct_column):
    return it_mp_f(a_distinct, [tuple([url, target_directory, lst_distinct_column]) for url in lst_url])


def a_group(url, target_directory, lst_distinct_column, lst_group_by_column):
    def write(bytes1):
        df = pl_read_csv_distinct(bytes1, lst_distinct_column)
        return groupby_write_gzip(df, url, lst_group_by_column, target_directory)

    return requests_get_write(write, target_directory, url)


def it_group(lst_url, target_directory, lst_distinct_column, lst_group_by_column):
    return it_mp_f(a_group,
                   [tuple([url, target_directory, lst_distinct_column, lst_group_by_column]) for url in lst_url])


def a_filter(url, target_directory, lst_distinct_column, lst_column_match=[], sort_column=''):
    def write(bytes1):
        df = distinct_filter_sort(bytes1, lst_distinct_column, lst_column_match, sort_column)
        bytesio_to_gzip(df, url, target_directory)
        return url

    return requests_get_write(write, target_directory, url)


def it_filter(lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column):
    return it_f(a_filter, lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column)


def a_chunk_pl_lst(url, target_directory, lst_distinct_column, lst_column_match, sort_column):
    tup_distinct_column = tuple(lst_distinct_column)
    tup_lst_column_match = tuple([tuple(l) for l in lst_column_match])
    return a_chunk_pl_tup(url, target_directory, tup_distinct_column, tup_lst_column_match, sort_column)


@lru_cache(maxsize=5000)
def a_chunk_pl_tup(url, target_directory, tup_distinct_column, tup_column_match, sort_column):
    def write(bytes1):
        df = pl.read_csv(bytes1)
        df = df.distinct(subset=list(tup_distinct_column))
        df = condition_filter_sort(df, tup_column_match, sort_column)
        bytesio_csv = BytesIO()
        df.to_csv_gz(bytesio_csv, has_header=False)
        bytesio_gzip = BytesIO()
        with gzip.open(bytesio_gzip, 'wb') as f:
            f.write(bytesio_csv.getvalue())
        return bytesio_gzip.getvalue()

    return requests_get_write(write, target_directory, url)


def it_chunk_pl(lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column):
    return it_f(a_chunk_pl_lst, lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column)


def a_filter_group(url, target_directory, lst_distinct_column, lst_column_match=[], sort_column='',
                   lst_group_by_column=[]):
    def write(bytes1):
        df = distinct_filter_sort(bytes1, lst_distinct_column, lst_column_match, sort_column)
        return groupby_write_gzip(df, url, lst_group_by_column, target_directory)

    return requests_get_write(write, target_directory, url)


def it_filter_group(lst_url, target_directory, lst_distinct_column,
                    lst_column_match, sort_column, lst_group_by_column):
    return it_mp_f(a_filter_group,
                   [tuple([url, target_directory, lst_distinct_column,
                           lst_column_match, sort_column, lst_group_by_column]) for url in lst_url])


def a_filter_group_append(url, target_directory, lst_distinct_column, lst_column_match,
                          sort_column, lst_group_by_column, append_column, column_header):
    def write(bytes1):
        df = distinct_filter_sort(bytes1, lst_distinct_column, lst_column_match, sort_column)
        g = df.groupby(lst_group_by_column)
        for df in g:
            bytesio = BytesIO()
            df_write_csv(df, bytesio, has_header=False)
            path = f'{target_directory}{append_column}_{str(df.row(0)[df.find_idx_by_name(append_column)])}.csv.gz'
            with FileLock(f'{path}.lock', timeout=60 * 60 * 2):
                if not exists(path):
                    with gzip.open(path, 'wb') as f:
                        f.write(column_header.encode('utf-8'))
                write_gzip(bytesio, path, 'ab')
        return url

    return requests_get_write(write, target_directory, url)


import hashlib


def it_filter_group_append(lst_url, target_directory, lst_distinct_column, lst_column_match,
                           sort_column, lst_group_by_column, append_column, column_header):
    return it_mp_f(a_filter_group_append,
                   [tuple([url, target_directory, lst_distinct_column,
                           lst_column_match, sort_column, lst_group_by_column, append_column, column_header]) for url in
                    lst_url])


def a_filter_group_mean_count(url, target_directory, lst_distinct_column,
                              lst_column_match, sort_column, lst_group_by_column,
                              time_column, value_column):
    def write(bytes1):
        df = distinct_filter_sort(bytes1, lst_distinct_column, lst_column_match, sort_column)
        for df in df.groupby(lst_group_by_column):
            filename_tail = df_write_gzip(df, True, lst_group_by_column, target_directory, url)
            df_mean_daily = (
                df.lazy()
                    .groupby(lst_group_by_column)
                    .agg(
                    [
                        pl.first('localTime'),
                        pl.col(value_column).mean(),
                    ]
                )
            ).collect()
            bytesio, filename = bytesio_filename(df_mean_daily, url)
            path = f'{target_directory}{filename}{filename_tail}_mean_daily.csv.gz'
            write_gzip(bytesio, path)

    return requests_get_write(write, target_directory, url)


def it_filter_group_mean_count(lst_url, target_directory, lst_distinct_column,
                               lst_column_match, sort_column, lst_group_by_column,
                               time_column, value_column):
    return it_mp_f(a_filter_group_mean_count,
                   [tuple([url, target_directory, lst_distinct_column,
                           lst_column_match, sort_column, lst_group_by_column,
                           time_column, value_column]) for url in lst_url])


def md5_hex(d):
    return hashlib.md5(str(d).encode('utf-8')).hexdigest()


# def cache_directory(d):
#     return d['target_directory'] + f'{md5_hex(d)}/'


def zip_cache_path(d):
    hash = md5_hex(d)
    return d['target_directory'] + f'{hash}/{hash}.zip'


def read_csv(url):
    return pl.read_csv(requests_get_bytes(url), infer_schema_length=20000)


def distinct(df, lst_distinct_column):
    return df.distinct(subset=lst_distinct_column, keep='last')


def filter(df, lst_column_match):
    return df.filter(eval(condition(lst_column_match)))


def sort(df, sort_column):
    return df.sort(sort_column)


def groupby(df, lst_group_by_column):
    return df.groupby(lst_group_by_column)


def append_csv_hash(df, target_directory, append_column, column_header, hash_path):
    mkdir(target_directory + hash_path)
    bytesio = BytesIO()
    df_write_csv(df, bytesio, has_header=False)
    path = f"{target_directory}{hash_path}/{append_column}_{str(df.row(0)[df.find_idx_by_name(append_column)])}.csv.gz"
    with FileLock(f'{path}.lock', timeout=60 * 60 * 2):
        if not exists(path):
            with gzip.open(path, 'wb') as f:
                f.write(column_header.encode('utf-8'))
        write_gzip(bytesio, path, 'ab')
    return path


def append_csv(df, d):
    hash_path = md5_hex(d)
    return append_csv_hash(df, d['target_directory'], d['append_column'], d['column_header'], hash_path)


def pipe(f, lst, dic, is_lock=True):
    yield from it_mp_f(f, [tuple([item, dic]) for item in lst], is_lock)


def zip_path(target_directory):
    path = target_directory + target_directory[target_directory.rfind('/', 0, -1) + 1:-1] + '.zip'
    return path


def make_zip(wildcard_source_path, target_path):
    with ZipFile(target_path, 'w') as f:
        for target_path in glob(wildcard_source_path):
            f.write(target_path)
    return target_path


def has_zip_cache(d):
    return exists(zip_cache_path(d))


def zip_cache(d):
    wildcard_source_path = f"{d['target_directory']}{md5_hex(d)}/*.csv.gz"
    if not glob(wildcard_source_path):
        return None
    return make_zip(wildcard_source_path, zip_cache_path(d))


def to_csv_gz(df, target_directory, url, lst_group_by_column):
    mkdir(target_directory)
    filename_tail = '_group_' + '-'.join(list(
        map(lambda column: str(df.row(0)[df.find_idx_by_name(column)]).replace('_', '-'), lst_group_by_column)))
    bytesio, filename = bytesio_filename(df, url, has_header=True)
    path = f'{target_directory}{filename}{filename_tail}.csv.gz'
    return write_gzip(bytesio, path)


def to_parquet(df, target_directory, url, lst_group_by_column):
    mkdir(target_directory)
    filename_tail = '_group_' + '-'.join(list(
        map(lambda column: str(df.row(0)[df.find_idx_by_name(column)]).replace('_', '-'), lst_group_by_column)))
    filename = url_to_filename(url)
    path = f'{target_directory}{filename}{filename_tail}.parquet'
    df.write_parquet(path, compression='snappy')
    return True
