from datetime import datetime

from SimpleSLACalc import SLACalculator

my_sla_cal = SLACalculator()
current_time = datetime.now()
sla_value = my_sla_cal.calculate(
    start_time=current_time, open_hour=9, close_hour=17, sla_hours=6, time_zone="America/Chicago", skip_business_hours=False
)
print(sla_value.sla_expiration_time)
