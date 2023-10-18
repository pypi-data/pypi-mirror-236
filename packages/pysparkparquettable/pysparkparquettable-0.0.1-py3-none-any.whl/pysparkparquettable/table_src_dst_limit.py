from pysparkparquettable import TableSrcDst

class TableSrcDstLimit(TableSrcDst):

    def __init__(self, 
        table_src,
        table_dst,
        limit = 1
    ):
        super().__init__(
            table_src = table_src,
            table_dst = table_dst,
        )
        
        self.limit = limit
    
    def dst_df_from_src_df_file(self, src_df, src_file):
        src_df = src_df.limit(1)
        dst_df = super().dst_df_from_src_df_file(src_df, src_file)
        return dst_df









