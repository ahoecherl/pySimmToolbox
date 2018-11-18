class Crifs():

    def __init__(self, CRIFsdataframe):
        self.asDataFrame = CRIFsdataframe
        CRIFs = CRIFsdataframe[['IMLedis', 'CollectRegulations', 'PostRegulations']]