// Each of these files is a set of points in two-dimensional space. For each file, determine the distance between the closest two points in the set (using standard Euclidean distance).

// The first few can theoretically be done by hand, but you will probably want to write code for the later questions. Each answer should be given rounded to three decimal digits.

// For example, for the input {{3.46204, 6.64694}, {0.634868, 3.93809}, {6.65893, 7.41089}, {0.286643, 7.59746}, {8.77236, 4.80401}} would result in the answer 3.287.

const array = [5, 6, 7, 1, 5, 12, 2, 8, 4, 2, 4, 7, 1, 8];

import { promises as fs } from "fs";
import path, { dirname } from "path";

function parseStringToCoordinates(string: string) {
    const pairs = string.slice(2, -2).split("}, {");
    const coords = pairs.map((pair) => {
        const [x, y] = pair.split(", ");
        return { x: parseFloat(x), y: parseFloat(y) };
    });
    return coords;
}

async function parseFile(fileName: string) {
    const data = await fs.readFile(path.resolve(__dirname, `./files/${fileName}`), "binary");
    return Buffer.from(data);
}

type ICoordinates = { x: number; y: number };

function findMinAmongThree(coordinates: ICoordinates[]) {
    const aToB = calcEuclideanDistance(coordinates[0], coordinates[1]);
    const bToC = calcEuclideanDistance(coordinates[1], coordinates[2]);
    const cToA = calcEuclideanDistance(coordinates[2], coordinates[0]);

    console.log("FindMinAmongThree: ", aToB, bToC, cToA);
    return Math.min(aToB, bToC, cToA);
}
function calculateClosestPoints(coordinates: ICoordinates[], coordsByY: ICoordinates[]) {
    // Base Case

    // if (coordinates.length === 0) throw new Error("Coordinates had a length of 0");
    if (coordinates.length == 2) return calcEuclideanDistance(coordinates[0], coordinates[1]);
    if (coordinates.length <= 3) return findMinAmongThree(coordinates);

    // Divide and conquer
    const middlePoint = Math.floor(coordinates.length / 2);
    const m1 = calculateClosestPoints(coordinates.slice(0, middlePoint), coordsByY); // returns 2
    const m2 = calculateClosestPoints(
        coordinates.slice(middlePoint, coordinates.length),
        coordsByY
    ); // returns 3

    const d = Math.min(m1, m2);

    // Now we got to check if there are any coords actually less than d distance.
    //

    const strip = [];
    for (let i = 0; i < coordsByY.length; i++) {
        if (Math.abs(coordsByY[i].x - coordsByY[middlePoint].x) < d) {
            strip.push(coordsByY[i]);
        }
    }

    return Math.min(d, stripClosest(strip, strip.length, d));
}

function stripClosest(strip: ICoordinates[], size: number, d: number) {
    let min = d; // Initialize the minimum distance as d

    strip.sort((a, b) => a.y - b.y);

    // Pick all points one by one and try the next points till the difference
    // between y coordinates is smaller than d.
    for (let i = 0; i < size; ++i)
        for (let j = i + 1; j < size && strip[j].y - strip[i].y < min; ++j) {
            const dist = calcEuclideanDistance(strip[i], strip[j]);
            if (dist < min) min = dist;
        }
    return min;
}

function quickSort(coordinates: ICoordinates[], sortBy: "x" | "y"): ICoordinates[] {
    const pivot = coordinates[0];
    if (coordinates.length <= 1) return coordinates;
    const leftCoords = [];
    const rightCoords = [];
    for (let i = 1; i < coordinates.length; i++) {
        if (coordinates[i][sortBy] < pivot[sortBy]) {
            leftCoords.push(coordinates[i]);
        } else if (coordinates[i][sortBy] > pivot[sortBy]) {
            rightCoords.push(coordinates[i]);
        }
    }

    return [...quickSort(leftCoords, sortBy), pivot, ...quickSort(rightCoords, sortBy)];
}
function calcEuclideanDistance(one: ICoordinates, two: ICoordinates) {
    const { x: x1, y: y1 } = one;
    const { x: x2, y: y2 } = two;

    return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
... (13 lines left)