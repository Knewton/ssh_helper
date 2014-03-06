import subprocess
import shlex
from ssh_helper.prompt import Prompt
from ssh_helper.config import get_overridden_config

def print_instances(instances):
	n = 0
	for instance in instances:
		print "%s. %s" % (n, print_instance(instance))
		n += 1

def print_instance(winner):
	print_fields = ['state', 'launch_time', 'id', 'public_dns_name', 'instance_type']
	instance, groups, tags, auth, env = winner
	fields = [eval('instance.' + field) for field in print_fields]
	fields[1] = fields[1][:16] # Cutting down the datetime field for screen space
	fields.append(auth)
	elements = ','.join(groups)
	if len(tags) > 0:
		elements = elements + "," + ','.join(tags)
	fields.append(elements)
	return "\t".join(fields)

def open_ssh_connection(options, user_config, instance):
	print print_instance(instance)
	config = get_overridden_config(user_config, instance[4])
	args = ['ssh', '-o', 'StrictHostKeyChecking=no']
	code = config.get('ssh_command', '')
	if code:
		try:
			args = eval(code)
		except TypeError:
			pass
	args.append(instance[0].public_dns_name)
	if options.ssh_args:
		args.extend(shlex.split(options.ssh_args))
	if options.ssh_command is not None:
		args.append(options.ssh_command)
	else:
		args.extend(Prompt(user_config, instance).prompt())
	subprocess.call(args)

def open_cssh_connection(options, user_config, instances):
	print_instances(instances)
	config = get_overridden_config(user_config, instances[0][4])
	args = ['cssh', '-o', '-o StrictHostKeyChecking=no']
	code = config.get('cssh_command', '')
	if code:
		try:
			args = eval(code)
		except TypeError:
			pass
	per_host_args = []
	code = config.get('cssh_per_host_args', '[]')
	if code:
		try:
			per_host_args = eval(code)
		except TypeError:
			pass
	for instance in instances:
		hargs = []
		hargs.extend(per_host_args)
		hargs.append(instance[0].public_dns_name)
		args.extend(hargs)
	if options.ssh_command is not None:
		flag = config.get('cssh_command_flag', '-a')
		if flag:
			args.append(flag)
		args.append(options.ssh_command)
	subprocess.call(args)

def cmp_instance(i1, i2):
	return cmp(i2[0],i1[0])

def construct_range(ssh_range, rlen):
	if not ssh_range:
		if rlen == 1:
			return set([0])
		return set([])
	if ssh_range.lower() == 'all':
		return set(range(0, rlen))
	range_set = set([])
	for chunk in ssh_range.split(","):
		if chunk.find('-') > -1:
			rlist = chunk.split('-')
			bottom = int(rlist[0])
			top = int(rlist[-1]) + 1
			range_set.update(range(bottom, top))
		else:
			range_set.add(int(chunk))
	return range_set

def report_and_connect(options, user_config, winners, ssh_range, search):
	winners = list(winners)
	range_set = construct_range(ssh_range, len(winners))
	winners.sort(cmp_instance)

	ssh_winners = []
	for i in range(0, len(winners)):
		if i in range_set:
			ssh_winners.append(winners[i])

	if len(ssh_winners) == 1 and not search:
		open_ssh_connection(options, user_config, ssh_winners[0])
	elif len(ssh_winners) > 1 and not search:
		open_cssh_connection(options, user_config, ssh_winners)
	else:
		print_instances(winners)

