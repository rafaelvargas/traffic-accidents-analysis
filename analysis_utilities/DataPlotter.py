from bokeh.plotting import figure, output_file, save
from bokeh.embed import components
from bokeh.transform import jitter
from bokeh.palettes import Category20
import numpy as np
import os


class DataPlotter:
    def __init__(self):
        self.output_directory = "plots"
        self.aspect_ratio = 16 / 9
        self.xaxis_label_rotation = (120 / 360) * np.pi
        self.plots = {}

        self.make_output_directory()

    def make_output_directory(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def plot_accidents_by_year(self, data, output_filename):
        output_path = "{}/{}.html".format(self.output_directory, output_filename)
        output_file(output_path)

        point_description = [("Year", "@x"), ("Qty.", "@y")]

        p = figure(
            x_axis_label="year",
            toolbar_location=None,
            sizing_mode="stretch_both",
            aspect_ratio=self.aspect_ratio,
            tools="",
            tooltips=point_description,
        )
        p.line(data.index, data.values, line_width=2)
        p.circle(data.index, data.values, size=6)
        p.xaxis.ticker = data.index
        p.xaxis.major_label_orientation = self.xaxis_label_rotation
        p.y_range.start = 0
        p.y_range.range_padding_units = "percent"
        p.y_range.range_padding = 0.35
        self.plots[output_filename] = p
        save(p)

    def plot_accidents_by_day(self, data, output_filename):
        output_path = "{}/{}.html".format(self.output_directory, output_filename)
        output_file(output_path)

        bar_description = [("Day", "@x"), ("Qty.", "@top")]

        p = figure(
            x_axis_label="day",
            x_range=data.index.tolist(),
            toolbar_location=None,
            sizing_mode="stretch_both",
            aspect_ratio=self.aspect_ratio,
            tools="",
            tooltips=bar_description,
        )
        p.vbar(x=data.index, top=data.values, width=0.8)
        p.y_range.start = 0

        self.plots[output_filename] = p
        save(p)

    def plot_accidents_by_hour_each_year(self, data, output_filename):
        output_path = "{}/{}.html".format(self.output_directory, output_filename)
        output_file(output_path)

        line_description = [("Year", "@year")]
        p = figure(
            x_axis_label="hour",
            toolbar_location=None,
            sizing_mode="stretch_both",
            aspect_ratio=self.aspect_ratio,
            tools="",
            tooltips=line_description,
        )

        p.multi_line(
            xs="hour",
            ys="quantity",
            line_width=2,
            line_color="color",
            line_alpha=0.6,
            hover_line_color="color",
            hover_line_alpha=1.0,
            source=data,
        )

        p.xaxis.ticker = [i for i in range(0, 24)]
        p.xaxis.major_label_orientation = self.xaxis_label_rotation
        p.y_range.start = 0
        p.x_range.range_padding = 0

        self.plots[output_filename] = p
        save(p)

    def plot_accidents_by_time_each_day(self, data, output_filename):
        output_path = "{}/{}.html".format(self.output_directory, output_filename)
        output_file(output_path)

        days_english = np.array(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        p = figure(
            y_range=days_english.tolist(),
            x_axis_type="datetime",
            x_axis_label="time",
            toolbar_location=None,
            sizing_mode="stretch_both",
            aspect_ratio=self.aspect_ratio,
            tools="",
        )

        p.circle(
            x="DATA_HORA",
            y=jitter("DAY_ENGLISH", width=0.4, range=p.y_range),
            source=data,
            alpha=0.2,
        )

        p.xaxis[0].formatter.days = ["%Hh"]
        p.x_range.range_padding = 0
        p.ygrid.grid_line_color = None

        self.plots[output_filename] = p
        save(p)

    def save_plots_elements(self):
        script, divs = components(self.plots)
        with open(
            "{}/plots_loader_script.js".format(self.output_directory), "w"
        ) as script_file:
            script_file.write(script)
        for key, div in divs.items():
            with open("{}/{}.js".format(self.output_directory, key), "w") as div_file:
                div_file.write(div)
