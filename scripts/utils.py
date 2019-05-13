def parseArgs(argList, flagList):
	flags = flagList.split(',')
	argc = len(argList)
	argv = []
	args = dict()
	i = 0
	while (i < argc):
		arg = argList[i]
		if (arg[1:] in flags):
			args[arg[1:]] = ""
			i += 1
		if ('-' in arg and i+1 < argc):
			args[arg[1:]] = argList[i+1]
			i += 2
		else:
			argv.append(arg)
			i += 1
	return (argc, argv, args)

def file_concat(prepend_str, fname):
	f_li = fname.split('\\')
	f_li[-1] = prepend_str + "_" + f_li[-1]
	return "\\".join(f_li)