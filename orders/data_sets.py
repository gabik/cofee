strong_choices = ([('1','Light'), ('2','Normal'),('3','Strong'), ])

size_choices = ([('1','Small'), ('2','Normal'),('3','Big'), ])

def map_status(order_status):
	status = {}
	status["Sent"] = "nonready"
	status["Ready"] = "ready"
	status["Branch"] = None
	status["Done"] = None
	status["Cart"] = None
	status["Dropped"] = None
	return status[str(order_status)]
	
