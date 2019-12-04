import { promises as fs } from "fs";
import _ from "lodash";
import { rangeBetween } from "../util";

const MIN = 402328;
const MAX = 864247;

const isInputValid = (num: number) => {
  const numString = num.toString();

  const pairs = _.zip(
    Array.from(numString.slice(0, 5)),
    Array.from(numString.slice(1))
  );

  let hasDuplicate = false;
  let hasLonelyTwo = false;

  let index = 0;
  for (const [first, second] of pairs) {
    const num1 = parseInt(first);
    const num2 = parseInt(second);

    if (num1 > num2) {
      return false;
    }

    const isDuplicate = first === second;
    hasDuplicate = isDuplicate || hasDuplicate;

    if (isDuplicate) {
      if (index >= 1 && index <= 5) {
        if (numString[index - 1] !== first && numString[index + 2] !== first) {
          hasLonelyTwo = true;
        }
      }
      if (index === 0 && numString[index + 2] !== first) {
        hasLonelyTwo = true;
      }
      if (index === 4 && numString[index - 1] !== first) {
        hasLonelyTwo = true;
      }
    }

    index += 1;
  }

  return hasDuplicate && hasLonelyTwo;
};

const partOne = async () => {
  const candidates = rangeBetween(MIN, MAX + 1);
  console.log(candidates.length, MAX - MIN);

  const goodCandidates = candidates.filter(isInputValid);
  console.log(goodCandidates);
  console.log(goodCandidates.length);
};

const partTwo = async () => {};

const main = async () => {
  await partOne();
  // await partTwo();
};

main();
