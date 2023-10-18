from pysparkparquettable import Table

from pysparkparquethelper import PySparkParquetHelper

import pyspark.sql.functions as F

import gc

class TableDst(Table):
    
    def __init__(self, basepath, part_colnames):
        super().__init__([basepath])
        self.basepath = basepath
        self.part_colnames = part_colnames

    def write_df(self, df):
        self.logger().debug(f'#beg# write_df')
        
        PySparkParquetHelper.write_df(df, self.basepath, self.part_colnames)
        gc.collect()
        
        self.logger().debug(f'#end# write_df')





