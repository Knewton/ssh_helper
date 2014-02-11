To use this, you will want to install it on your base system.
./setup.py install
add this like to your .bashrc or .bash_profile:
source /usr/local/bin/ssh_helper_aliases.sh

If you instead install this into a virtualenv, you'll need to source it from the virtualenv bin and somehow add ssh_helper to your path (via symlink or adding the bin folder to your path)

you can then use the following commands:
ussh : ssh to the utility cloud
sssh : ssh to the staging cloud
pssh : ssh to the production cloud

the program will return a list of servers that meet your search string.  the search string you input will search over the group names, tags, ip addresses, dns names, images and states for all instances in the environment you are searching in.

You can then ssh to a server by number from the list:

$ sssh kestrel
0. running	2012-05-03T19:05:21.000Z	ec2-23-20-83-237.compute-1.amazonaws.com	Groups:[dev_kcs]	Tags:[dev-kestrel,dev-kestrel-kestrelgroup-vs54ef9m0qo3,kestrelgroup]
1. running	2012-04-25T16:19:55.000Z	ec2-184-73-120-252.compute-1.amazonaws.com	Groups:[kestrel_dev_kcs,dev_kcs]	Tags:[kestrel,kestrel-kestrelgroup-15ypee65aqnvz,kestrelgroup]
2. running	2012-04-11T18:51:37.000Z	ec2-23-20-109-151.compute-1.amazonaws.com	Groups:[superstaging-kestrel,base,superstaging]	Tags:[kestrel,superstaging,superstaging-kestrel-0,0]
3. running	2012-03-21T22:11:18.000Z	ec2-50-19-21-193.compute-1.amazonaws.com	Groups:[kpip,haagkpip-kestrel,base,haagkpip]	Tags:[kestrel,haagkpip,haagkpip-kestrel-0,0]

$ sssh kestrel 0
running	2012-05-03T19:05:21.000Z	ec2-23-20-83-237.compute-1.amazonaws.com	Groups:[dev_kcs]	Tags:[dev-kestrel,dev-kestrel-kestrelgroup-vs54ef9m0qo3,kestrelgroup]


If you have clusterssh installed, you can also ssh to multiple boxes at once:

$ sssh kestrel 0,2
0. running	2012-05-03T19:05:21.000Z	ec2-23-20-83-237.compute-1.amazonaws.com	Groups:[dev_kcs]	Tags:[dev-kestrel,dev-kestrel-kestrelgroup-vs54ef9m0qo3,kestrelgroup]
1. running	2012-04-11T18:51:37.000Z	ec2-23-20-109-151.compute-1.amazonaws.com	Groups:[superstaging-kestrel,base,superstaging]	Tags:[kestrel,superstaging,superstaging-kestrel-0,0]

