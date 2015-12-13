ROTATION_DEGREE = 5

class defaultState(object):
	@staticmethod
	def execute():
		newAngle = getHeading() + ROTATION_DEGREE;
		if( newAngle > 360 ):
			newAngle = newAngle - 360;
		setHeading(newAngle)
		return idle();

def validateMainMessages():
	messages = getMessages()
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			setDebugString("I'm a WarTurret");
			sendMessage(message.getSenderID(), "responseIdentify", ("WarTurret") );
			
		elif(message.getMessage() == "yourGroupIs"):
			setHeading(message.getAngle())
			content = message.getContent()
			WarTurret.GroupName = content[0]; #Jimmy: setGroupName
			if( WarTurret.GroupName == "Defense" ):
				requestRole ("defenceurs", "defend")
			

	return None

			
def reflexes():
	percepts = getPercepts()
	for percept in getPerceptsEnemies():
		setHeading(percept.getAngle())
		if (isReloaded()):
			return fire()
			#return move()
		else :
			return reloadWeapon()
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

