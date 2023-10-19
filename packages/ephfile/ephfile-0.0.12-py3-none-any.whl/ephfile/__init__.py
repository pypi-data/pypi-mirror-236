import os,sys,shutil

class ephfile(object):
	def __init__(self,foil=None,contents=None,create=True, contents_lambda=None, delete=True,suffix=None):
		self.delete=delete
		to_str = lambda x:str(x) + "\n"
		if foil is None or suffix is not None:
			import tempfile
			self.named = tempfile.NamedTemporaryFile(suffix=suffix)
			self.foil = self.named.name
		else:
			self.named = None
			if not os.path.exists(foil) and create:
				try:
					import pathlib
					pathlib.Path(foil).touch()
				except Exception as  e:
					pass
			self.foil = foil
		self.contents_lambda = contents_lambda or to_str

		if isinstance(contents,list):
			contents = "\n".join(contents)

		if isinstance(contents,str):
			contents = contents.split('\n')
			for cont in contents:
				contz = self.contents_lambda(cont)
				if False and self.named:
					self.named.write(str.encode(contz + "\n"))
				else:
					with open(self.foil,"a+") as writer:
						writer.write(contz)

	@property
	def contents(self):
		with open(self.foil,'r') as reader:
			return ''.join(reader.readlines())

	def __iadd__(self,contents):
		if not isinstance(contents,list):
			contents = [contents]
		elif isinstance(contents,str):
			contents = contents.split('\n')

		contz = '\n'.join([self.contents_lambda(x) for x in contents])
		if self.named:
			self.named.write(str.encode(contz + "\n"))
		else:
			with open(self.foil,"a+") as writer:
				writer.write(contz)

		return self
	
	def __call__(self):
		return self.foil

	def __enter__(self):
		return self

	def close(self):
		try:
			if self.named:
				self.named.close()
			else:
				if self.delete:
					try:
						os.remove(self.foil)
					except:
						try:
							os.system("yes|rm -r " + str(self.foil))
						except Exception as e:
							pass
		except Exception as e:
			print(e)
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()
		return self

class ephdir(object):
	def __init__(self,dirpath=None):
		if not os.path.exists(dirpath):
			os.system("mkdir -p {0}".format(dirpath))
		self.dir = dirpath
		self.files = []
	
	def addephfileto(self, ephfile, newpathwithin):
		if newpathwithin != '':
			print(self.dir)
			newpath = self()+"/"+newpathwithin
			print(newpath)
			os.system("mkdir -p {0}".format(newpath))
		else:
			newpath = self()
		shutil.copyfile(ephfile,str(newpath)+"/"+str(ephfile))

	def __iadd__(self,contentobj):
		if isinstance(contentobj,ephdir):
			newpath = self()+"/"+currentobj()
			os.system("mkdir -p {0}".format(newpath))
			for foil in currentobj.files:
				self.addephfileto(ephfile(),newpath)
		elif isinstance(contentobj,ephfile):
			self.addephfileto(contentobj(),"")
		print(":>>>")
		return self
	
	def __call__(self):
		return self.dir

	def __enter__(self):
		return self

	def close(self):
		try:
			print("yes|rm -r " + str(self.dir))
			os.system("yes|rm -r " + str(self.dir))
		except Exception as e:
			pass
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()
		return self
