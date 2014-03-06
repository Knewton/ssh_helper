from ssh_helper.config import get_overridden_config
from ssh_helper.constants import RESET, FG, FG_BOLD

class Prompt(object):
	def __init__(self, user_config, instance):
		self.user_config = user_config
		self.instance = instance[0]
		self.groups = instance[1]
		self.tags = instance[2]
		self.aws = instance[4]
		self.stack = None
		self.group = None
		self.get_group()

	def get_group(self):
		testgroups = []
		testgroups.extend(self.groups)
		if 'base' in testgroups:
			testgroups.remove('base')
		if 'application' in testgroups:
			testgroups.remove('application')
		if 'webservice' in testgroups:
			testgroups.remove('webservice')
		if 'utility' in testgroups:
			testgroups.remove('utility')
		if 'autodeploy' in testgroups:
			testgroups.remove('autodeploy')
		for group in testgroups:
			if group.startswith('application-') or group.startswith('webservice-'):
				self.group = group
				return
		if len(testgroups) > 0:
			self.group = testgroups[0]
		else:
			self.group = self.groups[0]

	def prompt(self):
		config = get_overridden_config(self.user_config)
		code = config.get('prompt', '')
		if code:
			try:
				pstr = eval(code)
				if pstr.strip() != '':
					return ['-t', "export PS1='%s' && bash --norc -i" % pstr]
			except TypeError:
				pass
		return []

	def aws_prompt(self):
		retstr = ""
		if self.aws:
			config = get_overridden_config(self.user_config, self.aws)
			code = config.get('aws_prompt', '')
			if code:
				try:
					return eval(code)
				except TypeError:
					pass
		return retstr

	def group_prompt(self):
		retstr = ""
		if self.group:
			config = get_overridden_config(self.user_config, self.group)
			code = config.get('group_prompt', '')
			if code:
				try:
					return eval(code)
				except TypeError:
					pass
		return retstr
