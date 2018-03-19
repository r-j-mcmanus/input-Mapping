
import main


def TiltLeftMainAttack(Input):
    actions = (InputMapping.InputConstants.Action.Main_Attack, InputMapping.InputConstants.Action.Tilt_Left)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltLeftMainAttack called"
    Input.EatActions(actions)
    return True

    
def TiltRightMainAttack(Input):
    actions = (InputMapping.InputConstants.Action.Main_Attack, InputMapping.InputConstants.Action.Tilt_Right)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltRightMainAttack called"
    Input.EatActions(actions)
    return True

def TiltUpMainAttack(Input):
    actions = (InputMapping.InputConstants.Action.Main_Attack, InputMapping.InputConstants.Action.Tilt_Up)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltUpMainAttack called"
    Input.EatActions(actions)
    return True

def TiltDownMainAttack(Input):
    actions = (InputMapping.InputConstants.Action.Main_Attack, InputMapping.InputConstants.Action.Tilt_Down)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltDownMainAttack called"
    Input.EatActions(actions)
    return True

def MainAttack(Input):
    actions = (InputMapping.InputConstants.Action.Main_Attack)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "MainAttack called"
    Input.EatActions(actions)
    return True

def TiltLeftSpecialAttack(Input):
    actions = (InputMapping.InputConstants.Action.Special_Attack, InputMapping.InputConstants.Action.Tilt_Left)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltLeftSpecialAttack called"
    Input.EatActions(actions)
    return True

    
def TiltRightSpecialAttack(Input):
    actions = (InputMapping.InputConstants.Action.Special_Attack, InputMapping.InputConstants.Action.Tilt_Right)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltRightSpecialAttack called"
    Input.EatActions(actions)
    return True

def TiltUpSpecialAttack(Input):
    actions = (InputMapping.InputConstants.Action.Special_Attack, InputMapping.InputConstants.Action.Tilt_Up)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltUpSpecialAttack called"
    Input.EatActions(actions)
    return True

def TiltDownSpecialAttack(Input):
    actions = (InputMapping.InputConstants.Action.Special_Attack, InputMapping.InputConstants.Action.Tilt_Down)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "TiltDownSpecialAttack called"
    Input.EatActions(actions)
    return True

def SpecialAttack(Input):
    actions = (InputMapping.InputConstants.Action.Special_Attack)
    for action in actions:
        if action not in Input.Actions:
            return False

    print "SpecialAttack called"
    Input.EatActions(actions)
    return True
