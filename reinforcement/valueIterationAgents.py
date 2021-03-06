# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

  
import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** THIS IS DIFFERENT? YOUR CODE HERE ***"
        #Run through iterations with for loop
        
        for iteration in range(self.iterations):
            valueOfIteration = self.values.copy()
            for curState in self.mdp.getStates():
                allActions = self.mdp.getPossibleActions(curState)
                if self.mdp.isTerminal(curState):
                    continue
                else:
                    allStatesList = []
                    for curAction in allActions:
                        CurReward = self.getQValue(curState, curAction)
                        allStatesList.append(CurReward)
                    valueOfIteration[curState] = max(allStatesList)
            self.values = valueOfIteration

            


                

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #Get the list of transistions in the mdp
        transistions = self.mdp.getTransitionStatesAndProbs(state, action)
        #Empty list we will use to add up all values
        addValues = 0
        #Go through one at a time
        for transistion in transistions:
            Goal = self.mdp.getReward(state, action, transistion[0])
            addValues += transistion[1]*(Goal + self.discount*(self.getValue(transistion[0])))   
        return addValues
        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actionState = util.Counter()
        for i in self.mdp.getPossibleActions(state):
            actionState[i] = self.getQValue(state, i)
        newPolicy = actionState.argMax()
        return newPolicy
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.

    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #Get All Possible States 
        allStates = self.mdp.getStates()
        #Get the amount of all possible states
        numOfStates = len(allStates)
        #Iterate through game boards
        for i in range(self.iterations):
            #Must select states one by one: So use % to remainder as 1 through numOfStates
            curState = allStates[i % numOfStates]
            #Check if Terminal
            if self.mdp.isTerminal(curState):
                continue
            #If Not Terminal, then finish 
            else:
                values = []
                for curAction in self.mdp.getPossibleActions(curState):
                    curQValue = self.computeQValueFromValues(curState, curAction)
                    values.append(curQValue)
                self.values[curState] = max(values)
                    


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #Step 1 is to initiate Priority Queue 
        thePriorityQ = util.PriorityQueue()
        #Step 2 is to have predeccesors 
        predecessors = {}
        #Go Through Each State
        for state in self.mdp.getStates():
          if not self.mdp.isTerminal(state):
            for action in self.mdp.getPossibleActions(state):
              for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                if nextState in predecessors:
                  predecessors[nextState].add(state)
                else:
                  predecessors[nextState] = {state}

        for state in self.mdp.getStates():
          if not self.mdp.isTerminal(state):
            values = []
            for action in self.mdp.getPossibleActions(state):
              q_value = self.computeQValueFromValues(state, action)
              values.append(q_value)
            diff = abs(max(values) - self.values[state])
            thePriorityQ.update(state, - diff)

        for i in range(self.iterations):
          if thePriorityQ.isEmpty():
            break
          temp_state = thePriorityQ.pop()
          if not self.mdp.isTerminal(temp_state):
            values = []
            for action in self.mdp.getPossibleActions(temp_state):
              q_value = self.computeQValueFromValues(temp_state, action)
              values.append(q_value)
            self.values[temp_state] = max(values)

          for p in predecessors[temp_state]:
            if not self.mdp.isTerminal(p):
              values = []
              for action in self.mdp.getPossibleActions(p):
                q_value = self.computeQValueFromValues(p, action)
                values.append(q_value)
              diff = abs(max(values) - self.values[p])
              if diff > self.theta:
                thePriorityQ.update(p, -diff)

                            


        

