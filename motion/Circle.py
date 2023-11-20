class Circle:
    def __init__(self, color, center_x, center_y):
        self.color = color
        self.last_center_x = center_x
        self.last_center_y = center_y
        self.coords = [(self.last_center_x, self.last_center_y)]

    def __str__(self):
        return f"Circle(color={self.color}, center_x={self.last_center_x}, center_y={self.last_center_y})"

    def ensure_coords(self, new_coords, threshold=10):
        distance = ((new_coords[0] - self.last_center_x) ** 2 + (new_coords[1] - self.last_center_y) ** 2) ** 0.5
        return distance <= threshold

    def add_coords(self, coords):
        self.last_center_x = coords[0]
        self.last_center_y = coords[1]
        self.coords += [(self.last_center_x, self.last_center_y)]

    def get_x_coords(self):
        return [coord[0] for coord in self.coords]

    def get_y_coords(self):
        return [coord[1] for coord in self.coords]