from logclshelper import LogClsHelper
from pysparkhdfshelper import PySparkHdfsHelper

class TableSrcDst(LogClsHelper):
    
    def __init__(self, 
        table_src,
        table_dst
    ):
        self.table_src = table_src
        self.table_dst = table_dst

        self._processed_src_files = None
        self._unprocessed_src_files = None

    def processed_src_files(self):
        if(self._processed_src_files is None):

            self.logger().debug('#beg# processed_src_files is None')
            
            if(PySparkHdfsHelper.exists(self.table_dst.basepath)):
                df = self.table_dst.df_from_file(self.table_dst.basepath)
                self._processed_src_files = {
                    filename
                    for row in df.select(self.table_src.filename_colname).distinct().collect()
                    for filename in row[self.table_src.filename_colname].split(':')
                }
            else:
                self._processed_src_files = set()

            self.logger().debug(f'#end# processed_src_files {len(self._processed_src_files)}')
        
        return self._processed_src_files 

    def unprocessed_src_files(self):
        if(self._unprocessed_src_files is None):

            self.logger().debug('#beg# unprocessed_src_files is None')
            
            processed_files = self.processed_src_files()
            self._unprocessed_src_files = [file for file in self.table_src.files() if file not in processed_files]

            self.logger().debug(f'#end# unprocessed_src_files {len(self._unprocessed_src_files)}')
            
        return self._unprocessed_src_files

    def dst_df_from_src_df_file(self, src_df, src_file):
        dst_df = src_df.select(*self.table_src.cols_from_df_file(src_df, src_file))
        return dst_df
           
    def dst_df_from_src_file(self, src_file):
        src_df = self.table_src.df_from_file(src_file)
        dst_df = self.dst_df_from_src_df_file(src_df, src_file) 
        return dst_df
    
    def dst_df_from_src_files_chunk(self, src_files_chunk):
        src_df = self.table_src.df_from_files_chunk(src_files_chunk)
        joined_src_files_chunk = ':'.join(src_files_chunk)
        dst_df = self.dst_df_from_src_df_file(src_df, joined_src_files_chunk)
    
    def yield_dst_dfs_from_src_files_chunk(self, src_files_chunk):
        for src_file in src_files_chunk:
            yield self.dst_df_from_src_file(src_file)
        
    def dst_df_from_src_files_chunk_by_union_dfs(self, src_files_chunk):
        return PySparkParquetHelper.union_dfs_by_name(self.yield_dst_dfs_from_src_files_chunk(src_files_chunk))
    
    def write_dst_df(self, dst_df):
        self.logger().debug(f'#beg# write_dst_df')
        
        self.table_dst.write_df(dst_df)
        
        self.logger().debug(f'#end# write_dst_df')
                
    def write_dst_df_from_src_files_chunk(self, src_files_chunk):
        self.logger().debug(f'#beg# write_dst_df_from_src_files_chunk')
        
        dst_df = self.dst_df_from_src_files_chunk(src_files_chunk)
        self.write_dst_df(dst_df)
        
        self.logger().debug(f'#end# write_dst_df_from_src_files_chunk')
        
    def write_dst_dfs_from_src_files_chunk(self, src_files_chunk):
        self.logger().debug(f'#beg# write_dst_dfs_from_src_files_chunk')
        
        dst_dfs = self.yield_dst_dfs_from_src_files_chunk(src_files_chunk)
        for dst_df in dst_dfs:
            self.write_dst_df(dst_df)
            
        self.logger().debug(f'#end# write_dst_dfs_from_src_files_chunk')
            
    def write_dst_df_from_src_files_by_union_dfs(self, src_files_chunk):
        self.logger().debug(f'#beg# write_dst_df_from_src_files_by_union_dfs')
            
        dst_df = self.dst_df_from_src_files_chunk_by_union_dfs(src_files_chunk)
        self.write_dst_df(dst_df)
            
        self.logger().debug(f'#end# write_dst_df_from_src_files_by_union_dfs')
        
    def run(self, src_files_chunk):
        self.logger().debug(f'#beg# run')
        
        self.write_dst_dfs_from_src_files_chunk(src_files_chunk)
        
        self.logger().debug(f'#end# run')

    def run_unprocessed_src_files(self):
        self.logger().debug(f'#beg# run_unprocessed_src_files')
        
        self.run(self.unprocessed_src_files())

        self.logger().debug(f'#end# run_unprocessed_src_files')



