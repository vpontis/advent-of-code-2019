import { promises as fs } from "fs";
import _ from "lodash";

const massToFuel = (mass: number): number => {
  const fuel = Math.floor(mass / 3) - 2;
  if (fuel <= 0) {
    return 0;
  }

  return fuel;
};

const getRecursiveFuel = (mass: number): number => {
  const fuel = massToFuel(mass);
  if (fuel === 0) {
    return 0;
  }

  return fuel + getRecursiveFuel(fuel);
};

const getMasses = async (): Promise<number[]> => {
  const fileHandle = await fs.open("1/input.txt", "r");
  const contentBuffer = await fileHandle.readFile();
  const content = contentBuffer.toString().trim();
  return content.split("\n").map(line => parseInt(line.trim()));
};

const partOne = async () => {
  const masses = await getMasses();
  const fuelCounts = masses.map(massToFuel);

  console.log("Part 1 answer", _.sum(fuelCounts));
};

const partTwo = async () => {
  const masses = await getMasses();
  const fuelCounts = masses.map(getRecursiveFuel);

  console.log("Part 2 answer", _.sum(fuelCounts));
};

const main = async () => {
  console.log(getRecursiveFuel(100756));
  await partOne();
  await partTwo();
};

main();
