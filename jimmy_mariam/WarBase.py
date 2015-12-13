
def actionWarBase():

	messages = getMessages();

	if( True ):
		for message in messages:
			if(message.getMessage() == "whereAreYou"):
				setDebugString("OurBaseIsHere");
				sendMessage(message.getSenderID(), "OurBaseIsHere", "");
			if(message.getMessage() == "whereAreYo"):
				setDebugString("OurBaseIsHere");
				sendMessage(message.getSenderID(), "OurBaseIsHere", "");
			elif( message.getMessage() == "b" ) :
				debugStr = "RocketLaunchersAttack: (" + str(message.getAngle()) + ") Angle ";
				setDebugString(debugStr);
				params = (str(message.getAngle()),  str(message.getDistance()) )
				broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "RocketLaunchersAttack", params );#str to cast string
			else:
				setDebugString("BaseOk");
	#Jimmy: All Enemies	
	if( False ):
		percepts = getPerceptsEnemies();
		for percept in percepts:
			broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemiesInOurBase", "");#str to cast string
			setDebugString("ThereAreEnemiesInOurBase distance:" + str(percept.getDistance()) );
		
	else: #Only Rocket Launchers
		percepts = getPercepts();
		for percept in percepts:
			if (percept.getType().equals(WarAgentType.WarRocketLauncher) and isEnemy(percept) and percept.getDistance() <= 50 ):
				broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemiesLauncher", "");#str to cast string
				setDebugString("ThereAreEnemiesInOurBase distance:" + str(percept.getDistance()) );
	
	return idle();


