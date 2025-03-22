import FreeCAD as App
import Part
import Draft

# Constants for the floor plan (all measurements in millimeters)
WALL_HEIGHT = 2700  # 2.7 meters
WALL_THICKNESS = 200  # 20 cm
DOOR_WIDTH = 900  # 90 cm
DOOR_HEIGHT = 2100  # 2.1 meters

# Main floor dimensions
FLOOR_WIDTH = 12000  # 12 meters
FLOOR_LENGTH = 10000  # 10 meters

def create_wall(length, height, thickness, placement):
    wall = Part.makeBox(length, thickness, height, placement)
    return wall

def create_floor():
    doc = App.newDocument("FloorPlan")
    
    # Create the main floor slab
    floor_slab = Part.makeBox(FLOOR_WIDTH, FLOOR_LENGTH, 200)  # 20cm thick floor
    floor = doc.addObject("Part::Feature", "FloorSlab")
    floor.Shape = floor_slab
    
    # Create exterior walls
    walls = []
    # Front wall
    walls.append(create_wall(FLOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS, 
                           App.Vector(0, 0, 200)))
    # Back wall
    walls.append(create_wall(FLOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS, 
                           App.Vector(0, FLOOR_LENGTH - WALL_THICKNESS, 200)))
    # Left wall
    walls.append(create_wall(WALL_THICKNESS, FLOOR_LENGTH, WALL_HEIGHT, 
                           App.Vector(0, 0, 200)))
    # Right wall
    walls.append(create_wall(WALL_THICKNESS, FLOOR_LENGTH, WALL_HEIGHT, 
                           App.Vector(FLOOR_WIDTH - WALL_THICKNESS, 0, 200)))
    
    # Interior walls
    # Central corridor wall (horizontal)
    walls.append(create_wall(FLOOR_WIDTH, WALL_HEIGHT, WALL_THICKNESS,
                           App.Vector(0, FLOOR_LENGTH/2 - WALL_THICKNESS/2, 200)))
    
    # Vertical dividing walls
    div_positions = [FLOOR_WIDTH/3, 2*FLOOR_WIDTH/3]  # Divide into 3 sections
    for x in div_positions:
        # Upper section wall
        walls.append(create_wall(WALL_THICKNESS, FLOOR_LENGTH/2, WALL_HEIGHT,
                               App.Vector(x - WALL_THICKNESS/2, FLOOR_LENGTH/2, 200)))
        # Lower section wall
        walls.append(create_wall(WALL_THICKNESS, FLOOR_LENGTH/2 - WALL_THICKNESS, WALL_HEIGHT,
                               App.Vector(x - WALL_THICKNESS/2, 0, 200)))

    # Bathroom and toilet dividing wall
    bathroom_wall = create_wall(WALL_THICKNESS, FLOOR_LENGTH/4, WALL_HEIGHT,
                              App.Vector(5*FLOOR_WIDTH/6, 0, 200))
    walls.append(bathroom_wall)
    
    # Combine all walls
    wall_compound = Part.makeCompound(walls)
    walls_obj = doc.addObject("Part::Feature", "Walls")
    walls_obj.Shape = wall_compound
    
    # Add labels for rooms
    room_labels = [
        ("Room1", App.Vector(FLOOR_WIDTH/6, 3*FLOOR_LENGTH/4, 0)),
        ("Room2", App.Vector(FLOOR_WIDTH/2, 3*FLOOR_LENGTH/4, 0)),
        ("Room3", App.Vector(5*FLOOR_WIDTH/6, 3*FLOOR_LENGTH/4, 0)),
        ("Room4", App.Vector(FLOOR_WIDTH/6, FLOOR_LENGTH/4, 0)),
        ("Bathroom", App.Vector(2*FLOOR_WIDTH/3 + WALL_THICKNESS, FLOOR_LENGTH/4, 0)),
        ("Toilet", App.Vector(5*FLOOR_WIDTH/6 + WALL_THICKNESS, FLOOR_LENGTH/8, 0))
    ]
    
    for label, pos in room_labels:
        text = Draft.make_text([label], pos)
        text.ViewObject.FontSize = 200  # Make text visible
    
    doc.recompute()
    
    # Set the view
    doc.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0))
    
    return doc

if __name__ == "__main__":
    doc = create_floor()
    doc.saveAs("floor_plan.FCStd") 