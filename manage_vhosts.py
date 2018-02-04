#!/usr/local/bin/python3

### IMPORTS ###
import argparse
import os
import sys


### CLASSES ###
class Vhost:
	def __init__(self):
		self.file = '/etc/hosts'
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
			except Exception:
				self.errors += 1
				print('vhost does not exists')

	def del_all_types(self, vhost):
		types = [1, 2]
		for t in types:
			self.del_vhost(vhost, t)

	def list(self):
		start_limit = "### START VHOSTS ###\n"
		end_limit = "### END VHOSTS ###\n"
		start_limit_pos = self.lines.index(start_limit)
		end_limit_pos = self.lines.index(end_limit)
		short_search = "::1 " # space is important
		full_search = "127.0.0.1 " # space is important
		vhosts_list = {} # dict {vhost:vhost_type}

		if end_limit_pos > start_limit_pos:
			for line in self.lines[start_limit_pos+1:end_limit_pos]:
				add = False
				strip = ''

				if short_search in line and '#' not in line:
					add = True
					strip = short_search
					
				elif full_search in line and '#' not in line:
					add = True
					strip = full_search


				if add is True:
					vhost_to_add = line.rstrip().lstrip(strip)
					vhost_type = strip.rstrip()

					if vhost_to_add not in vhosts_list:
						vhosts_list[vhost_to_add] = vhost_type
					elif vhosts_list[vhost_to_add] != vhost_type:
						vhosts_list[vhost_to_add] += ', ' + vhost_type
		
		print('######################\nListing your vhosts...\n######################')
		[print("Vhost : %s \t Type : %s" % (vhost, vhosts_list[vhost])) for vhost in vhosts_list]

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
					print('adding %s as type %d ...' % (args.vhost, args.type))
					vhostManager.add_vhost(args.vhost, args.type)
				else:
					print('adding %s ...' % args.vhost)
					vhostManager.add_all_types(args.vhost)

			else:
				if args.type is not None:
					print('removing %s ...' % args.vhost)
					vhostManager.del_vhost(args.vhost, args.type)
				else:
					print('removing all %s ...' % args.vhost)
					vhostManager.del_all_types(args.vhost)
				
			# save file
			vhostManager.write_lines()
		else:
			print('Please do specify a vhost with the command [%s]' % args.command[0])
	elif args.command[0] == 'list':
		vhostManager.list()

#### MAIN ####
if __name__ == '__main__':
	main()
