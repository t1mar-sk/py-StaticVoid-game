import pyglet

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1000, height=800, caption="2.5D Pyglet Engine", resizable=True)
        self.batch = pyglet.graphics.Batch()

    def update(self, dt):
        pass

if __name__ == "__main__":
    window = GameWindow()

    pyglet.clock.schedule_interval(window.update, 1 / 60.0) #60 FPS

    pyglet.app.run()