import pandas as pd

class ImNodeData(object):
    def __init__(self, row):
        self.rowNumber = row[0]
        self.Level = int(row[1].Level[0])
        self.levelName = row[1].Level[2:]
        self.ExposureAmount = row[1].ExposureAmount
        if self.Level == 1:
            self.manifestation = 'Total'
        elif self.Level == 2:
            self.manifestation = row[1]['Im Model']
        elif self.Level == 3:
            self.manifestation = row[1]['Silo']
        elif self.Level == 4:
            self.manifestation = row[1]['RiskClass']
        elif self.Level == 5:
            self.manifestation = row[1]['SensitivityType']
        elif self.Level == 6:
            self.manifestation = row[1]['Bucket']
        elif self.Level == 7:
            self.manifestation = row[1]['WeightedSensitivity']
        self.identifier = ''
        for i in range(1, self.Level):
            if self.identifier == '':
                self.identifier = self.identifier + row[1][i]
            else:
                self.identifier = self.identifier + '_' + row[1][i]

    def __str__(self):
        return self.manifestation + ' ' + '%.0f' % self.ExposureAmount