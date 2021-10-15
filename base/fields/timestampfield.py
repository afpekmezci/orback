from rest_framework import serializers
from core.utils import TimeUtils
class TimestampField(serializers.Field):


	def to_representation(self, value):
		return round(value.timestamp() * 1000)

	def to_internal_value(self, data):
		print('DATA : ', data)
		data = round(data / 1000, 0)
		return TimeUtils().recalculate_time_wtih_tz(data)



