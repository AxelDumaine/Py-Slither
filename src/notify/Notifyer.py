import string

class Notifyer:

	servingClass = None
	NOTIFY = 'NOTIFY'
	DEBUG = 'DEBUG'
	WARNING = 'WARNING'
	ERROR = 'ERROR'

	@staticmethod
	def parseString(string):
		if string == '' and len(string) == 0:
			return False

		return True

	@classmethod
	def setupClassNotify(cls, className):
		cls.servingClass = className
		return cls

	@classmethod
	def setNotifyInfo(cls, string):
		if cls.parseString(string) == False:
			return

		print ('%s: %s:: %s' % (cls.servingClass, cls.NOTIFY, string))

	@classmethod
	def setNotifyDebug(cls, string):
		if cls.parseString(string) == False:
			return

		print ('%s: %s:: %s' % (cls.servingClass, cls.DEBUG, string))

	@classmethod
	def setNotifyWarning(cls, string):
		if cls.parseString(string) == False:
			return

		print ('%s: %s:: %s' % (cls.servingClass, cls.WARNING, string))

	@classmethod
	def setNotifyError(cls, string):
		if cls.parseString(string) == False:
			return

		print ('%s: %s:: %s' % (cls.servingClass, cls.ERROR, string))