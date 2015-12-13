
#def processMessages


def actionWarExplorer():
    arrStates = ["explore", "takeFood", "returnToBase"]
    agentState = "explore"
    arrInfoToProcess = {} # https://bdhacker.wordpress.com/2010/02/27/python-tutorial-dictionaries-key-value-pair-maps-basics/

    percepts = getPercepts();
    arrInfoToProcess['foundFood'] = False ##Jimmy: Boolean Var to know if he have food
    arrInfoToProcess['bagFull'] = isBagFull()

    for percept in percepts:
        #if( percept.getType().equals(WarAgentType.WarFood) and isBagFull() ): #send the message only if the bag is full
        if( percept.getType().equals(WarAgentType.WarFood)): #send the message only if the bag is full
            arrInfoToProcess['foundFood'] = True
            sendMessageToExplorers("Food", "There are food!");
            arrInfoToProcess['perceptFood'] = percept
            if (not isBagFull() ):
                agentState = "takeFood"
                return processState(agentState, arrInfoToProcess)

    if( isBagFull() ):
        agentState = "returnToBase"

    messages = getMessages();
    for message in messages :
        if(message.getSenderType() == WarAgentType.WarExplorer):
            if ( (not isBagFull()) and (not arrInfoToProcess['foundFood']) ):
                agentState = "goToFoundFood"
                arrInfoToProcess['goToFoundFood'] = message;
                ##return move();
    

    

    if (isBlocked()) :
        RandomHeading()

    return processState(agentState, arrInfoToProcess)

def processState(agentState, arrInfoToProcess):

    if (agentState == "explore"):
        setDebugString("Exploring")
        return move()

    elif (agentState == "takeFood"):
        setDebugString("takeFood")
        percept = arrInfoToProcess['perceptFood']
        if((percept.getDistance() < getMaxDistanceTakeFood()) and (not isBagFull())):
            setHeading(percept.getAngle());
            setDebugString("Take food")
            return take()
        elif (not isBagFull()) :
            setHeading(percept.getAngle());
            return move()

    elif (agentState == "goToFoundFood"):
        setDebugString("goToFoundFood")
        message = arrInfoToProcess['goToFoundFood']
        setHeading(message.getAngle());
        return move()
    elif (agentState == "returnToBase"):
        setDebugString("Bag full return base")
        
        percepts = getPerceptsAlliesByType(WarAgentType.WarExplorer)

        if((percepts is None) or (len(percepts) == 0)):
            broadcastMessageToAll("whereAreYou", "");
            return move()

        else :
            base = percepts[0];
            if(base.getDistance() > maxDistanceGive()):
                setHeading(base.getAngle());
                return move()
            else:
                setIdNextAgentToGive(base.getID());
                return give()

    else :
        return customMove()
        

def customMove():
    setRandomHeading(5)
    return move();


