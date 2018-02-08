#!/usr/local/bin/python3

### IMPORTS ###
import argparse
import os
import sys


### CLASSES ###
class Vhost:
	def __init__(self):
		self.file = '/etc/hosts'
		# self.file = 'vhost.local'
		self.lines = ''
		self.errors = 0
		self.short_target = "# +::1\n"
		self.full_target = "# +127.0.0.1\n"

	def load_lines(self):
		handle = open(self.file, 'r')
		self.lines = handle.readlines()
		handle.close()

	def add_vhost(self, vhost, type):
		prefixe = False
		target = ""

		# choose prefixe
		if type == 1:
			prefixe = '::1 '
			target = self.short_target
		elif type == 2:
			prefixe = '127.0.0.1 '
			target = self.full_target

		if prefixe != False:
			try:
				index = self.lines.index(target)
				self.lines.insert(index, prefixe + vhost + '\n')
			except Exception:
				self.errors += 1
				print('no such target')

	def add_all_types(self, vhost):
		types = [1, 2]
		for t in types:
			self.add_vhost(vhost, t)

	def del_vhost(self, vhost, type):
		prefixe = False

		if type == 1:
			prefixe = '::1 '
		elif type == 2:
			prefixe = '127.0.0.1 '

		if prefixe != False:
			target = prefixe + vhost + '\n'
			try:
				index = self.lines.index(target)
				del self.lines[index]
				return 0 # ok
			except Exception:
				self.errors += 1
				return 1 # error

	def del_all_types(self, vhost):
		types = {1:'::1', 2:'127.0.0.1'}
		res = {}
		
		for t in types:
			res[t] = self.del_vhost(vhost, t)

		nb_errors = 0
		nb_ok = 0
		for r in res:
			if res[r] == 1:
				nb_errors += 1
				print('> Could not delete vhost of type %s' % types[r])
			else:
				nb_ok += 1
				print('> Removed vhost of type %s' % types[r])

		if nb_ok>0:
			self.errors -= nb_errors


	def list(self):
		short_search = "::1 " # space is important
		full_search = "127.0.0.1 " # space is important
		vhosts_list = {} # dict {vhost:vhost_type}

		# parse file
		for line in self.lines:
			# pass if line contains a comment
			if '#' in line:
				continue

			# pass if ::1 or 127.0.0.1 is not in line
			strip = ''
			if short_search in line:
				strip = short_search
			elif full_search in line:
				strip = full_search
			else:
				continue

			# clean line
			vhost_to_add = line.rstrip().lstrip(strip)
			vhost_type = strip.rstrip()

			# add it to the vhosts list
			if vhost_to_add not in vhosts_list:
				vhosts_list[vhost_to_add] = vhost_type
			elif vhosts_list[vhost_to_add] != vhost_type:
				vhosts_list[vhost_to_add] += ', ' + vhost_type

		print( '{:<30s} {:<20s}'.format('## Vhost ##', '## Type ##') )
		[print( '{:<30s} {:<20s}'.format(vhost, vhosts_list[vhost]) ) for vhost in vhosts_list]	

	def print_lines(self):
		print(self.lines)

	def write_lines(self):
		handle = open(self.file, 'w')
		handle.writelines(self.lines)
		handle.close()
		
		if self.errors == 0:
			print(self.file + ' updated !')
		else:
			print("Could not update %s, %d errors !" % (self.file, self.errors))




### FUNCTIONS ###
def main():
	# init parser
	parser = argparse.ArgumentParser(description='Manage Vhosts')
	parser.add_argument('command', metavar='command', type=str, nargs=1,
	                    help='(add | remove | list)')
	parser.add_argument('vhost', metavar='vhost', type=str, nargs='?',
	                    help='The vhost to manage')
	parser.add_argument('type', metavar='vhost_type', type=int, nargs='?',
	                    help='The vhost type (1->::1 | 2->127.0.0.1)')
	args = parser.parse_args()
	

	# ask for root access
	euid = os.geteuid()
	if euid != 0:
	    print("Script not started as root. Running sudo..")
	    args = ['sudo', sys.executable] + sys.argv + [os.environ]
	    # the next line replaces the currently-running process with the sudo
	    os.execlpe('sudo', *args)


	# init vhost manager
	vhostManager = Vhost()
	vhostManager.load_lines()
	
	if args.command[0] == 'add' or args.command[0] == 'remove':
		if args.vhost is not None:
			if args.command[0] == 'add':
				if args.type is not None:
					print('\n######################\nadding %s as type %d ...\n######################' % (args.vhost, args.type))
					vhostManager.add_vhost(args.vhost, args.type)
				else:
					print('\n######################\nadding %s ...\n######################' % args.vhost)
					vhostManager.add_all_types(args.vhost)

			else:
				if args.type is not None:
					print('\n######################\nremoving %s ...\n######################' % args.vhost)
					vhostManager.del_vhost(args.vhost, args.type)
				else:
					print('\n######################\nremoving all %s occurrences...\n######################' % args.vhost)
					vhostManager.del_all_types(args.vhost)
				
			# save file
			vhostManager.write_lines()
		else:
			print('Please do specify a vhost with the command [%s]' % args.command[0])
	elif args.command[0] == 'list':
		print('\n######################\nListing your vhosts...\n######################')
		vhostManager.list()

#### MAIN ####
if __name__ == '__main__':
	main()
