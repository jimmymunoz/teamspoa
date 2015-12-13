class SearchFoodState(object):
	@staticmethod
	def execute():
		setDebugString("SearchFoodState")
		
		if isBagFull():
			actionWarExplorer.nextState = GoHomeState
			return idle()

		actionWarExplorer.nextState = SearchFoodState
		percepts = getPerceptsFood()
		if percepts:
            #broadcastMessageToAgentType(WarAgentType.WarExplorer,"FoodHere","")
			if percepts[0].getDistance() < getMaxDistanceTakeFood():
				return take()
			else:
				followTarget(percepts[0])
				return move()
		else:
			for message in getMessages():
				if message.getMessage() == "FoodHere":
					followTarget(message)
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "Base ennemie" and message.getDistance < 200): 
				setDebugString("Base ennemie"+str(message.getAngle()+180))
				setHeading(360);
		return move()

class GoHomeState(object):
	@staticmethod
	def execute():
		setDebugString("GoHomeState")
		if getNbElementsInBag() == 0:
            # Transition vers l'Ã©tat SearchFood
			actionWarExplorer.nextState = WiggleState
			return idle()
        # Maintien de l'Ã©tat
		actionWarExplorer.nextState = GoHomeState
		percepts = getPerceptsAlliesWarBase()
        # Cherche une base dans son champs de vision
		if percepts:
			if percepts[0].getDistance() < maxDistanceGive():
				giveToTarget(percepts[0])
				return give()
			else:
				followTarget(percepts[0])
				return move()
        # Cherche une base par les messages
		broadcastMessageToAgentType(WarAgentType.WarBase,"whereAreYouBase","")
		for mess in getMessages():
			if isMessageOfWarBase(mess):
				followTarget(mess)
			elif(mess.getMessage() == "Base ennemie" and mess.getDistance < 200): 
				setDebugString("Base ennemie"+str(mess.getAngle()+180))
				setHeading(360)
			return move()
		return move()
		

class WiggleState(object):
	@staticmethod
	def execute():
		setDebugString("WiggleState")
		percept1 = getPerceptsFood();
		percept2 = getPerceptsEnemiesByType(WarAgentType.WarBase);
		if percept1:
			actionWarExplorer.nextState = SearchFoodState
		#elif percept2:
		#	setDebugString("Base ennemie")
		#	angle = percept2.getAngle()
		#	broadcastMessageToAgentType(WarAgentType.WarRocketLauncher,"Base ennemie",str(angle))
		#	setHeading(angle)
		#	return move();
		if(isBlocked()):	
			RandomHeading()
		return move();

def reflexes():
	enemiBases = getPerceptsEnemiesWarBase()
	
	if enemiBases:
		for Ebases in enemiBases:
			setDebugString("Base ennemie"+str(Ebases.getAngle()))
			#broadcastMessageToAgentType(WarAgentType.WarRocketLauncher,"Base ennemie",(str(Ebases.getAngle())))
		#broadcastMessageToAgentType(WarAgentType.WarRocketLauncher,"Base ennemie","")
		#broadcastMessage("defenceurs", "attaque","attaqueeee","")
			broadcastMessageToAll("Base ennemie",(str(Ebases.getAngle())))
			setHeading(Ebases.getAngle())
			if(Ebases.getDistance()>1):
				return move();
			else:
				return idle()
					
	else:		
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "Base ennemie" and message.getDistance < 200): 
				setDebugString("Base ennemie"+str(message.getAngle()))
				setHeading(360)
					
	if isBlocked(): 
		RandomHeading()
	return None


def actionWarExplorer():
	result = reflexes() # Reflexes
	if result:
		return result

    # FSM - Changement d'Ã©tat
	actionWarExplorer.currentState = actionWarExplorer.nextState
	actionWarExplorer.nextState = None

	if actionWarExplorer.currentState:
		return actionWarExplorer.currentState.execute()
	else:
		result = WiggleState.execute()
		actionWarExplorer.nextState = WiggleState
		return result

# Initialisation des variables
actionWarExplorer.nextState = WiggleState
actionWarExplorer.currentState = None
