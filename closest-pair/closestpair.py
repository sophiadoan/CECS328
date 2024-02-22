import math

for i in range(1,11):
    with open(f'{i}.txt','r') as file:
        
        f = file.read()
        c = [' ','{','}']
        for char in c:
            f = f.replace(char,'')
        f = f.split(',')
        f = [eval(item) for item in f]

        points = []
        for i in range(0, len(f),2):
            p = f[i:i+2]
            points.append(p)

    points.sort(key=lambda x:x[0])
    # soet points x values
    def closestPair(points):
        n = len(points)
        # base cases
        if n == 2:
            return math.dist(points[0], points[1])
        if n == 3:
            dist1 = math.dist(points[0], points[1])
            dist2 = math.dist(points[1], points[2])
            dist3 = math.dist(points[0], points[2])
            min_distance = min(dist1, dist2, dist3)
            return min_distance
        
        # divide
        mid = n//2
        left = points[:mid]
        right = points[mid:]
        dL = closestPair(left)
        dR = closestPair(right)
        d = min(dL, dR)

        s = [point for point in points if abs(point[0] - points[mid][0]) < d]
        sorted(s,key=lambda x:x[1])

        for i in range(len(s)):
            for j in range(i + 1, min(i + 8, len(s))):
                dist = math.dist(s[i], s[j])
                d = min(d, dist)
        
        return d
    def main():
        print(closestPair(points))

    main()




    