import { promises as fs } from "fs";
import _ from 'lodash';

const main = async () => {
  const fileHandle = await fs.open("1/input.txt", "r");
  const contentBuffer = await fileHandle.readFile();
  const content = contentBuffer.toString().trim();
  const masses = content.split("\n").map(line => parseInt(line.trim()));
  console.log(masses);

  const fuelCounts = masses.map((mass) => {
      return Math.floor(mass / 3) - 2
  })

  console.log(_.sum(fuelCounts))
};

main();
