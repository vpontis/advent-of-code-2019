export const range = (n: number): number[] => {
  // @ts-ignore
  return Array.from([...Array(n).keys()]);
};

export const rangeBetween = (from: number, to: number) => {
  const firstRange = range(to - from);
  return firstRange.map(num => num + from);
};

import * as inquirer from "inquirer";

export const readLine = async (
  question: string,
  type: string = "number"
): Promise<string> => {
  const { answer } = await inquirer.prompt([
    {
      type,
      name: "answer",
      message: question
    }
  ]);
  return answer;
};
