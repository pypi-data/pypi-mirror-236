from SimpleSLACalc import SLACalculator

my_sla_cal = SLACalculator()
sla_value = my_sla_cal.calculate(
    start_time="2023-10-18 01:27:30", open_hour=9, close_hour=17, sla_hours=6, time_zone="America/Chicago", skip_business_hours=False
)

print(sla_value.sla_expiration_time)
