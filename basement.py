import FreeCAD
import Part

doc = FreeCAD.newDocument()
box = Part.makeBox(1000, 1000, 3000)
part = doc.addObject("Part::Feature", "Box")
part.Shape = box
doc.recompute()
doc.saveAs("box_model.FCStd")