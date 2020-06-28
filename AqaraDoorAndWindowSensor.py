from typing import Dict, Union
from core.base.model.AliceSkill import AliceSkill

try:
	from skills.Zigbee2Mqtt.model.ZigbeeDeviceHandler import ZigbeeDeviceHandler
except:
	pass


class AqaraDoorAndWindowSensor(AliceSkill):
	"""
	Author: Psychokiller1888
	Description: Connect your aqara door and window sensors to alice. requires zigbee2mqtt
	"""

	def __init__(self):
		super().__init__()
		self._handler = None
		self._state = None
		self._battery = None
		self._linkQuality = None


	def onStart(self):
		super().onStart()
		self._handler = ZigbeeDeviceHandler(skillInstance=self.onDeviceMessage, modelId='lumi.sensor_magneet.aq2')


	def onBooted(self) -> bool:
		return self._handler.onBooted()


	def onDeviceMessage(self, message: Union[str, Dict]):
		if 'contact' in message:
			self._state = message['contact']

		print(f'my state is {self._state}')

		if 'battery' in message:
			self._battery = message['battery']

		if 'linkquality' in message:
			self._linkQuality = message['linkquality']


	@property
	def state(self) -> bool:
		return self._state


	@property
	def battery(self) -> int:
		return self._battery
