#!/usr/bin/python

# This connects to a test ftp server and downloads a sample file.
print "hello. testing python module 'pexpect'..."

import pexpect

#child = pexpect.spawn('ftp ftp.openbsd.org')
child = pexpect.spawn('ssh admin@10.250.0.100')

#child.expect('admin@10.250.0.10\'s password:')
child.expect('password: ')
print child.before, child.after

child.sendline('testtest')

#child.expect('(Aruba7005) ^[mynode] #')
#child.expect('\(Aruba 7005*')
#child.expect('[mynode] #')
child.expect('#')
print child.before, child.after

#==========
# get firmware version

child.sendline('show version')
child.expect('#')
print child.before, child.after

#==========

child.sendline('show wlan ssid-profile')
child.expect('#')
print child.before, child.after

#==========

child.sendline('show wlan ssid-profile Aruba_7005-ssid_prof')
#child.expect('#')
child.expect('--More--')
print child.before, child.after

child.sendline('q')

#==========

print "enter the config mode..."
child.sendline('configure terminal')
child.expect('#')
print child.before, child.after

child.sendline('wlan ssid-profile kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('essid kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('wpa-passphrase testtest')
child.expect('#')
print child.before, child.after

child.sendline('opmode wpa2-psk-aes')
child.expect('#')
print child.before, child.after

child.sendline('ssid-enable')
child.expect('#')
print child.before, child.after

child.sendline('write memory')
child.expect('#')
print child.before, child.after

#==========
# create authentication-dot1x kloftin-test

child.sendline('aaa authentication dot1x kloftin-test')
child.expect('#')
print child.before, child.after

# no options needed.
child.sendline('write memory')
child.expect('#')
print child.before, child.after

#==========
# create aaa-profile kloftin-test

child.sendline('aaa profile kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('authentication-dot1x kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('write memory')
child.expect('#')
print child.before, child.after

#==========
# create virtual-ap kloftin-test

child.sendline('wlan virtual-ap kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('vlan 1')
child.expect('#')
print child.before, child.after

child.sendline('ssid-profile kloftin-test')
#child.sendline('no ssid-profile kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('aaa-profile kloftin-test')
#child.sendline('no aaa-profile Aruba_7005-aaa_prof')
child.expect('#')
print child.before, child.after

child.sendline('write memory')
child.expect('#')
print child.before, child.after

#==========

child.sendline('ap-group default')
child.expect('#')
print child.before, child.after

child.sendline('virtual-ap kloftin-test')
#child.sendline('no virtual-ap kloftin-test')
child.expect('#')
print child.before, child.after

child.sendline('write memory')
child.expect('#')
print child.before, child.after

#==========
# no wlan ssid-profile kloftin-test
# no wlan virtual-ap kloftin-test
#==========

print "exit the config mode..."
child.sendline('exit')
child.expect('#')
print child.before, child.after

print "send final 'exit'"
child.sendline('exit')
#child.expect('#')
#print child.before, child.after

exit(0)
