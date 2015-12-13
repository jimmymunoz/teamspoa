class defaultState(object):
	@staticmethod
	def execute():
		return move();

def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			setDebugString("I'm a WarKamikaze");
			sendMessage(message.getSenderID(), "responseIdentify", ("WarKamikaze") );
			
def reflexes():
	percepts = getPercepts()
	#for percept in percepts:
			
	return None

def actionWarKamikaze():
	validateMainMessages()
	result = reflexes() # Reflexes
	if result:
		return result
		
	# FSM - Changement d'Ã©tat
	WarKamikaze.currentState = WarKamikaze.nextState
	WarKamikaze.nextState = None

	if WarKamikaze.currentState:
		return WarKamikaze.currentState.execute()
	else:
		result = defaultState.execute()
		WarKamikaze.nextState = defaultState
		return result;

	return move();

WarKamikaze.nextState = defaultState
WarKamikaze.currentState = None
