class defaultState(object):
	@staticmethod
	def execute():
		return idle();

def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			setDebugString("I'm a WarTurret");
			sendMessage(message.getSenderID(), "responseIdentify", ("WarTurret") );
			
def reflexes():
	percepts = getPercepts()
	#for percept in percepts:
			
	return None

def actionWarTurret():
	validateMainMessages()
	result = reflexes() # Reflexes
	if result:
		return result
		
	# FSM - Changement d'Ã©tat
	WarTurret.currentState = WarTurret.nextState
	WarTurret.nextState = None

	if WarTurret.currentState:
		return WarTurret.currentState.execute()
	else:
		result = defaultState.execute()
		WarTurret.nextState = defaultState
		return result;

	return move();

WarTurret.nextState = defaultState
WarTurret.currentState = None

