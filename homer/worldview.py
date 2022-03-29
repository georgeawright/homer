class Worldview:
    def __init__(self):
        self.view = None
        self.satisfaction = 0


# worldview setter finds a complete view and sets as worldview
# worldview satisfaction depends on quality, how much of original input space it covers, number of frames used, number of frame types used
# quality * (proportion_of_input / no_of_frames/frame_types)?
# future worldview setters find a new complete view and replace worldview if it is better wrt above metric

# publisher codelet has high chance of publishing high quality worldview
# publisher more likely to publish when satisfaction is high and focus is low
