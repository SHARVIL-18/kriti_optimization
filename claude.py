from typing import Tuple, List

Coordinate = Tuple[int, int]
StellarCrystal = Tuple[Coordinate, int]
VoidMine = Tuple[Coordinate, int]


def construct_containment_field(stellar_crystals: List[StellarCrystal], void_mines: List[VoidMine]) -> List[Coordinate]:
    """
    Constructs a containment field polygon to maximize the net value of the Stellar Crystals.

    Parameters:
    stellar_crystals (List[StellarCrystal]): List of (x, y, value) tuples for Stellar Crystals.
    void_mines (List[VoidMine]): List of (x, y, penalty) tuples for Void Mines.

    Returns:
    List[Coordinate]: List of (x, y) coordinates defining the vertices of the containment field polygon.
    """
    # Sort Stellar Crystals in descending order of value
    stellar_crystals.sort(key=lambda x: x[1], reverse=True)

    polygon = []
    total_value = 0
    total_penalty = 0

    for crystal in stellar_crystals:
        x, y, value = crystal

        # Check if adding the current Stellar Crystal violates constraints
        if len(polygon) + 1 <= 1000 and not self_intersects(polygon + [(x, y)]):
            polygon.append((x, y))
            total_value += value

            # Calculate penalties from nearby Void Mines
            for mine in void_mines:
                mx, my, penalty = mine
                if distance((x, y), (mx, my)) <= 1:
                    total_penalty += penalty

    return polygon


def distance(p1: Coordinate, p2: Coordinate) -> float:
    """Calculate Euclidean distance between two points."""
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def self_intersects(polygon: List[Coordinate]) -> bool:
    """Check if a polygon self-intersects."""
    # Implement a simple line segment intersection algorithm
    # to check for self-intersection in the polygon
    # (omitted for brevity)
    return False

