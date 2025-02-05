class grid:
    def __init__(self, length, width, block_size, points):
        self.width = width
        self.length = length
        self.rows = length // block_size
        self.cols = width // block_size
        self.pts = points

        self.vals = [[0 for st in range(self.cols)] for en in range(self.rows)]
        for point in points:
            cp = point[0] // block_size
            rp = point[1] // block_size
            self.vals[rp][cp] += point[2]
        self.blocks = set()
        # add all the boundary points
        for i in range(self.rows):
            self.blocks.add(self.block(i, 0, self.vals[i][0]))
            self.blocks.add(self.block(i, self.cols - 1, self.vals[i][self.cols - 1]))
        for i in range(self.cols):
            self.blocks.add(self.block(0, i, self.vals[0][i]))
            self.blocks.add(self.block(self.rows - 1, i, self.vals[self.rows - 1][i]))

    class block:
        def __init__(self, r, c, value):
            self.r = r
            self.c = c
            self.value = value

        # comparator
        def __lt__(self, other):
            return self.value < other.value

    class polygon:
        def __init__(self, init_score, block_size, length, width):
            self.score = init_score
            self.block_size = block_size
            self.rows = length // block_size
            self.cols = width // block_size
            self.points = set()
            self.points.add((0, 0))
            self.points.add((0, self.cols - 1))
            self.points.add((self.rows - 1, 0))
            self.points.add((self.rows - 1, self.cols - 1))

        def edges(self):
            return len(self.points)

        def is_point_in_polygon(self, point, epsilon=0):
            """
            Ray-casting algorithm to determine if a point is inside a polygon.
            Converts set of points to a sorted list to ensure consistent ordering.
            """
            print(self.points) # print the points

            x, y = point
            # Convert set to a sorted list to get a consistent order
            sorted_points = sorted(list(self.points), key=lambda p: (p[0], p[1]))
            n = len(sorted_points)
            inside = False
            if (x, y) in self.points:
                return True
            for i in range(n):
                p1x, p1y = sorted_points[i]
                p2x, p2y = sorted_points[(i + 1) % n]

                # Check if point is within the vertical range of the edge
                if min(p1y, p2y) - epsilon <= y <= max(p1y, p2y) + epsilon:
                    # Check if point is to the left of the edge
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if abs(p1x - p2x) > epsilon:
                            if x <= xinters + epsilon:
                                inside = not inside
                        else:
                            # Vertical edge case
                            if abs(x - p1x) <= epsilon:
                                inside = not inside
            print(point, inside)
            return inside

        def check_block_in_polygon(self, blk):
            """
            Check if a block is inside the polygon.
            Checks multiple points to ensure thorough coverage.
            """
            x = blk.r * self.block_size
            y = blk.c * self.block_size

            # Check more points for more accurate detection
            block_points = [
                (x, y),  # top-left
                (x + self.block_size, y),  # top-right
                (x, y - self.block_size),  # bottom-left
                (x + self.block_size, y - self.block_size),  # bottom-right
                (x + self.block_size / 2, y),  # top-center
                (x + self.block_size / 2, y - self.block_size),  # bottom-center
                (x, y - self.block_size / 2),  # left-center
                (x + self.block_size, y - self.block_size / 2)  # right-center
            ]

            # You can adjust the condition based on your specific requirements
            return all(self.is_point_in_polygon(point) for point in block_points)

        def count_neighbouring_blocks(self, blk):
            count = 0
            if blk.r - 1 >= 0 and self.check_block_in_polygon(
                    grid.block(blk.r - 1, blk.c, grid.vals[blk.r - 1][blk.c])):
                count += 1
            if blk.c - 1 >= 0 and self.check_block_in_polygon(
                    grid.block(blk.r, blk.c - 1, grid.vals[blk.r][blk.c - 1])):
                count += 1
            if blk.c + 2 < self.cols and self.check_block_in_polygon(
                    grid.block(blk.r, blk.c + 2, grid.vals[blk.r][blk.c + 2])):
                count += 1
            if blk.r + 1 < self.rows and self.check_block_in_polygon(
                    grid.block(blk.r + 1, blk.c, grid.vals[blk.r + 1][blk.c])):
                count += 1
            return count

        def check_can_be_removed(self, blk):
            if blk.r - 1 >= 0 and self.check_block_in_polygon(grid.block(blk.r - 1, blk.c, grid.vals[blk.r - 1][blk.c])) and self.count_neighbouring_blocks(
                    grid.block(blk.r - 1, blk.c, grid.vals[blk.r - 1][blk.c])) <= 1:
                return False
            if blk.c - 1 >= 0 and self.check_block_in_polygon(grid.block(blk.r, blk.c - 1, grid.vals[blk.r][blk.c - 1])) and self.count_neighbouring_blocks(
                    grid.block(blk.r, blk.c - 1, grid.vals[blk.r][blk.c - 1])) <= 1:
                return False
            if blk.c + 2 < self.cols and self.check_block_in_polygon(grid.block(blk.r, blk.c + 2, grid.vals[blk.r][blk.c + 2])) and self.count_neighbouring_blocks(
                    grid.block(blk.r, blk.c + 2, grid.vals[blk.r][blk.c + 2])) <= 1:
                return False
            if blk.r + 1 < self.rows and self.check_block_in_polygon(grid.block(blk.r + 1, blk.c, grid.vals[blk.r + 1][blk.c])) and self.count_neighbouring_blocks(
                    grid.block(blk.r + 1, blk.c, grid.vals[blk.r + 1][blk.c])) <= 1:
                return False
            return True

        def remove_block(self, blk):
            if self.check_block_in_polygon(blk) == False:
                print(f"block not in polygon {blk.r}, {blk.c}")
                return 0
            if not self.check_can_be_removed(blk):
                return 0
            self.score -= blk.value
            x = blk.c * self.block_size
            y = blk.r * self.block_size
            if x < self.block_size or y + self.block_size >= self.cols * self.block_size:
                return 0
            new_blocks = []
            cnt = 0
            if blk.r - 1 >= 0 and (grid.vals[blk.r - 1][blk.c] <= 0):
                new_blocks.append(grid.block(blk.r - 1, blk.c, grid.vals[blk.r - 1][blk.c]))
                print(f"Adding block at {blk.r - 1}, {blk.c}")
            if blk.c - 1 >= 0 and (grid.vals[blk.r][blk.c - 1] <= 0):
                new_blocks.append(grid.block(blk.r, blk.c - 1, grid.vals[blk.r][blk.c - 1]))
                print(f"Adding block at {blk.r}, {blk.c - 1}")
            if blk.c + 2 < self.cols and grid.vals[blk.r][blk.c + 2] <= 0:
                new_blocks.append(grid.block(blk.r, blk.c + 2, grid.vals[blk.r][blk.c + 2]))
                print(f"Adding block at {blk.r}, {blk.c + 2}")
            if blk.r + 1 < self.rows and grid.vals[blk.r + 1][blk.c] <= 0:
                new_blocks.append(grid.block(blk.r + 1, blk.c, grid.vals[blk.r + 1][blk.c]))
                print(f"Adding block at {blk.r + 1}, {blk.c}")
            for to_add in new_blocks:
                print(to_add.r, to_add.c, self.count_neighbouring_blocks(to_add))

            print(f"Removing block at {blk.r}, {blk.c}")
            new_points = [(x, y), (x - self.block_size, y), (x, y + self.block_size),
                          (x - self.block_size, y + self.block_size)]
            exist = []
            for point in new_points:
                if point in self.points:
                    exist.append(-1)
                else:
                    exist.append(1)
            if self.edges() + sum(exist) > 1000:
                return 0
            idx = 0
            print(new_points)
            for point in new_points:
                if point in self.points:
                    self.points.remove(point)
                else:
                    self.points.add(point)
                idx += 1

            for to_add in new_blocks:
                if self.check_block_in_polygon(to_add) and self.count_neighbouring_blocks(to_add) > 1:
                    cnt += 1
                    grid.blocks.add(to_add)

            print(f"Added {cnt} blocks")

        def plot_status(self):
            initial_x_points = [point[0] for point in grid.pts]
            initial_y_points = [point[1] for point in grid.pts]
            initial_values = [point[2] for point in grid.pts]

            # Plot initial input points
            plt.scatter(initial_x_points, initial_y_points, c="b", cmap='viridis', marker='o',
                        label='Initial Input Points')

            # Plot final polygon points
            final_polygon_points = list(polygon.points)
            final_polygon_points.append(final_polygon_points[0])  # Close the polygon
            final_polygon_x = [point[0] for point in final_polygon_points]
            final_polygon_y = [point[1] for point in final_polygon_points]
            plt.scatter(final_polygon_x, final_polygon_y, c="r", cmap='viridis', marker='x',
                        label='Final Polygon Points')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Initial Input Points and Final Polygon Points')
            plt.legend()
            plt.colorbar(label='Score Value')
            plt.show()


points = []
max_score = 0
# open input file
with open('input1.txt', 'r') as file:
    # read input file
    lines = file.readlines()
    # parse input
    for i in range(1, len(lines)):
        x, y, value = map(int, lines[i].split())
        temp = [x, y, value]
        points.append(temp)
        max_score += value

length = 8
width = 8
block_size = 1  # block size is 1000
grid = grid(length, width, block_size, points)
polygon = grid.polygon(max_score, block_size, length, width)
print(max_score)
import matplotlib.pyplot as plt

# create a set of the class grid.blocks
polygon.plot_status()
while (1):
    if len(grid.blocks) == 0:
        break
    block = min(grid.blocks)
    prev = len(grid.blocks)
    if block.value <= 0:
        grid.blocks.remove(block)
        polygon.remove_block(block)

        print(f"current blocks {len(grid.blocks)}")
        polygon.plot_status()
        print(polygon.score)
    else:
        break

import matplotlib.pyplot as plt

# Plot the initial input points and the final polygon points
initial_x_points = [point[0] for point in points]
initial_y_points = [point[1] for point in points]
initial_values = [point[2] for point in points]

# Plot initial input points
plt.scatter(initial_x_points, initial_y_points, c="b", cmap='viridis', marker='o', label='Initial Input Points')

# Plot final polygon points
final_polygon_points = list(polygon.points)
final_polygon_points.append(final_polygon_points[0])  # Close the polygon
final_polygon_x = [point[0] for point in final_polygon_points]
final_polygon_y = [point[1] for point in final_polygon_points]
plt.scatter(final_polygon_x, final_polygon_y, c="r", cmap='viridis', marker='x', label='Final Polygon Points')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Initial Input Points and Final Polygon Points')
plt.legend()
plt.colorbar(label='Score Value')
plt.show()
# print(polygon.points)
