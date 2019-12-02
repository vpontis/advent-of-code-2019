import { promises as fs } from "fs";
import _ from "lodash";

const getNumbers = async (): Promise<number[]> => {
  const fileHandle = await fs.open("2/input.txt", "r");
  const contentBuffer = await fileHandle.readFile();
  const content = contentBuffer.toString().trim();
  return content.split(",").map(line => parseInt(line.trim()));
};

const runOperation = (numbers: number[], position: number): number | null => {
  const [opcode, arg1, arg2, destination] = numbers.slice(
    position,
    position + 4
  );

  let result;
  if (opcode === 99) {
    return null;
  }

  const val1 = numbers[arg1];
  const val2 = numbers[arg2];
  if (opcode === 1) {
    result = val1 + val2;
  } else if (opcode === 2) {
    result = val1 * val2;
  } else {
    throw new Error("Frick");
  }

  numbers[destination] = result;

  return position + 4;
};

const runOperationsUntilHalt = (numbers: number[]) => {
  let position = 0;
  while (position != null) {
    position = runOperation(numbers, position);
  }

  return numbers[0];
};

const partOne = async () => {
  const numbers = await getNumbers();
  console.log(numbers);
  numbers[1] = 12;
  numbers[2] = 2;
  runOperationsUntilHalt(numbers);
};

const range = (n: number): number[] => {
  // @ts-ignore
  return Array.from([...Array(100).keys()]);
};

const partTwo = async () => {
  const numbers = await getNumbers();

  const guesses = range(100);
  for (const noun of guesses) {
    for (const verb of guesses) {
      const memory = numbers.slice();
      memory[1] = noun;
      memory[2] = verb;
      const answer = runOperationsUntilHalt(memory);

      console.log(answer);
      if (answer === 19690720) {
        console.log(noun, verb);
        console.log(100 * noun + verb);
        return;
      }
    }
  }
};

const main = async () => {
  // await partOne();
  await partTwo();
};

main();
