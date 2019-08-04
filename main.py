from analysis_utilities.DataCollector import DataCollector
from analysis_utilities.DataAnalyser import DataAnalyser
from analysis_utilities.DataPlotter import DataPlotter

if __name__ == "__main__":
    print("Downloading data...")
    data_collector = DataCollector()
    data_collector.collect_accidents_data()

    print("Performing analysis and plotting results...")
    data_analyser = DataAnalyser()
    data_plotter = DataPlotter()

    data_plotter.plot_accidents_by_year(
        data_analyser.get_accidents_by_year(), "accidents-by-year"
    )
    data_plotter.plot_accidents_by_year(
        data_analyser.get_accidents_by_year(severity=13), "fatal-accidents-by-year"
    )
    data_plotter.plot_accidents_by_year(
        data_analyser.get_accidents_by_year(severity=5),
        "accidents-with-injured-by-year",
    )
    data_plotter.plot_accidents_by_day(
        data_analyser.get_accidents_by_day(), "accidents-by-day-of-the-week"
    )
    data_plotter.plot_accidents_by_day(
        data_analyser.get_accidents_by_day(severity=13),
        "fatal-accidents-by-day-of-the-week",
    )
    data_plotter.plot_accidents_by_hour_each_year(
        data_analyser.get_accidents_by_hour_each_year(2000, 2016),
        "accidents-by-hour-each-year",
    )
    data_plotter.plot_accidents_by_time_each_day(
        data_analyser.get_accidents_by_time_each_day(year=2016, severity=5),
        "accidents-by-time-each-day",
    )
    data_plotter.save_plots_elements()
