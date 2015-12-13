class buildWarWarTurret(object):
	@staticmethod
	def execute():
		#broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYou","")
		setDebugString("buildingWarWarTurret");
		sendMessage(WarEngineer.baseId, "whereAreYou", "" );
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "OurBaseIsHere" ):
				setDebugString("Distance to Build " + str(message.getDistance()));
				setHeading( message.getAngle() )
				if( message.getDistance() > WarEngineer.infoBuildBase[0] and message.getDistance() < (WarEngineer.infoBuildBase[0] + WarEngineer.infoBuildBase[1]) ):
					#setRandomHeading(45);
					enableToCreate = 0
					if (isAbleToCreate(WarAgentType.WarTurret) ):
						enableToCreate = 1
						resultBuild = buildWarTurret()
						if (resultBuild):
							return resultBuild;
					
					setDebugString("Distance OK " + str(message.getDistance()) + " enableToCreate: " + str(enableToCreate) );
					return idle();
				#followTarget(message)
		return move()


class defaultState(object):
	@staticmethod
	def execute():
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "buildWarWarTurret" ):
				setDebugString("buildWarWarTurret");
				sendMessage(message.getSenderID(), "IDoIt", (str("WarEngineer") ) );
				WarEngineer.baseId = message.getSenderID()
				WarEngineer.nextState = buildWarWarTurret
				WarEngineer.infoBuildBase = message.getContent()
				setHeading( message.getAngle() )
				return move();


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

def buildWarTurret():
	if(len(WarBase.teamInformation['WarTurret']) == 0):
		setNextAgentToCreate(WarAgentType.WarTurret);
		if (isAbleToCreate(WarAgentType.WarTurret) ):
			return create();

	return None;


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
WarEngineer.baseId = 0
WarEngineer.infoBuildBase = []
