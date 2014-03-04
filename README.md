# SSH Helper

##About

ssh_helper is a very flexible ssh tool used to find boxes in the knewton cloud.  Not every box is in a kcs environment, which causes frusterations for people when on prod support and having to deal with legacy or non platform boxes.  ssh_helper exists to fill this gap

## Setup

To use this, you will want to install it on your base system.
./setup.py install
add this like to your .bashrc or .bash_profile:
source /usr/local/bin/ssh_helper_aliases.sh

By default this will enable:
* hss s : ssh to your staging account
* hss p : ssh to your production account

Note: All of these commands use the hss alias from ssh_helper_aliases.sh.  hss s is the equivelent of ssh_helper -e staging.  For more invormation about aws environments with ssh helper, see [k.aws](https://github.com/Knewton/k.aws)

You will want to edit ssh_helper_aliases.sh to have an option for every account you want access to.

## Usage

the program will return a list of servers that meet your search string. the search string you input will search over the group names, tags, ip addresses, dns names, instance ids, images and states for all instances in the environment you are searching in.

(from ssh_helper -h)

> Give the system an environment and a search string. The search strings will match on any of:
>   * instance id
>   * security groups
>   * public/private dns/ip
>   * tags
>   * nagios canonical instance name
>     (No environment needed if using only nagios canonical instance names)
>  
> You can do set logic on results.  By passing in multiple search strings, you can alter the final resturned set.  Each set operation is against the setthat has been created thus far up to that arg.
>   * starting a search string with - will do a difference
>   * starting a search string with ^ will do an intersection
>   * additional args with no set character is an implicit intersection
>  
> If you do not pass in an ssh range, if only one box is found, it will ssh to it.  If multiple are found, it will return a list of boxes.
> If you pass in an ssh range, it will ssh to the box(es) using ssh for one box or cssh for multiple
>   ssh range can look like the following:
>   * 1
>   * 2,4,5
>   * 3-10
>   * 3-10,12-13
>   * all
>  
> ssh helper can also take search strings on stdin in the form of a list, or the json output from knife search.  The servers passed in will be treated as the first set if any additional search strings are added


If your search finds only one box that meets the conditions, it will ssh to that box
> $ hss s i-095b5d66
> running 2013-06-05T03:37    i-095b5d66  ec2-54-226-42-232.compute-1.amazonaws.com   Kerberos    nagios_apiuat_kcs,apiuat_kcs,base,apiuat-nagios-nagiossecuritygroup-9jzszob9vzqy,apiuat-nagios
>  
> <opening ssh session>

You can then ssh to a server by number from the list:
> $ hss s nagios
> 0. running  2013-02-01T20:52    i-bad75fca  ec2-50-17-16-29.compute-1.amazonaws.com Kerberos    nagios,base
> 1. running  2013-06-05T03:37    i-095b5d66  ec2-54-226-42-232.compute-1.amazonaws.com   Kerberos    nagios_apiuat_kcs,apiuat_kcs,base,apiuat-nagios-nagiossecuritygroup-9jzszob9vzqy,apiuat-nagios
> 2. running  2013-06-12T14:11    i-88ec12e6  ec2-54-234-6-241.compute-1.amazonaws.com    Kerberos    qa_kcs,qa-nagios-nagiossecuritygroup-fo4tcuo01cwp,base,nagios_qa_kcs,qa-nagios
> 3. running  2013-06-12T14:50    i-b4e9cade  ec2-107-21-173-225.compute-1.amazonaws.com  Kerberos    wonderwoman-nagios-nagiossecuritygroup-1a0v6oy7jig0z,wonderwoman_kcs,base,nagios_wonderwoman_kcs,wonderwoman-nagios
> $ hss s nagios 1
> running 2013-06-05T03:37    i-095b5d66  ec2-54-226-42-232.compute-1.amazonaws.com   Kerberos    nagios_apiuat_kcs,apiuat_kcs,base,apiuat-nagios-nagiossecuritygroup-9jzszob9vzqy,apiuat-nagios
> 
> <opening ssh session>

If you have cssh installed, or have configured ssh helper to use an alternate multi ssh tool you can ssh to multiple boxes at once:
> $ hss s nagios 1,3
> 0. running  2013-06-05T03:37    i-095b5d66  ec2-54-226-42-232.compute-1.amazonaws.com   Kerberos    nagios_apiuat_kcs,apiuat_kcs,base,apiuat-nagios-nagiossecuritygroup-9jzszob9vzqy,apiuat-nagios
> 1. running  2013-06-12T14:50    i-b4e9cade  ec2-107-21-173-225.compute-1.amazonaws.com  Kerberos    wonderwoman-nagios-nagiossecuritygroup-1a0v6oy7jig0z,wonderwoman_kcs,base,nagios_wonderwoman_kcs,wonderwoman-nagios
> Opening to: ec2-54-226-42-232.compute-1.amazonaws.com ec2-107-21-173-225.compute-1.amazonaws.com
>  
> <Opening a cluster ssh session>


ssh helper has some powerful search features.  You can search for a box by substring from any of the following:

* ec2 instance id (example: i-1bf0bd74)
* ec2 internal dns name (example: ip-10-98-41-207.ec2.internal)
* ec2 external dns name (example: ec2-54-211-37-220.compute-1.amazonaws.com)
* ec2 internal ip address (example: 10.98.41.207)
* ec2 external ip address (example: 54.211.37.220)
* security group names
* tags

The search can use set logic to narrow or increase the server list.  The ssh helper set functions include union (prepend +), intersection (prepend nothing) and difference (prepend -).

*intersection example*

> $ hss s nagios
> 0. running  2013-02-01T20:52    i-bad75fca  ec2-50-17-16-29.compute-1.amazonaws.com Kerberos    nagios,base
> 1. running  2013-06-05T03:37    i-095b5d66  ec2-54-226-42-232.compute-1.amazonaws.com   Kerberos    nagios_apiuat_kcs,apiuat_kcs,base,apiuat-nagios-nagiossecuritygroup-9jzszob9vzqy,apiuat-nagios
> 2. running  2013-06-12T14:11    i-88ec12e6  ec2-54-234-6-241.compute-1.amazonaws.com    Kerberos    qa_kcs,qa-nagios-nagiossecuritygroup-fo4tcuo01cwp,base,nagios_qa_kcs,qa-nagios
> 3. running  2013-06-12T14:50    i-b4e9cade  ec2-107-21-173-225.compute-1.amazonaws.com  Kerberos    wonderwoman-nagios-nagiossecuritygroup-1a0v6oy7jig0z,wonderwoman_kcs,base,nagios_wonderwoman_kcs,wonderwoman-nagios
>  
> $ hss s nagios api
> running 2013-06-05T03:37    i-095b5d66  ec2-54-226-42-232.compute-1.amazonaws.com   Kerberos    nagios_apiuat_kcs,apiuat_kcs,base,apiuat-nagios-nagiossecuritygroup-9jzszob9vzqy,apiuat-nagios
> <opening ssh session>

*union example*
> $ ussh techbot
> running 2013-04-27T20:03    i-307d165e  ec2-54-224-231-194.compute-1.amazonaws.com  Kerberos    base,techbot
>  
> $ ussh aka
> running 2013-04-01T19:50    i-8ed340e2  ec2-23-22-39-28.compute-1.amazonaws.com Kerberos    aka,base
>  
> $ ussh techbot +aka
> 0. running  2013-04-01T19:50    i-8ed340e2  ec2-23-22-39-28.compute-1.amazonaws.com Kerberos    aka,base
> 1. running  2013-04-27T20:03    i-307d165e  ec2-54-224-231-194.compute-1.amazonaws.com  Kerberos    base,techbot

*difference example*
> $ ussh graphite staging
> 0. running  2013-07-02T19:38    i-1a0d1d74  ec2-54-226-212-38.compute-1.amazonaws.com   Kerberos    base,graphite,graphite-relay,facet=relay,cluster=staging
> 1. running  2013-06-17T21:40    i-fa1cac94  ec2-50-16-2-85.compute-1.amazonaws.com  Kerberos    base,graphite,facet=cache,cluster=staging
> 2. running  2013-07-02T19:37    i-8e3805e2  ec2-54-234-200-129.compute-1.amazonaws.com  Kerberos    base,graphite,graphite-relay,facet=relay,cluster=staging
> 3. running  2013-06-17T21:36    i-e188878a  ec2-54-235-34-178.compute-1.amazonaws.com   Kerberos    base,graphite,facet=cache,cluster=staging
>  
> $ ussh graphite staging -cache
> 0. running  2013-07-02T19:38    i-1a0d1d74  ec2-54-226-212-38.compute-1.amazonaws.com   Kerberos    base,graphite,graphite-relay,facet=relay,cluster=staging
> 1. running  2013-07-02T19:37    i-8e3805e2  ec2-54-234-200-129.compute-1.amazonaws.com  Kerberos    base,graphite,graphite-relay,facet=relay,cluster=staging








