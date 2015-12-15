class defaultState(object):
	@staticmethod
	def execute():
		setDebugString("I'm a WarKamikaze");
		messages = getMessages();
		for message in messages:
			#if( WarKamikaze.GroupName == "Attack" ):
			if(message.getMessage() == "EnemyBaseFound"): #Pending to calculate base enemy position
				arrContent = message.getContent()
				#WarKamikaze.enemyBaseAngle = message.getAngle();
				baseDistance = float(message.getDistance());

				debugStr = "Explote EnemyBase ";
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
	percepts = getPerceptsEnemies()
	enemyFound = None
	for percept in percepts:
		if( percept.getType() == WarAgentType.WarBase ):
			enemyFound = percept
			break
		if( WarKamikaze.GroupName == "Defense" ):#Only Defense
			if( percept.getType() == WarAgentType.WarRocketLauncher ):
				enemyFound = percept
				break
			elif( percept.getType() == WarAgentType.WarExplorer ):
				enemyFound = percept
				break
			elif( percept.getType() == WarAgentType.WarKamikaze ):
				enemyFound = percept
				break
			elif( percept.getType() == WarAgentType.WarEngineer and False ):#Disabled
				enemyFound = percept
				break
			elif( percept.getType() == WarAgentType.WarTurret and False ):#Disabled
				enemyFound = percept
				break

	if (enemyFound):
		setHeading(enemyFound.getAngle())
		if (isReloaded()):
			return fire()
		else :
			return reloadWeapon()
	#for percept in percepts:
	if isBlocked():
		#RandomHeading()
		setRandomHeading(30)
		
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
WarKamikaze.GroupName = "Attack"
