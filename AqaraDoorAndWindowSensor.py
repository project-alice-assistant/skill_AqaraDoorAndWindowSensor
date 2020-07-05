from typing import Dict, Optional, Union

from core.base.model.AliceSkill import AliceSkill

try:
	from skills.Zigbee2Mqtt.model.ZigbeeDeviceHandler import ZigbeeDeviceHandler
except:
	# Required skill is not installed
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


	def onBooted(self) -> bool:
		server = self.SkillManager.getSkillInstance('Zigbee2Mqtt')
		if not server:
			self.logWarning('Requiring Zigbee2Mqtt but it is not available')
			self.SkillManager.deactivateSkill(self.name)
			return False

		self._handler = server.subscribe(deviceType='xiaomi_MCCGQ11LM', onMessageCallback=self.onDeviceMessage)


	def onDeviceMessage(self, message: Union[str, Dict]):
		if 'contact' in message:
			self._state = message['contact']

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
