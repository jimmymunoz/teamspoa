class defaultState(object):
	@staticmethod
	def execute():
		return move();

def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			setDebugString("I'm a WarEngineer");
			sendMessage(message.getSenderID(), "responseIdentify", ("WarEngineer") );
			
def reflexes():
	percepts = getPercepts()
	#for percept in percepts:
	if isBlocked():
		RandomHeading()
		return None	
	return None



def actionWarEngineer():
	validateMainMessages()
	result = reflexes() # Reflexes
	if result:
		return result
		
	# FSM - Changement d'Ã©tat
	WarEngineer.currentState = WarEngineer.nextState
	WarEngineer.nextState = None

	if WarEngineer.currentState:
		return WarEngineer.currentState.execute()
	else:
		result = defaultState.execute()
		WarEngineer.nextState = defaultState
		return result;

	return move();

WarEngineer.nextState = defaultState
WarEngineer.currentState = None