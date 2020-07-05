import sqlite3

from core.commons import constants
from core.device.model import Device
from core.device.model.DeviceType import DeviceType
from core.dialog.model.DialogSession import DialogSession


class AqaraDoorAndWindowSensor(DeviceType):

	def __init__(self, data: sqlite3.Row):
		super().__init__(data)
		self._timeout = None


	def getDeviceIcon(self, device: Device) -> str:
		if not device.connected:
			return 'aqara_offline.png'

		if device.getCustomValue('open'):
			return 'aqara_open.png'
		else:
			return 'aqara_close.png'


	def toggle(self, device: Device):
		pass # Nothing to be done if clicked on the interface


	def discover(self, device: Device, uid: str, replyOnSiteId: str = '', session: DialogSession = None) -> bool:
		self.broadcast(method=constants.EVENT_BROADCASTING_FOR_NEW_DEVICE, exceptions=[self.name], propagateToSkills=True)
		self._timeout = self.ThreadManager.newTimer(interval=300, func=self.discoverFailed, args=[replyOnSiteId])

		server = self.SkillManager.getSkillInstance('Zigbee2Mqtt')
		if not server:
			return False

		server.allowNewDeviceJoining()

		return True


	def onDeviceDiscovered(self, device: Device, uid: str):
		device.pairingDone(uid=uid)


	def discoverFailed(self, replyOnSiteId: str = None):
		self.broadcast(method=constants.EVENT_STOP_BROADCASTING_FOR_NEW_DEVICE, exceptions=[self.name], propagateToSkills=True)

		if replyOnSiteId:
			self.MqttManager.say(text=self.TalkManager.randomTalk('newDeviceAdditionFailed'), client=replyOnSiteId)

		server = self.SkillManager.getSkillInstance('Zigbee2Mqtt')
		if not server:
			return False

		server.blockNewDeviceJoining()
