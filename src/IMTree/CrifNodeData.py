class CrifNodeData(object):
    def __init__(self, row):
        self.Level = int(row[1].Level[0])
        self.levelName = row[1].Level[2:]
        self.value = row[1].ExposureAmount
        if self.Level == 1:
            self.manifestation = 'Total'
        if self.Level == 2:
            self.manifestation = row[1]['Im Model']
        if self.Level == 3:
            self.manifestation = row[1]['Silo']
        if self.Level == 4:
            self.manifestation = row[1]['RiskClass']
        if self.Level == 5:
            self.manifestation = row[1]['SensitivityType']
        if self.Level == 6:
            self.manifestation = row[1]['Bucket']
        if self.Level == 7:
            self.manifestation = row[1]['WeightedSensitivity']

    def __str__(self):
        return self.manifestation + ' ' + '%.0f' % self.value