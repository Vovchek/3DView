import sys
import Part
import Mesh
import MeshPart

step_path = sys.argv[2]
stl_path = sys.argv[3]

print(f"[INFO] Reading STEP file: {step_path}")
shape = Part.read(step_path)

print("[INFO] Meshing shape...")
mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.523599, Relative=False)

print("[INFO] Writing STL file...")
mesh.write(stl_path)

print(f"[SUCCESS] STL exported to: {stl_path}")
