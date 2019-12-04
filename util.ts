export const range = (n: number): number[] => {
  // @ts-ignore
  return Array.from([...Array(n).keys()]);
};

export const rangeBetween = (from: number, to: number) => {
  const firstRange = range(to - from);
  return firstRange.map(num => num + from);
};
