import cProfile,io,pstats

def profile(func):
	def inner(*args,**kwargs):
		pr = cProfile.Profile()
		pr.enable()
		retriev = func(*args,**kwargs)
		pr.disable()
		s = io.StringIO()
		sortby = 'cumulative'
		ps = pstats.Stats(pr,stream = s).sort_stats(sortby)
		ps.print_stats()
		print(s.getvalue())
		return retriev
	    
	return inner




    
