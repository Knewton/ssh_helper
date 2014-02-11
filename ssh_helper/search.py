import sys
import k.aws.ec2
import k.aws.config

def match_string(x, y):
	return x.find(y) > -1

def match_instance(instance, groups, k):
	search_fields = ['state', 'public_dns_name', 'private_dns_name', 'ip_address', 'private_ip_address', 'id', 'image_id', 'placement']
	for g in groups:
		if match_string(g, k):
			return True
	for f in search_fields:
		v = eval('instance.' + f)
		if v:
			if match_string(v.lower(), k):
				return True
	for t in instance.tags.keys():
		if match_string(instance.tags[t].lower(), k):
			return True
	return False

def get_group_name(group):
	try:
		return group.name
	except:
		return group.id

def list_instances(ec2conn, env):
	reservations = ec2conn.get_all_instances()
	instances = set()
	for reservation in reservations:
		groups = [get_group_name(group).lower() for group in reservation.groups]
		for instance in reservation.instances:
			tagdict = instance.tags.copy()
			if tagdict.has_key('aws:cloudformation:stack-id'):
				del tagdict['aws:cloudformation:stack-id']
			if tagdict.has_key('aws:autoscaling:groupName'):
				del tagdict['aws:autoscaling:groupName']
			if tagdict.has_key('aws:cloudformation:stack-name'):
				groups.append(tagdict['aws:cloudformation:stack-name'].lower())
				del tagdict['aws:cloudformation:stack-name']
			if tagdict.has_key('aws:cloudformation:logical-id'):
				del tagdict['aws:cloudformation:logical-id']
			tags = ["%s=%s" % (tag.lower(), tagdict[tag].lower()) for tag in tagdict.keys()]
			auth = "RSA-Only"
			if "kerberoskeytabisdeployed=true" in tags:
				auth = "Kerberos"
				tags.remove("kerberoskeytabisdeployed=true")
			instances.add((instance, tuple(groups), tuple(tags), auth, env))
	return instances

def get_list(cache, options):
	if not options.knewton_env:
		sys.stderr.write("No environment passed in\n")
		sys.exit(1)
	if not cache.has_key(options.knewton_env):
		creds = k.aws.config.get_keys(options)
		ec2conn = k.aws.ec2.connect(creds)
		cache[options.knewton_env] = list_instances(ec2conn, options.knewton_env)
	return cache[options.knewton_env]

def find_instances(options, cache, search_string):
	parts = search_string.split(".")
	if len(parts) == 7 and parts[5] == 'knewton' and parts[6] == 'net':
		# Canonical format:
		# i-eebbef96.us-east-1d.cassandra.qa.staging.knewton.net
		options = k.aws.config.ManualOptions(knewton_env=parts[4])
		search_string = parts[0]
	winners = set()
	for instance, groups, tags, auth, env in get_list(cache, options):
		if match_instance(instance, groups, search_string):
			winners.add((instance, groups, tags, auth, env))
	return winners

def search(options, search_strings):
	cache = {}
	instance_set = None
	if len(search_strings) == 0:
		instance_set = set()
		for instance, groups, tags, auth, env in get_list(cache, options):
			instance_set.add((instance, groups, tags, auth, env))
	else:
		for search_string in search_strings:
			if instance_set:
				if search_string.endswith("+"):
					instance_set = instance_set.union(
						find_instances(options, cache, search_string[:-1]))
				elif search_string.startswith("+"):
					instance_set = instance_set.union(
						find_instances(options, cache, search_string[1:]))
				elif search_string.endswith("^"):
					instance_set = instance_set.intersection(
						find_instances(options, cache, search_string[:-1]))
				elif search_string.startswith("^"):
					instance_set = instance_set.intersection(
						find_instances(options, cache, search_string[1:]))
				elif search_string.endswith("-"):
					instance_set = instance_set.difference(
						find_instances(options, cache, search_string[:-1]))
				elif search_string.startswith("-"):
					instance_set = instance_set.difference(
						find_instances(options, cache, search_string[1:]))
				else:
					instance_set = instance_set.intersection(
						find_instances(options, cache, search_string))
			else:
				instance_set = find_instances(options, cache, search_string)
	return instance_set

