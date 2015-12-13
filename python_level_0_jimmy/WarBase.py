
def actionWarBase():

	messages = getMessages();

	if( False ):
		for message in messages:
			if(message.getMessage() == "whereAreYou"):
				setDebugString("OurBaseIsHere");
				sendMessage(message.getSenderID(), "OurBaseIsHere", "");
			elif( message.getMessage() == "EnemyBaseHere" ) :
				debugStr = "RocketLaunchersAttack: (" + str(message.getAngle()) + ") Angle ";
				setDebugString(debugStr);
				broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "RocketLaunchersAttack", str(message.getAngle()) );#str to cast string
		
	percepts = getPercepts();
	for percept in percepts:
		if (percept.getType().equals(WarAgentType.WarRocketLauncher) and isEnemy(percept) and percept.getDistance() <= 30 ):
			setDebugString("ThereAreEnemies distance:" + str(percept.getDistance()) );
			broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemies", "");#str to cast string
	
	return idle();
