import os
import yaml
from ssh_helper.constants import RESET, FG, FG_BOLD

def default_configs():
	configs = {}
	configs.update(default_prompt_configs())
	configs.update(default_ssh_config())
	configs.update(default_cssh_config())
	return configs

def default_prompt_configs():
	return {
		'aws_color': FG['yellow'],
		'aws_prompt': 'FG_BOLD["white"] + "[" + config["aws_color"] + ' +
			'self.aws + FG_BOLD["white"] + "]" + RESET + " "',
		'kcs_color': FG_BOLD['cyan'],
		'kcs_prompt': 'FG_BOLD["white"] + "(" + config["kcs_color"] + ' +
			'self.kcs + "-" + self.stack + FG_BOLD["white"] + ")" + RESET + " "',
		'group_color': FG_BOLD['cyan'],
		'group_prompt': 'FG_BOLD["white"] + "(" + config["group_color"] + ' +
			'self.group + FG_BOLD["white"] + ")" + RESET + " "',
		'prompt': 'self.aws_prompt() + self.kcs_or_group_prompt() + ' +
			'FG_BOLD["green"] + "\u@\h" + FG_BOLD["white"] + ":" + ' +
			'FG_BOLD["yellow"] + "\w" + FG_BOLD["white"] + " $" + RESET  + " "',
		'overrides': {
			'production': {
				'aws_color': FG_BOLD['red'],
			},
			'uat': {
				'aws_color': FG_BOLD['red'],
			},
			'biggie': {
				'kcs_color': FG_BOLD['red'],
			}
		}
	}

def default_ssh_config():
	return {
		'ssh_command': '["ssh", "-o", "StrictHostKeyChecking=no"]'
	}

def default_cssh_config():
	return {
		'cssh_command': '["cssh", "-o", "-o StrictHostKeyChecking=no"]',
		'cssh_per_host_args': '[]',
		'cssh_command_flag': '-a'
	}

def get_overridden_config(user_config, key=None):
	result = {}
	result.update(default_configs())
	overrides = default_configs().get('overrides', {})
	result.update(user_config)
	result.update(overrides.get(key, {}))
	overrides = user_config.get('overrides', {})
	result.update(overrides.get(key, {}))
	return result

SSH_HELPER_PATH = os.path.expanduser('~/.ssh_helper')
def get_user_config():
	filename = os.path.join(SSH_HELPER_PATH, "config.yml")
	if not os.path.exists(filename):
		config = default_configs()
		if not os.path.exists(SSH_HELPER_PATH):
			os.mkdir(SSH_HELPER_PATH, 0700)
		with open(filename, "w") as yaml_file:
			yaml_file.write(yaml.dump(config))
		return config
	else:
		with open(filename) as yaml_file:
			return yaml.load(yaml_file)
