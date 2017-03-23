from panda3d.core import *
loadPrcFileData("", "show-frame-rate-meter  #t")
loadPrcFileData("", "window-title Press SPACE")
from direct.showbase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
import random

def make_lightning(start, end, count=12):
    ray=loader.load_model('ray')
    ray.reparent_to(render)
    ray.set_pos(start)
    ray.look_at(end)
    distance=(end-start).length()
    time=distance/10.0
    ray.set_instance_count(count)
    ray.setShader(Shader.load(Shader.SLGLSL, 'lightning_v.glsl','lightning_f.glsl'))
    ray.set_shader_input('start_time', globalClock.get_frame_time())
    ray.set_shader_input('max_length', distance)
    delete=Func(ray.remove_node)
    Sequence(Wait(time+0.5), delete).start()


class Demo(DirectObject):
    def __init__(self):
        base = ShowBase.ShowBase()

        base.trackball.node().setHpr(0, 40, 0)
        base.trackball.node().setPos(0, 10, 0)

        grid=loader.load_model('grid1')
        grid.reparent_to(render)
        grid.set_scale(0.1)

        self.accept('space', self.run)

    def run(self):
        target=Vec3(random.uniform(-5, 5), random.uniform(-5, 5), 0.0)
        make_lightning(Vec3(0,0,0.5), target, count=random.randint(3, 7))

    def turn(self, task):
        dt = globalClock.getDt()
        self.ray.set_h(self.ray, 15.0*dt)
        return task.cont

    def set_slider_input(self):
        v=float(self.slider['value'])
        render.set_shader_input('length', v)

d=Demo()
base.run()
