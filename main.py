

#https://www.gamedev.net/articles/programming/general-and-gameplay-programming/designing-a-robust-input-handling-system-for-games-r2975



#raw input gathering

#input mapping 
#despatching 

#high level handler



#contexts dictate what inputs are available eg menu, title screen, mainn game


#Types of input:
# 1. Actions - single thing eg. cast spell, open door - one off actions that occure when buttion is pressed (releced), do not depend on key repeat
# 2. States - continuous activities - running shooting. Will be a binary flag - state is on or off. If on, the corrisponding action is performed , if off then not
# 3. Ranges - input can take a range of values (say 0,1 or -1, 1) good for analoge input 

# Each context defiens an input map - takes raw input and translate to final type of input, "an input mapper is really a set of code that can convert raw input IDs to high-level context-dependent IDs"
# one to one fn between context and inputmap
# More than one context can be active at one, eg. one for walking/running around willbe used all the time, and others might be dependent on things such as the current weapon
#one posible implimentation is a list of contexts, and if one reacts then stop, if not pass to the next in the list
# "Chain of Responsibility pattern"


# callbacks code design 
# (Callback - a fn pointer)
# 1. Each frame get raw input
# 2. Evaluate current contexts to find list of actions, states and ranges
# 3. put input into approprite structure 
# 4. pass structure through ordered list of callbacks
# 5. if callback uses input, remove input from structure

# Summery: 
# raw input -> context List -> input data structure -> callback list -> Callback data structure -> perform callbacks


class InputMapping:
    class InputConstants:
        class Action:
            #Lower Actions
            Main_Attack = 1
            Tilt_Right = 2
            Tilt_Left = 3
            Tilt_Up = 4
            Tilt_Down = 5
            Special_Attack = 6
            #Higher Actions
            Tilt_Left_Main_Attack = 101
            Tilt_Up_Main_Attack = 102
            Tilt_Down_Main_Attack = 103
            Tilt_Right_Main_Attack = 104
            Tilt_Left_Special_Attack = 105
            Tilt_Up_Special_Attack = 106
            Tilt_Down_Special_Attack = 107
            Tilt_Right_Special_Attack = 108

        class State:
            Right = 1
            Left = 2 
            Up = 3
            Down = 4

        class Range:
            Range_one = 1
            Range_two = 2

    #------------------------------------------------#

    class _LowerContextID:
        Directions = 0
        Attacking  = 1
        
        IDs = [self.Directions, self.Attacking]
        

    class LowerContextMaker:
        IDMap = {_LowerContextID.Directions : _Directions,
                 _LowerContextID.Attacking  : _Attacking}

        def Make(self, ID):
            return _IDMap[ID]()
            
        def _Directions(self):
            action = {K_a: InputConstants.Action.Tilt_Left,
                      K_d: InputConstants.Action.Tilt_Right,
                      K_s: InputConstants.Action.Tilt_Down,
                      K_w: InputConstants.Action.Tilt_Up}
            state  = {K_a: InputConstants.State.Left,
                      K_d: InputConstants.State.Right,
                      K_s: InputConstants.State.Down,
                      K_w: InputConstants.State.Up}
            return action, state

        def _Attacking(self):
            action = {K_down : InputConstants.Action.Main_Attack,
                      K_Right: InputConstants.Action.Special_Attack}
            state  = {}
            return action, state

    class _HigherContextID:
        TiltAttack = 0
        
        IDs = [self.TiltAttack]

    class HigerContextMaker:
        IDMap = {_HigherContextID.TiltAttack  : _Attacking}

        def Make(self, ID):
            return _IDMap[ID]()
            
        def _TiltAttack(self):
            action = {(InputConstants.Action.Main_attack   , InputConstants.Action.Tilt_Right) : InputConstants.Action.Tilt_Right_Main_Attack,
                      (InputConstants.Action.Main_attack   , InputConstants.Action.Tilt_Left)  : InputConstants.Action.Tilt_Left_Main_Attack,
                      (InputConstants.Action.Main_attack   , InputConstants.Action.Tilt_Up)    : InputConstants.Action.Tilt_Up_Main_Attack,
                      (InputConstants.Action.Main_attack   , InputConstants.Action.Tilt_Down)  : InputConstants.Action.Tilt_Down_Main_Attack, 
                      (InputConstants.Action.Special_attack, InputConstants.Action.Tilt_Right) : InputConstants.Action.Tilt_Right_Special_Attack,
                      (InputConstants.Action.Special_attack, InputConstants.Action.Tilt_Left)  : InputConstants.Action.Tilt_Left_Special_Attack,
                      (InputConstants.Action.Special_attack, InputConstants.Action.Tilt_Up)    : InputConstants.Action.Tilt_Up_Special_Attack,
                      (InputConstants.Action.Special_attack, InputConstants.Action.Tilt_Down)  : InputConstants.Action.Tilt_Down_Special_Attack}
            state = {}
            return action, state

    #------------------------------------------------#

    class InputLowerContext:

        _actionMap = {}#{button: action}
        _stateMap  = {}#{button: state}

        def __init__(self, lowerContextID):
            _actionMap, _stateMap = LowerContextMaker.Make(lowerContextID)

        def MapButtonToAction(self, button, action):
            # map a raw button to an action
            if button in _actionMap.keys():
                action = _actionMap[button]
                return True
            return False

        def MapButtonToState(self, button, action):
            # map a raw button to a state
            if button in _stateMap.keys():
                action = _stateMap[button]
                return True
            return False

    class InputHigherContext:

        _actionMap = {}#{combo: action}
        _stateMap  = {}#{combo: state}

        def __init__(self, HigherContextID):
            _actionMap, _stateMap = HigherContextMaker.Make(lowerContextID)

        def MapLowerToHigher(self, mappedInput, action):
            # map a combo of actions to to an action
            for combo in _actionMap.keys():
                if mappedInput.Actions >= combo #check is one is subset of other
                    mappedInput.Actions -= combo
                    mappedInput.Actions.add(_actionMap[combo])

        #def MapButtonToState(self, button, action):
        #    # map a raw button to a state
        #    if button in _stateMap.keys():
        #        action = _stateMap[button]
        #        return True
        #    return False

    #------------------------------------------------#

    class MappedInput:
        Actions = set([])
        States  = set([])
        
        def EatAction(self, action):
            self.Actions.remove(action)

        def EatState(self, state):
            self.States.remove(state)

    #------------------------------------------------#

    class InputMapper:

        _inputLowerContext = {}                  #{contextID: InputContext}
        _activeLowerContexts = set([])
        _inputHigherContext = {}                 #{contextID: InputContext}
        _activeHigherContexts = set([])
        _mappedInput = MappedInput()
        _callbackTable = {}                      #(int, inputCallback)

        def __init__(self):
            #make all contexts
            for ID in _LowerContextID.IDs
                _inputLowerContext[ID] = InputLowerContext(ID)
            for ID in _HigherContextID.IDs
                _inputHigherContext[ID] = InputHigherContext(ID)

        def Clear(self):
            self._mappedInput.Actions.clear()
            self._mappedInput.States.clear()
            # Note: we do NOT clear states, because they need to remain set
	        # across frames so that they don't accidentally show "off" for
	        # a tick or two while the raw input is still pending.

            # Play with this to understand it
        
        def _RawToLowerInput(self, button, pressed, previouslyPressed):
            action = 1
            state  = 2

            #checks if a button was newly pressed to prevent being called again for actions
            if pressed and !previouslypressed:
                if _MapButtonToAction(button, action):
                    self._mappedInput.Actions.append(action)
                    return

            #checks if a button if held for states
            if pressed:
                if _MapButtonToState(button, state):
                    self._mappedInput.States.append(state)
                    return

            _MapAndEatButton(button) #not sure why this is here
            
        def Dispatch(self):
            _input = self._mappedInput
            for callback in CallbackTable.values():
                callback(_input)

        def AddCallback(self, callback, priority):
            _callbackTable.append((priority, callback))

        def pushLowerContext(self, contextID):
            _activeLowerContexts.add(_inputLowerContext[contextID])

        def popLowerContext():
            _activeLowerContexts.remove(_inputLowerContext[contextID])

        def pushHigherContext(self, contextID):
            _activeHeigherContexts.add(_inputHeigherContext[contextID])

        def popHeigherContext():
            _activeHeigherContexts.remove(_inputHeigherContext[contextID])

        def _MapButtonToAction(self, button, actions):
            for context in _activeLowerContexts:
                if context.MapButtonToAction(button, action):
                    return True
            return False

        def _MapButtonToState(self, button, state):
            for context in _activeLowerContexts:
                if context.MapButtonToState(button, state):
                    return True
            return False

        def _LowerToHigherInput(self):
            for context in _activeHigherContexts:
                context.MapLowerToHigher(_mappedInput)

        def _MapAndEatButton(self, button):
            action = 1
            state  = 1

            if _MapButtonToLowerAction(button, action):
                self._mappedInput.EatAction(action)

            if _MapButtonToLowerState(button, state):
                self._mappedInput.EatState(state)


        
















