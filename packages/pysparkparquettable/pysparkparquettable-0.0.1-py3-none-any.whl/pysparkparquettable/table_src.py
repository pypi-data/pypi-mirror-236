from pysparkparquettable import Table

import pyspark.sql.functions as F

class TableSrc(Table):
    
    def __init__(self, paths, filename_colname = 'filename', clean_filename_colname = 'clean_filename'):
        super().__init__(paths)
        self.filename_colname = filename_colname
        self.clean_filename_colname = clean_filename_colname
        
    def col_filename_from_file(self, file):
        return F.expr('"' + file + '" AS ' + self.filename_colname)

    def col_clean_filename_from_file(self, file):
        return F.expr('"' + file.replace('/', '__').replace('=', '_eq_').replace(':', ' ') + '" AS ' + self.clean_filename_colname)

    def cols_from_df_file(self, df, file):
        return ['*', self.col_filename_from_file(file), self.col_clean_filename_from_file(file)]





