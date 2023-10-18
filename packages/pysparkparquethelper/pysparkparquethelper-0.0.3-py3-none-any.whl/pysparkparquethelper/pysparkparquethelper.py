from logclshelper import LogClsHelper
from pysparkhelper import PySparkHelper
from pysparkhdfshelper import PySparkHdfsHelper
import itertools
import re

class PySparkParquetHelper(LogClsHelper):
    
    @classmethod
    def get_files_from_path(cls, path, extension = '.parquet'):        
        files = PySparkHdfsHelper.yield_filtered_paths(
            parent_dir = path, 
            accept_dirs = False,
            lambda_filter_path = lambda p : p.endswith(extension)
        )        
        return files
        
    @classmethod
    def get_files_from_paths(cls, paths, extension = '.parquet'):        
        files = (
            itertools.chain(
                *(
                    cls.get_files_from_path(path, extension = extension)
                    for path in paths
                )
            )
        )
        return files

    @classmethod
    def get_part_name_value_list_from_path(cls, path):
        valid_pattern='([^/]+)'
        part_pattern = f'({valid_pattern}={valid_pattern})'
        matches = re.findall(part_pattern, path)
        return matches

    @classmethod
    def get_part_names_from_path(cls, path):
        part_name_value_list = cls.get_part_name_value_list_from_path(path)
        part_names = [part_name_value[1] for part_name_value in part_name_value_list]
        return part_names
        
    @classmethod
    def get_part_value_from_path_part_name(cls, path, part_name = '(?s:.*)'):   
        group1 = f'({part_name})'
        group2 = '([^/]+)'
        pattern = f'{group1}={group2}'
        match = re.search(pattern, path)
        return match.group(2) if(match) else None 
    
    @classmethod
    def get_last_part_value_from_path(cls, path):
        return cls.get_part_value_from_path_part_name(path, part_name = '(?s:.*)')
    
    @classmethod
    def sort_paths_by_last_part_value(cls, paths):
        cls.logger().debug(f'#beg# sort_paths_by_last_part_value')
        
        sorted_paths = sorted(paths, key = lambda f : cls.get_last_part_value_from_path(f))
    
        cls.logger().debug(f'#end# sort_paths_by_last_part_value {len(sorted_paths)}')
    
        return sorted_paths
    
    @classmethod
    def get_sorted_files_by_last_part_value_from_paths(cls, paths):
        #cls.logger().debug(f'#beg# get_sorted_files_by_last_part_value_from_paths')
        
        files = cls.get_files_from_paths(paths)
        sorted_files = cls.sort_paths_by_last_part_value(files)
        
        #cls.logger().debug(f'#end# get_sorted_files_by_last_part_value_from_paths {len(sorted_files)}')

        return sorted_files
        
    @classmethod
    def get_basepath_from_path(cls, path):
        valid_pattern='([a-z|A-Z|0-9|-|_]*)'
        basepath_pattern = '([a-z|A-Z|0-9|-|_|/|:]+)'
        part_pattern = f'({valid_pattern}={valid_pattern})'
        pattern = f'{basepath_pattern}/{part_pattern}'
        match = re.search(pattern, path)
        
        if(match):
            basepath = match.group(1)
        else:
            basepath = path
            
        return basepath
    
    @classmethodfile
    def read_parquet_from_file(cls, file):
        cls.logger().debug(f'#beg# read_parquet_from_file {file}')
        
        df = (
            PySparkHelper.get_or_create_spark()
            .read
            .option('basePath', cls.get_basepath_from_path(file))
            .option('mergeSchema', 'true')
            .parquet(file)
        )
        
        cls.logger().debug(f'#end# read_parquet_from_file {file}')
        
        return df
    
    @classmethod
    def read_parquet_from_files_chunk(cls, files_chunk):
        cls.logger().debug(f'#beg# read_parquet_from_files_chunk {len(files_chunk)}')
        
        df = (
            PySparkHelper.get_or_create_spark()
            .read
            .option('basePath', cls.get_basepath_from_path(next(files_chunk)))
            .option('mergeSchema', 'true')
            .parquet(*files_chunk)
        )
        
        cls.logger().debug(f'#end# read_parquet_from_files_chunk {len(files_chunk)}')
        
        return df
    
    @classmethod
    def union_dfs_by_name(cls, dfs):
        cls.logger().debug('#beg# union_dfs_by_name')
        
        df = ft.reduce(lambda df1, df2 : df1.unionByName(df2, allowMissingColumns = True), dfs)
        
        cls.logger().debug('#end# union_dfs_by_name')
        
        return df
    
    @classmethod
    def write_df(cls, df, path, partition_by_colnames):
        cls.logger().debug(f'#beg# write_df {path, partition_by_colnames}')
        
        (
            df
            .repartition(* partition_by_colnames)
            .write
            .mode('overwrite')
            .option("partitionOverwriteMode", "dynamic")
            .partitionBy(* partition_by_colnames)
            .format('parquet')
            .save(path)
        )
        
        cls.logger().debug(f'#end# write_df {path, partition_by_colnames}')

