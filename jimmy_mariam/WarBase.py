#Default Values
DEFAULT_ATTACK_PERCENTAGE = 0.6 #Defalut percentage 
DEFENSE_PERCENTAGE = 0.2 #Change to defense percentage 
ATTACK_PERCENTAGE = 0.8 #Change to attack percentage
BASE_AT_RISK_DISTANCE = 100
TICKS_TO_CREATE = 300

def manageCreations():
	#if( len(WarBase.teamInformation['WarEngineer']) >= 1 and len(WarBase.teamInformation['WarTurret']) <= len(WarBase.teamInformation['WarBase']) ):
	if(WarBase.enableCreation and WarBase.ticksToCreate <= 0 ):
		if ( 'WarRocketLauncher' in WarBase.teamInformation ):
			if(len(WarBase.teamInformation['WarRocketLauncher']) <= 10 ):
				setNextAgentToCreate(WarAgentType.WarRocketLauncher);
				WarBase.needsIdentityTeam = True
				WarBase.needsDefineGroups = True
				WarBase.ticksToCreate = TICKS_TO_CREATE
				return create();
		elif ( 'WarKamikaze' in WarBase.teamInformation ):
			if(len(WarBase.teamInformation['WarKamikaze']) <= 2 ):
				setNextAgentToCreate(WarAgentType.WarKamikaze);
				WarBase.needsIdentityTeam = True
				WarBase.needsDefineGroups = True
				WarBase.ticksToCreate = TICKS_TO_CREATE
				return create();
		elif ( 'WarEngineer' in WarBase.teamInformation ):
			if(len(WarBase.teamInformation['WarEngineer']) == 0):
				if (isAbleToCreate(WarAgentType.WarEngineer) ):
					setNextAgentToCreate(WarAgentType.WarEngineer);
					WarBase.needsIdentityTeam = True
					WarBase.needsDefineGroups = True
					WarBase.ticksToCreate = TICKS_TO_CREATE
					return create();
		elif ( 'WarTurret' in WarBase.teamInformation ):
			if( len(WarBase.teamInformation['WarEngineer']) >= 1 and WarBase.WarTurretId == 0 ):
				setNextAgentToCreate(WarAgentType.WarTurret);
				infoBuildBase = [WarBase.distanceFromOurBase, WarBase.distanceToleranceOurBse]
				#broadcastMessageToAgentType(WarAgentType.WarEngineer, "buildWarWarTurret", infoBuildBase);
				broadcastMessageToAll("buildWarWarTurret", infoBuildBase)
				return idle();

	return None;


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
				WarBase.ourTeam.append( [tmpContent[0], message.getSenderID(), message.getAngle(), message.getDistance()] ); #Agent Role, AngetId

	if (needsUpdate):
		updateTeamInformation()


# Update de variable with the Ids of the agents
#WarBase.teamInformation['WarBase'] = []
#WarBase.teamInformation['WarEngineer'] = []
#WarBase.teamInformation['WarExplorer'] = []
#WarBase.teamInformation['WarKamikaze'] = []
#WarBase.teamInformation['WarRocketLauncher'] = []
#WarBase.teamInformation['WarTurret'] = []
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
		agentObjet = {}
		agentObjet['agentType'] = agentData[0] #Type
		agentObjet['agentId'] = agentData[1] # Id
		agentObjet['agentAngle'] = agentData[2] # Angle
		agentObjet['agentDistance'] = agentData[3] # Distance
		if (not (agentType in WarBase.teamInformation) ):#Jimmy: if does not exists
			WarBase.teamInformation[agentType] = []
			
		#WarBase.teamInformation[agentType].append(agentId)
		WarBase.teamInformation[agentType].append(agentObjet)

def sortAgentGroupBy(agentArray, key):
	return sorted(agentArray, key=lambda agentObjet: agentObjet[key]);

def defineGroups():
	#for agentKey, agentIds in WarBase.teamInformation.items():
	for agentKey, agentArray in WarBase.teamInformation.items():
		totalGroup = 0
		totalAgent = len(WarBase.teamInformation[agentKey])
		#jimmy: Sort by Distance
		agentArray = sortAgentGroupBy(agentArray, 'agentDistance');
		#for agentId in agentIds:
		for agentObjet in agentArray:
			if( agentKey == "WarRocketLauncher" ):
				if( totalGroup < (WarBase.attackPercentage * totalAgent) ): #Send a Message to RocketLaunchers
					totalGroup = totalGroup + 1
					sendMessage(agentObjet['agentId'], "yourGroupIs", ("Attack") );
				else:
					totalGroup = totalGroup + 1
					sendMessage(agentObjet['agentId'], "yourGroupIs", ("Defense") );
			if( agentKey == "WarTurret" ):
				sendMessage(agentObjet['agentId'], "yourGroupIs", ("Defense") );
			if( agentKey == "WarKamikaze" ):
				sendMessage(agentObjet['agentId'], "yourGroupIs", ("Attack") );

			#elif( agentKey == "WarExplorer" ):
			#	sendMessage(agentObjet['agentId'], "yourGroupIs", ("Defense") );




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

		if(WarBase.baseState == "BaseAtRisk"):#Defend base
			WarBase.attackPercentage = DEFENSE_PERCENTAGE
			WarBase.needsIdentityTeam = True
			WarBase.needsDefineGroups = True

		if( WarBase.needsIdentityTeam ):
			broadcastMessageToAll("identifyYou", "")
			WarBase.needsIdentityTeam = False
			
		identifyAgents()
			
		if( WarBase.needsDefineGroups ): #Pending condition
			defineGroups();
			#WarBase.needsDefineGroups = False
		
		
		if(False): # Debug TeamInformation
			setDebugString( getResumenTeamInformation() );

		if(False): # isAbleToCreate
			if(isAbleToCreate(WarAgentType.WarKamikaze)):
				ableCreate = 1
			else:
				ableCreate = 0
			setDebugString( "isAbleToCreate WarKamikaze: " + str(ableCreate) );
			
		
		#broadcastMessageToAll("baseState", WarBase.baseState);

		
		if( getHealth() < getMaxHealth() ):#Jimmy Recovery Heatlth
			return eat();
		
		resultCreations = manageCreations();#Jimmy: If is possible create a agent
		
		if( resultCreations ):
			return resultCreations;

		return idle();

def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "EnemyBaseFound" and WarBase.baseState == "BaseOk"):#Jimmy change strategy
			WarBase.attackPercentage = ATTACK_PERCENTAGE
			WarBase.needsIdentityTeam = True
			WarBase.needsDefineGroups = True
		elif(message.getMessage() == "identifyYou"):
			#reply to Base
			sendMessage(message.getSenderID(), "responseIdentify", ("WarBase") );
		elif(message.getMessage() == "whereAreYou"):
			#setDebugString("OurBaseIsHere");
			sendMessage(message.getSenderID(), "OurBaseIsHere", "");
		elif( message.getMessage() == "EnemyBase" and False ) :
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
	
		
	
def reflexes():
	percepts = getPerceptsEnemies()
	enemyFound = None
	for percept in percepts:
		if( percept.getType() == WarAgentType.WarKamikaze ):
			enemyFound = percept
			break
		elif( percept.getType() == WarAgentType.WarRocketLauncher ):
			enemyFound = percept
			break
		elif( percept.getType() == WarAgentType.WarExplorer ):
			enemyFound = percept
			break
		elif( percept.getType() == WarAgentType.WarEngineer and False ):#Disabled
			enemyFound = percept
			break
		elif( percept.getType() == WarAgentType.WarTurret and False ):#Disabled
			enemyFound = percept
			break

	if (enemyFound):
		broadcastMessageToAll("ThereAreEnemiesInOurBase", "")
		#broadcastMessageToAgentType(WarAgentType.WarRocketLauncher, "ThereAreEnemiesInOurBase", "");#str to cast string
		WarBase.baseState = "BaseAtRisk"
		setDebugString("BaseAtRisk distance:" + str(percept.getDistance()) );
		setHeading(enemyFound.getAngle())
		setDebugString(WarBase.baseState);
	else:
		WarBase.baseState = "BaseOk"
		setDebugString(WarBase.baseState);

	
	return None

def actionWarBase():
	validateMainMessages()
	WarBase.ticksToCreate = WarBase.ticksToCreate - 1;
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
WarBase.baseState = "BaseOk"
WarBase.needsIdentityTeam = True
WarBase.needsDefineGroups = True
WarBase.baseEnemy = []; #Array with the enemy bases location.
WarBase.WarTurretId = 0

WarBase.attackPercentage = DEFAULT_ATTACK_PERCENTAGE
WarBase.enableCreation = False
WarBase.distanceFromOurBase = 100
WarBase.distanceToleranceOurBse = 20
WarBase.ticksToCreate = 10
#WarBase.ticksToCreate = TICKS_TO_CREATE
