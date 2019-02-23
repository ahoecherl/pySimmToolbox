import os
pathname = os.path.dirname(os.path.abspath(__file__))+'\\simm.jar'
os.environ['CLASSPATH'] = pathname

from jnius import autoclass

#Java Classes
String = autoclass('java.lang.String')
BigDecimal = autoclass('java.math.BigDecimal')
LocalDate = autoclass('java.time.LocalDate')
Arrays = autoclass('java.util.Arrays')
ArrayList = autoclass('java.util.ArrayList')

#SimmLib Classes
Simm = autoclass('com.acadiasoft.im.simm.engine.Simm')
Schedule = autoclass('com.acadiasoft.im.schedule.engine.Schedule')
GenerateCsvString = autoclass('com.acadiasoft.im.base.imtree.GenerateCsvString')
Sensitivity = autoclass('com.acadiasoft.im.simm.model.Sensitivity')
ProductMultiplier = autoclass('com.acadiasoft.im.simm.model.ProductMultiplier')
AddOnNotionalFactor = autoclass('com.acadiasoft.im.simm.model.AddOnNotionalFactor')
AddOnFixedAmount = autoclass('com.acadiasoft.im.simm.model.AddOnFixedAmount')
AddOnNotional = autoclass('com.acadiasoft.im.simm.model.AddOnNotional')
ScheduleNotional = autoclass('com.acadiasoft.im.schedule.models.ScheduleNotional')
ScheduleProductClass = autoclass('com.acadiasoft.im.schedule.models.imtree.identifiers.ScheduleProductClass')
SchedulePv = autoclass('com.acadiasoft.im.schedule.models.SchedulePv')