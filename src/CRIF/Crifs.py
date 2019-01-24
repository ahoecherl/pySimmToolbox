from CRIF.Crif import Crif

class Crifs(dict):

    def __init__(self, CRIFsdataframe):
        CRIFs = CRIFsdataframe[['IMLedis', 'CollectRegulations', 'PostRegulations']].drop_duplicates()
        for row in CRIFs.itertuples():
            identifier = tuple([row[1],
                          row[2],
                          row[3]])
            CrifFrame = CRIFsdataframe[(CRIFsdataframe.IMLedis == row[1])
                                            & (CRIFsdataframe.CollectRegulations == row[2])
                                            & (CRIFsdataframe.PostRegulations == row[3])]
            thisCrif = Crif(CrifFrame)
            self[str(thisCrif)] = thisCrif