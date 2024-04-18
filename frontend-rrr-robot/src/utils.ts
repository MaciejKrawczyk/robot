
type Action = {
    id: number;
    name: string;
    body: string;
};

export function parseCommandsToCode(input: { [key: string]: string }): Action[] {
    const result: Action[] = [];
    const pattern = /(\w+)-(\d+)/;

    const tempStorage: { [key: number]: { id: number; name?: string; body?: string } } = {};

    for (const key in input) {
        const match = key.match(pattern);
        if (match) {
            const type = match[1];
            const index = parseInt(match[2], 10);

            if (!tempStorage[index]) {
                tempStorage[index] = { id: index };
            }

            if (type === 'name') {
                tempStorage[index].name = input[key];
            } else if (type === 'body') {
                tempStorage[index].body = input[key];
            }
        }
    }

    for (const index in tempStorage) {
        result.push(tempStorage[index] as Action);
    }

    return result;
}