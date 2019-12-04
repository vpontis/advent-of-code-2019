import { promises as fs } from "fs";
import _ from "lodash";

type Wire = string[];

const getWires = async (): Promise<[Wire, Wire]> => {
  const fileHandle = await fs.open("3/input.txt", "r");
  const contentBuffer = await fileHandle.readFile();
  const content = contentBuffer.toString().trim();
  const [wire1, wire2] = content.split("\n").map(wire => wire.split(","));
  console.log(wire1.length, wire2.length);
  return [wire1, wire2] as [Wire, Wire];
};

type Point = [number, number];
type WirePath = Point[];

type Direction = "R" | "D" | "L" | "U";
type Command = { direction: Direction; distance: number };

const getCommandsFromWire = (wire: Wire): Command[] => {
  return wire.map(commandString => {
    const [direction, ...rest] = commandString;

    return {
      direction: direction as Direction,
      distance: parseInt(rest.join(""))
    };
  });
};

const range = (n: number): number[] => {
  // @ts-ignore
  return Array.from([...Array(n).keys()]);
};

const getPointsFromCommand = (
  origin: Point,
  command: Command
): { newOrigin: Point; points: WirePath } => {
  const points = [];

  // @ts-ignore
  let newOrigin: Point = origin.slice();

  range(command.distance).forEach(i => {
    switch (command.direction) {
      case "D":
        newOrigin[1] -= 1;
        break;
      case "U":
        newOrigin[1] += 1;
        break;
      case "L":
        newOrigin[0] -= 1;
        break;
      case "R":
        newOrigin[0] += 1;
        break;
    }

    points.push(newOrigin.slice());
  });

  return { points, newOrigin };
};

const getPathFromWire = (wire: Wire): WirePath => {
  const commands = getCommandsFromWire(wire);

  const path: Point[] = [];

  let origin: Point = [0, 0];

  commands.forEach(command => {
    const data = getPointsFromCommand(origin, command);
    const { points }: { points: Point[] } = data;
    path.push(...points);
    origin = data.newOrigin;
  });

  return path;
};

const pointToString = ([x, y]: Point) => `${x},${y}`;
const pointToManhattan = ([x, y]: Point) => Math.abs(x) + Math.abs(y);

const partOne = async () => {
  const wires = await getWires();

  const [path1, path2] = wires.map(getPathFromWire);

  const set1 = new Set(path1.map(pointToString));

  const intersections = path2.filter(point => set1.has(pointToString(point)));

  const smallest = _.minBy(intersections, pointToManhattan);
  console.log(smallest);
  console.log(pointToManhattan(smallest));
};

const partTwo = async () => {};

const main = async () => {
  await partOne();
  // await partTwo();
};

main();
