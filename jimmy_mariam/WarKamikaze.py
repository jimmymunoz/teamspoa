class defaultState(object):
	@staticmethod
	def execute():
		setDebugString("I'm a WarKamikaze");
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "EnemyBaseFound"): #Pending to calculate base enemy position
				arrContent = message.getContent()
				#WarKamikaze.enemyBaseAngle = message.getAngle();
				baseDistance = float(message.getDistance());

				debugStr = "AttackEnemyBase BA( " + str(message.getAngle()) + " ) BD: (" + str(message.getDistance()) + ") ";
				setDebugString(debugStr);
				setHeading(message.getAngle())
				return move();

		return move();

def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			sendMessage(message.getSenderID(), "responseIdentify", ("WarKamikaze") );
			
def reflexes():
	#percepts = getPercepts()
	PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
	if PerceptsEnemiesWarBase:
		#broadcastMessageToAll("EnemyBase","")
		#infoBase = ( str(percetEnemyBase.getAngle()), str(percetEnemyBase.getDistance()), str(getHeading()) )
		#broadcastMessageToAll("EnemyBaseFound",  infoBase )
		for percept in PerceptsEnemiesWarBase:
			setHeading(percept.getAngle())
			if (isReloaded()):
				return fire()
				#return move()
			else :
				return reloadWeapon()
	#for percept in percepts:
	if isBlocked():
		RandomHeading()
		
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
WarKamikaze.enemyBaseAngle = 0
