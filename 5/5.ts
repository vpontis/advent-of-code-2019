import { promises as fs } from "fs";
import _ from "lodash";
import { readLine } from "../util";

const getNumbers = async (): Promise<number[]> => {
  const fileHandle = await fs.open("5/input.txt", "r");
  const contentBuffer = await fileHandle.readFile();
  const content = contentBuffer.toString().trim();
  return content
    .split("\n")[0]
    .split(",")
    .map(line => parseInt(line.trim()));
};

const parseOpcode = (opcode: number): { code: number; modes: string[] } => {
  // console.log("opcode", opcode);

  const opcodeStr = opcode.toString();

  const code = parseInt(opcodeStr.slice(opcodeStr.length - 2));

  if (code == 99) {
    return { code, modes: [] };
  }

  const modesStr = opcodeStr.slice(0, opcodeStr.length - 2);

  if (code == 1 || code == 2) {
    const padded = _.padStart(modesStr, 3, "0");
    return { code, modes: padded.split("").reverse() };
  }

  if (code == 3 || code == 4) {
    const padded = _.padStart(modesStr, 1, "0");
    return { code, modes: padded.split("").reverse() };
  }

  if (code == 5 || code == 6) {
    const padded = _.padStart(modesStr, 2, "0");
    return { code, modes: padded.split("").reverse() };
  }

  if (code == 7 || code == 8) {
    const padded = _.padStart(modesStr, 2, "0");
    return { code, modes: padded.split("").reverse() };
  }

  throw Error("opcode fucked");
};

const runOperation = async (
  numbers: number[],
  position: number
): Promise<number | null> => {
  const { code, modes } = parseOpcode(numbers[position]);

  if (code === 99) {
    return null;
  }

  if (code === 1 || code === 2) {
    const [arg1, arg2, destination] = numbers.slice(position + 1, position + 4);

    let result;

    const val1 = modes[0] === "1" ? arg1 : numbers[arg1];
    const val2 = modes[1] === "1" ? arg2 : numbers[arg2];

    if (code === 1) {
      result = val1 + val2;
    } else if (code === 2) {
      result = val1 * val2;
    }
    numbers[destination] = result;

    return position + 4;
  }

  if (code === 3) {
    const destination = numbers[position + 1];
    const input = await readLine("Input?");
    numbers[destination] = parseInt(input);
    return position + 2;
  }

  if (code === 4) {
    const destination = numbers[position + 1];
    const result = modes[0] === "1" ? destination : numbers[destination];
    console.log("result", result);
    return position + 2;
  }

  if (code === 5) {
    const param1 = numbers[position + 1];
    const param2 = numbers[position + 2];
    const firstParam = modes[0] === "1" ? param1 : numbers[param1];

    const shouldJump = firstParam !== 0;
    if (shouldJump) {
      return modes[1] === "1" ? param2 : numbers[param2];
    }
    return position + 3;
  }

  if (code === 6) {
    const param1 = numbers[position + 1];
    const param2 = numbers[position + 2];
    const firstParam = modes[0] === "1" ? param1 : numbers[param1];

    const shouldJump = firstParam === 0;
    if (shouldJump) {
      return modes[1] === "1" ? param2 : numbers[param2];
    }
    return position + 3;
  }

  if (code === 7) {
    const param1 =
      modes[0] === "1" ? numbers[position + 1] : numbers[numbers[position + 1]];
    const param2 =
      modes[1] === "1" ? numbers[position + 2] : numbers[numbers[position + 2]];
    const param3 = numbers[position + 3];

    numbers[param3] = param1 < param2 ? 1 : 0;
    return position + 4;
  }

  if (code === 8) {
    const param1 =
      modes[0] === "1" ? numbers[position + 1] : numbers[numbers[position + 1]];
    const param2 =
      modes[1] === "1" ? numbers[position + 2] : numbers[numbers[position + 2]];
    const param3 = numbers[position + 3];

    numbers[param3] = param1 == param2 ? 1 : 0;
    return position + 4;
  }

  throw new Error("Frick");
};

const runOperationsUntilHalt = async (numbers: number[]) => {
  let position = 0;
  while (position != null) {
    position = await runOperation(numbers, position);
  }

  return numbers[0];
};

const partOne = async () => {
  const numbers = await getNumbers();
  await runOperationsUntilHalt(numbers);
};

const partTwo = async () => {
  const numbers = await getNumbers();
  await runOperationsUntilHalt(numbers);
};

const main = async () => {
  await partTwo();
};

main();
