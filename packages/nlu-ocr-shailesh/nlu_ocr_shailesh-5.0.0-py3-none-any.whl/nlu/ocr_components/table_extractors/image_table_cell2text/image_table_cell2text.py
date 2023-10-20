class ImageTable2Cell2TextTable:
    @staticmethod
    def get_default_model():
        from sparkocr.transformers import ImageCellsToTextTable
        return ImageCellsToTextTable() \
            .setInputCol("image_region") \
            .setCellsCol('ocr_table_3')\
            .setOutputCol("table")

#             .setCellsCol('ocr_table_3')
