
#def processMessages

def actionWarExplorer():
    arrStates = ["explore", "returnToBase"]
    agentState = "explore"

    percepts = getPercepts();
    foundFood = False ##Jimmy: Boolean Var to know if he have food
    enemyBaseFood = False ##Jimmy: Boolean Var to know if he have food

    # perceptBase = getPerceptsEnemiesByType(WarAgentType.WarBase);
    # if((perceptBase is None) or (len(perceptBase) == 0)):
    #     enemyBaseFood = False
    #     #return move();
    # else:
    #     enemyBaseFood = True
    #     setDebugString("Enemy Base found");
    #     broadcastMessageToAgentType(WarAgentType.WarBase, "EnemyBaseHere", "");
    #     setHeading(perceptBase.getAngle());
    #     return move()

    for percept in percepts:
        if(percept.getType().equals(WarAgentType.WarBase) and isEnemy(percept) ):
            enemyBaseFood = True
            setDebugString("Enemy Base found");
            broadcastMessageToAgentType(WarAgentType.WarBase, "EnemyBaseHere", "");
            #setHeading(percept.getAngle());
            #return move();

        if(percept.getType().equals(WarAgentType.WarFood)):
            foundFood = True
            if (isBagFull()):
                broadcastMessageToAgentType(WarAgentType.WarExplorer, "ThereArefood", "ThereArefood");
                #sendMessageToExplorers("Food", "ThereArefood!");
                setDebugString("ThereAreFood")

            if((percept.getDistance() < getMaxDistanceTakeFood()) and (not isBagFull())):
                setHeading(percept.getAngle());
                setDebugString("Take food")
                agentState = "takeFood"
                return take();

            elif (not isBagFull()) :
                setHeading(percept.getAngle());
    
    if (isBagFull()) :
        agentState = "goToBase"
        setDebugString("Bag full return base")
        broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYou", "");

        percepts = getPerceptsAlliesByType(WarAgentType.WarBase);

        if((percepts is None) or (len(percepts) == 0)):
            #broadcastMessageToAll("whereAreYou", "");
            broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYou", "");
        else :
            base = percepts[0];

            if(base.getDistance() > maxDistanceGive()):
                setHeading(base.getAngle());
                return move();
            else:
                setIdNextAgentToGive(base.getID());
                setDebugString("explore again")
                return give();
    


    messages = getMessages();
    for message in messages :
        if( message.getMessage() == "ThereAreFood" and (not isBagFull() ) ) :
            #if( message.getContent() ):
        
            setHeading(message.getAngle());
            setDebugString("go to found food")
            return move();
           
                ##setDebugString("Find food");
        #elif( message.getMessage() == "EnemyBaseHere" ) :
        #    return move();
        #elif( message.getMessage() == "whereAreYou" ) :
        elif( message.getMessage() == "OurBaseIsHere" and agentState == "goToBase" ) :
            setHeading(message.getAngle());
            return move();

    if (isBlocked()) :
        RandomHeading()

    return customMove()

def customMove():
    setRandomHeading(3)
    return move();


