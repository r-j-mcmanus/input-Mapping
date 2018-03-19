

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
            Action_one = 1 
            Action_two = 2
            Action_three = 3
            Action_four = 4
            Action_five = 5
            Action_six = 6
            Action_seven = 7
            Main_Attack = 8
            Tilt_Right = 9
            Tilt_Left = 10
            Tilt_Up = 11
            Tilt_Down = 12
            Special_Attack = 13

        class State:
            Right = 1
            Left = 2 
            Up = 3
            Down = 4

        class Range:
            Range_one = 1
            Range_two = 2

    #------------------------------------------------#

    class ContextID:
        Directions = 0
        Attacking  = 1
        
        IDs = [self.Directions, self.Attacking]
        

    class ContextMaker:
        IDMap = {ContextID.Directions : _Directions,
                 ContextID.Attacking  : _Attacking}

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
 

    #------------------------------------------------#

    class InputContext:

        _actionMap = {}#{button: action}
        _stateMap  = {}#{button: state}

        def __init__(self, contextID):
            _actionMap, _stateMap = ContextMaker.Make(contextID)

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

        def _make(self, contextID):
            pass

    #------------------------------------------------#

    class MappedInput:
        Actions = set([])
        States  = set([])
        
        def EatAction(self, action):
            self.Actions.remove(action)

        def EatActions(self, actions):
            for action in actions:
                EatAction(action)

        def EatState(self, state):
            self.States.remove(state)

    #------------------------------------------------#

    class InputMapper:

        _inputContext = {}#{contextID: InputContext}
        _activeContexts = set([])
        _mappedInput = MappedInput()
        _callbackTable = {}#(int, inputCallback)

        def __init__(self):
            #make all contexts
            for ID in ContextID.IDs
                _inputContext[ID] = InputContext(ID)

        def Clear(self):
            _mappedInput.Actions.clear()
            _mappedInput.States.clear()
            # Note: we do NOT clear states, because they need to remain set
	        # across frames so that they don't accidentally show "off" for
	        # a tick or two while the raw input is still pending.

            # Play with this to understand it
        
        def SetRawButtonState(self, button, pressed, previouslyPressed):
            action = 1
            state  = 2

            #checks if a button was newly pressed to prevent being called again
            if pressed and !previouslypressed:
                if _MapButtonToAction(button, action):
                    _mappedInput.Actions.append(action)
                    return

            #checks if a button if held
            if pressed:
                if _MapButtonToState(button, state):
                    _mappedInput.States.append(state)
                    return

            _MapAndEatButton(button)

        def Dispatch(self):
            _input = _mappedInput
            for callback in CallbackTable.values():
                callback(_input)

        def AddCallback(self, callback, priority):
            _callbackTable.append((priority, callback))

        def pushContext(self, contextID):
            _activeContexts.add(_inputContext[contextID])

        def popContext():
            _activeContexts.remove(_inputContext[contextID])

        def _MapButtonToAction(self, button, actions):
            for context in _activeContexts:
                if context.MapButtonToAction(abutton, action):
                    return True
            return False

        def _MapButtonToState(self, button, state):
            for context in _activeContexts:
                if context.MapButtonToState(button, state):
                    return True
            return False

        def _MapAndEatButton(self, button):
            action = 1
            state  = 1

            if _MapButtonToAction(button, action):
                _mappedInput.EatAction(action)

            if _MapButtonToState(button, state):
                _mappedInput.EatState(state)


        
















