ATTACKPERCENTAGE = 0.5
ENABLE_CREATION = False

DISTANCE_TOUR_FROM_BASE = 100
DISTANCE_TOUR_TOLERANCE = 20

def manageCreations():
	#if( len(WarBase.teamInformation['WarEngineer']) >= 1 and len(WarBase.teamInformation['WarTurret']) <= len(WarBase.teamInformation['WarBase']) ):
	if(ENABLE_CREATION):
		if( len(WarBase.teamInformation['WarEngineer']) >= 1 and WarBase.WarTurretId == 0 ):
			setNextAgentToCreate(WarAgentType.WarTurret);
			infoBuildBase = [DISTANCE_TOUR_FROM_BASE, DISTANCE_TOUR_TOLERANCE]
			#broadcastMessageToAgentType(WarAgentType.WarEngineer, "buildWarWarTurret", infoBuildBase);
			broadcastMessageToAll("buildWarWarTurret", infoBuildBase)
			return idle();
		elif(len(WarBase.teamInformation['WarEngineer']) == 0):
			setNextAgentToCreate(WarAgentType.WarEngineer);
			if (isAbleToCreate(WarAgentType.WarEngineer) ):
				WarBase.needsIdentityTeam = True
				WarBase.needsDefineGroups = True
				return create();
		elif(len(WarBase.teamInformation['WarRocketLauncher']) <= 5 ):
			setNextAgentToCreate(WarAgentType.WarRocketLauncher);
			if (isAbleToCreate(WarAgentType.WarRocketLauncher) ):
				WarBase.needsIdentityTeam = True
				WarBase.needsDefineGroups = True
				return create();
		elif(len(WarBase.teamInformation['WarKamikaze']) <= 2 ):
			setNextAgentToCreate(WarAgentType.WarKamikaze);
			if (isAbleToCreate(WarAgentType.WarKamikaze) ):
				WarBase.needsIdentityTeam = True
				WarBase.needsDefineGroups = True
				return create();

			
			
			

def createAgent():
	setNextAgentToCreate(WarAgentType.WarKamikaze)
	if( isAbleToCreate(WarAgentType.WarKamikaze) ):
		create()
		return True;
	else:
		return False;

#def identifyOurTeam:
#	WarBase.ourTeam = ();

#Method to identify the Agents
def identifyAgents():
	needsUpdate = False
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "responseIdentify"):
			needsUpdate = True;
		

	if(needsUpdate):
		WarBase.ourTeam = []
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "responseIdentify"):
				tmpContent = message.getContent()
				WarBase.ourTeam.append( [tmpContent[0], message.getSenderID()] ); #Agent Role, AngetId

	if (needsUpdate):
		updateTeamInformation()


# Update de variable with the Ids of the agents
def updateTeamInformation():
	WarBase.teamInformation = {}

	#WarBase.teamInformation['WarBase'] = []
	#WarBase.teamInformation['WarEngineer'] = []
	#WarBase.teamInformation['WarExplorer'] = []
	#WarBase.teamInformation['WarKamikaze'] = []
	#WarBase.teamInformation['WarRocketLauncher'] = []
	#WarBase.teamInformation['WarTurret'] = []
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
			if( agentKey == "WarTurret" ):
				sendMessage(agentId, "yourGroupIs", ("Defense") );

			#elif( agentKey == "WarExplorer" ):
			#	sendMessage(agentId, "yourGroupIs", ("Defense") );




def getResumenTeamInformation():
	resumen = "TeamResume: "
	for agentKey, agentIds in WarBase.teamInformation.items():
		strIds = ','.join(str(e) for e in agentIds)
		resumen = resumen + " " + str(agentKey) + ": " + strIds

	return resumen;

class defaultState(object):
	@staticmethod
	def execute():
		WarBase.nextState = defaultState;
		messages = getMessages();

		if( WarBase.needsIdentityTeam ):
			broadcastMessageToAll("identifyYou", "")
			WarBase.needsIdentityTeam = False
			
		identifyAgents()
			
		if( WarBase.needsDefineGroups ): #Pending condition
			defineGroups();
			#WarBase.needsDefineGroups = False
		

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

		if(False): # isAbleToCreate
			if(isAbleToCreate(WarAgentType.WarKamikaze)):
				ableCreate = 1
			else:
				ableCreate = 0
			setDebugString( "isAbleToCreate WarKamikaze: " + str(ableCreate) );
			
		
		broadcastMessageToAll("baseState", WarBase.baseState);

		
		if( getHealth() < getMaxHealth() ):#Jimmy Recovery Heatlth
			return eat();
		
		resultCreations = manageCreations();#Jimmy: If is possible create a agent
		
		if( resultCreations ):
			return resultCreations;

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
		if(True): #Disable
			if (percept.getType().equals(WarAgentType.WarRocketLauncher) and isEnemy(percept) and percept.getDistance() <= 30 ):
				broadcastMessageToAll("ThereAreEnemiesInOurBase", "")
				#broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemiesInOurBase", "");#str to cast string
				WarBase.baseState = "BaseAtRisk"
				setDebugString("ThereAreEnemiesInOurBase distance:" + str(percept.getDistance()) );
			
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
WarBase.needsDefineGroups = True
WarBase.baseEnemy = []; #Array with the enemy bases location.
WarBase.WarTurretId = 0
