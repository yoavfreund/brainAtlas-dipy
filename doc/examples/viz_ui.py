import numpy as np

from dipy.data import read_viz_icons

# Conditional import machinery for vtk.
from dipy.utils.optpkg import optional_package

# Allow import, but disable doctests if we don't have vtk.
from dipy.viz import ui, window
from dipy.viz.ui import Button2D

vtk, have_vtk, setup_module = optional_package('vtk')

if have_vtk:
    vtkInteractorStyleUser = vtk.vtkInteractorStyleUser
    version = vtk.vtkVersion.GetVTKSourceVersion().split(' ')[-1]
    major_version = vtk.vtkVersion.GetVTKMajorVersion()
else:
    vtkInteractorStyleUser = object

numpy_support, have_ns, _ = optional_package('vtk.util.numpy_support')


# Cube Actors
def cube_maker(color=None, size=(0.2, 0.2, 0.2), center=None):
    cube = vtk.vtkCubeSource()
    cube.SetXLength(size[0])
    cube.SetYLength(size[1])
    cube.SetZLength(size[2])
    if center is not None:
        cube.SetCenter(*center)
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(cube.GetOutputPort())
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    if color is not None:
        cube_actor.GetProperty().SetColor(color)
    return cube_actor

cube_actor_1 = cube_maker((1, 0, 0), (50, 50, 50), center=(0, 0, 0))
cube_actor_2 = cube_maker((0, 1, 0), (10, 10, 10), center=(100, 0, 0))
# /Cube Actors

# Buttons
icon_files = dict()
icon_files['stop'] = read_viz_icons(fname='stop2.png')
icon_files['play'] = read_viz_icons(fname='play3.png')
icon_files['plus'] = read_viz_icons(fname='plus.png')
icon_files['cross'] = read_viz_icons(fname='cross.png')

button_example = ui.Button2D(icon_fnames=icon_files)


def left_mouse_button_drag(i_ren):
    print("Left Button Dragged")


def left_mouse_button_click(i_ren):
    print ("Left Button Clicked")

button_example.on_left_mouse_button_drag = left_mouse_button_drag
button_example.on_left_mouse_button_pressed = left_mouse_button_click


def right_mouse_button_drag(i_ren):
    print("Right Button Dragged")


def right_mouse_button_click(i_ren):
    print ("Right Button Clicked")

button_example.on_right_mouse_button_drag = right_mouse_button_drag
button_example.on_right_mouse_button_pressed = right_mouse_button_click


def hover(i_ren):
    print ("Hovered")

button_example.on_mouse_hover = hover

# def move_button_callback(i_ren, obj, button):
#     # i_ren: CustomInteractorStyle
#     # obj: vtkActor picked
#     # button: Button2D
#     pos_1 = np.array(cube_actor_1.GetPosition())
#     pos_1[0] += 2
#     cube_actor_1.SetPosition(tuple(pos_1))
#     pos_2 = np.array(cube_actor_2.GetPosition())
#     pos_2[1] += 2
#     cube_actor_2.SetPosition(tuple(pos_2))
#     i_ren.force_render()
#
#
# def modify_button_callback(i_ren, obj, button):
#     # i_ren: CustomInteractorStyle
#     # obj: vtkActor picked
#     # button: Button2D
#     button.next_icon()
#     i_ren.force_render()

# button_example.on_left_mouse_button_click(modify_button_callback)

# button_example.add_callback("RightButtonPressEvent", move_button_callback)
# button_example.add_callback("LeftButtonPressEvent", modify_button_callback)
# /Buttons


# Panel
panel = ui.Panel2D(center=(440, 90), size=(300, 150), color=(1, 1, 1), align="right")
panel.add_element(button_example, (0.2, 0.2))

# /Panel

# Show Manager
current_size = (600, 600)
show_manager = window.ShowManager(size=current_size, title="DIPY UI Example")

show_manager.ren.add(cube_actor_1)
show_manager.ren.add(cube_actor_2)
show_manager.ren.add(panel)

show_manager.start()
