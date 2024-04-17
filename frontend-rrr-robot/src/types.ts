export type Position = {
    theta1: number
    theta2: number
    theta3: number
    x: number
    y: number
    z: number
}

type CommandSleep = {
    name: 'sleep'
    body: '1s' | '2s' | '3s' | '4s'
}

type CommandMoveTo = {
    name: 'move-to'
    body: number
}

export type Command = CommandMoveTo | CommandSleep