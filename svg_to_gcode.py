import svg_to_gcode


# Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
# how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
gcode_compiler = svg_to_gcode.Compiler(svg_to_gcode.interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=0)

curves = parse_file("zmenit_combinace.svg")

gcode_compiler.append_curves(curves)
gcode_compiler.compile_to_file("drawing.gcode", passes=2)