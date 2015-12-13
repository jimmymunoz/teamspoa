class defaultState(object):
	@staticmethod
	def execute():
		WarBase.nextState = defaultState;
		messages = getMessages();

		if( True ):
			for message in messages:
				if(message.getMessage() == "whereAreYou"):
					setDebugString("OurBaseIsHere");
					sendMessage(message.getSenderID(), "OurBaseIsHere", "");
				elif( message.getMessage() == "EnemyBase" ) :
					arrContent = message.getContent()
					#indexoutofrange
					ExplorerbaseEnemyAngle = float(arrContent[0]);
					ExplorerbaseEnemyDistance = float(arrContent[1]);
					explorerAngle = float(arrContent[0]);
					explorerDistance = float(arrContent[1]);
					explorerHeading = float(arrContent[1]);

					baseEnemyAngle = explorerAngle + ExplorerbaseEnemyAngle;
					if (baseEnemyAngle > 360):
						baseEnemyAngle = baseEnemyAngle - 360
						
					baseEnemyDistance = 1;

					WarBase.baseState = "ExBasEAngle: " + arrContent[0] + " \nExD: " + arrContent[1] + " \nExpH: " + arrContent[2] + " BaseEA: " + str(baseEnemyAngle) + " baseED:" + str(baseEnemyDistance) + " ExpAn: " +  str(message.getAngle()) + " ExpD" + str(message.getDistance());
					#debugStr = "RocketLaunchersAttack: (" + str(message.getAngle()) + ") Angle ";
					#setDebugString(debugStr);
					infoBase = ( str(message.getAngle()), str(message.getDistance()), arrContent[0], arrContent[1], arrContent[2] )  
					broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "RocketLaunchersAttack", infoBase);#str to cast string
		
		setDebugString(WarBase.baseState);
		broadcastMessageToAll("baseState", WarBase.baseState);
		return idle();

	
def reflexes():
	percepts = getPercepts()
	for percept in percepts:
		#Jimmy: Only Rocket Launchers
		if (percept.getType().equals(WarAgentType.WarRocketLauncher) and isEnemy(percept) and percept.getDistance() <= 30 ):
			#Disable
			if(False): 
				broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemiesInOurBase", "");#str to cast string
				WarBase.baseState = "BaseAtRisk"
			#setDebugString("ThereAreEnemiesInOurBase distance:" + str(percept.getDistance()) );
			
	return None

def actionWarBase():
	WarBase.baseState = "BaseOk" #Default State
	result = reflexes() # Reflexes
	if result:
		return result

		
	# FSM - Changement d'Ã©tat
	WarBase.currentState = WarBase.nextState
	WarBase.nextState = None

	if WarBase.currentState:
		return WarBase.currentState.execute()
	else:
		result = searchEnemyBase.execute()
		WarBase.nextState = searchEnemyBase
		return result;
	

WarBase.nextState = defaultState
WarBase.baseState = "sateOk"
WarBase.currentState = None
WarBase.baseEnemy = (); #Array with the enemy bases location.
