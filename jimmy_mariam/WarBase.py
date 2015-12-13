ATTACKPERCENTAGE = 0.5

#def identifyOurTeam:
#	WarBase.ourTeam = ();

#Method to identify the Agents
def identifyAgents():
	WarBase.ourTeam = []
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "responseIdentify"):
			tmpContent = message.getContent()
			WarBase.ourTeam.append( [tmpContent[0], message.getSenderID()] ); #Agent Role, AngetId

	updateTeamInformation()


# Update de variable with the Ids of the agents
def updateTeamInformation():
	WarBase.teamInformation = {}
	WarBase.teamInformation['WarBase'] = []
	WarBase.teamInformation['WarEngineer'] = []
	WarBase.teamInformation['WarExplorer'] = []
	WarBase.teamInformation['WarKamikaze'] = []
	WarBase.teamInformation['WarRocketLauncher'] = []
	WarBase.teamInformation['WarTurret'] = []
	for agentData in WarBase.ourTeam:
		agentType = agentData[0] #Type
		agentId = agentData[1] # Id
		if (not (agentType in WarBase.teamInformation) ):#Jimmy: if does not exists
			WarBase.teamInformation[agentType] = []
			
		WarBase.teamInformation[agentType].append(agentId)

	

def defineGroups():
	for agentKey, agentIds in WarBase.teamInformation.items():
		totalGroup = 0
		totalAgent = len(WarBase.teamInformation[agentKey])
		for agentId in agentIds:
			if( agentKey == "WarRocketLauncher" ):
				if( totalGroup < (ATTACKPERCENTAGE * totalAgent) ): #Send a Message to RocketLaunchers
					totalGroup = totalGroup + 1
					sendMessage(agentId, "yourGroupIs", ("Attack") );
				else:
					totalGroup = totalGroup + 1
					sendMessage(agentId, "yourGroupIs", ("Defense") );
			#elif( agentKey == "WarExplorer" ):
			#	sendMessage(agentId, "yourGroupIs", ("Defense") );



def getResumenTeamInformation():
	resumen = "TeamResume: "
	for agentKey, agentIds in WarBase.teamInformation.items():
		strIds = ','.join(str(e) for e in agentIds)
		resumen = resumen + " " + str(agentKey) + ": " + str(strIds)
	return resumen;


def createAgent():
	setNextAgentToCreate(WarAgentType.WarKamikaze)
	if( isAbleToCreate(WarAgentType.WarKamikaze) ):
		create()
		return True;
	else:
		return False;

class defaultState(object):
	@staticmethod
	def execute():
		WarBase.nextState = defaultState;
		messages = getMessages();

		if( WarBase.needsIdentityTeam ):
			broadcastMessageToAll("identifyYou", "")
			WarBase.needsIdentityTeam = False
			
		identifyAgents()
			
		if(True): #Pending condition
			defineGroups();
		

		#if( createAgent() ):
		#	setDebugString("Created");

		
		for message in messages:
			if( message.getMessage() == "EnemyBase" and False ) :
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

				#WarBase.baseState = "ExBasEAngle: " + arrContent[0] + " \nExD: " + arrContent[1] + " \nExpH: " + arrContent[2] + " BaseEA: " + str(baseEnemyAngle) + " baseED:" + str(baseEnemyDistance) + " ExpAn: " +  str(message.getAngle()) + " ExpD" + str(message.getDistance());
				#debugStr = "RocketLaunchersAttack: (" + str(message.getAngle()) + ") Angle ";
				#setDebugString(debugStr);
				infoBase = ( str(message.getAngle()), str(message.getDistance()), arrContent[0], arrContent[1], arrContent[2] )  
				broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "RocketLaunchersAttack", infoBase);#str to cast string
		
		setDebugString(WarBase.baseState);
		if(True): # Debug TeamInformation
			setDebugString( getResumenTeamInformation() );
		
		broadcastMessageToAll("baseState", WarBase.baseState);
		return idle();

def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			#reply to Base
			sendMessage(message.getSenderID(), "responseIdentify", ("WarBase") );
		if(message.getMessage() == "whereAreYou"):
			setDebugString("OurBaseIsHere");
			sendMessage(message.getSenderID(), "OurBaseIsHere", "");
		
	
def reflexes():
	percepts = getPercepts()
	for percept in percepts:
		#Jimmy: Only Rocket Launchers
		if (percept.getType().equals(WarAgentType.WarRocketLauncher) and isEnemy(percept) and percept.getDistance() <= 30 ):
			if(False): #Disable
				broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemiesInOurBase", "");#str to cast string
				WarBase.baseState = "BaseAtRisk"
			#setDebugString("ThereAreEnemiesInOurBase distance:" + str(percept.getDistance()) );
			
	return None

def actionWarBase():
	WarBase.baseState = "BaseOk" #Default State
	validateMainMessages()
	result = reflexes() # Reflexes
	if result:
		return result
		
	# FSM - Changement d'Ã©tat
	WarBase.currentState = WarBase.nextState
	WarBase.nextState = None

	if WarBase.currentState:
		return WarBase.currentState.execute()
	else:
		result = defaultState.execute()
		WarBase.nextState = defaultState
		return result;


WarBase.nextState = defaultState
WarBase.currentState = None
WarBase.ourTeam = [];
WarBase.teamInformation = {};
WarBase.baseState = "sateOk"
WarBase.needsIdentityTeam = True
WarBase.baseEnemy = []; #Array with the enemy bases location.
