import numpy as np
import pandas as pd
from bokeh.palettes import Category20


class DataAnalyser:
    def __init__(self):
        self.data = self.read_data()

    def read_data(self):
        # TODO: Check if the directory and the data exists
        # Reading all the files
        data = pd.read_csv(
            "data/2000.csv", sep=";", parse_dates=["DATA_HORA"], error_bad_lines=False
        )
        for year in range(2001, 2016 + 1):
            data_to_append = pd.read_csv(
                "data/" + str(year) + ".csv",
                sep=";",
                parse_dates=["DATA_HORA"],
                error_bad_lines=False,
            )
            data = data.append(data_to_append, ignore_index=True, sort=False)
            # Converting date column
            data["DATA_HORA"] = pd.to_datetime(data["DATA_HORA"], errors="coerce")
        return data

    def get_accidents_by_year(self, severity=None):
        if severity == None:
            accidents_by_year = self.data.groupby(self.data["DATA_HORA"].dt.year).size()
        else:
            accidents_by_year = (
                self.data[self.data["UPS"] == severity]
                .groupby(self.data["DATA_HORA"].dt.year)
                .size()
            )
        return accidents_by_year

    def get_accidents_by_day(self, severity=None):
        days_english = np.array(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        days_portuguese = np.array(
            [
                "DOMINGO",
                "SEGUNDA-FEIRA",
                "TERCA-FEIRA",
                "QUARTA-FEIRA",
                "QUINTA-FEIRA",
                "SEXTA-FEIRA",
                "SABADO",
            ]
        )

        if severity == None:
            accidents_by_day = self.data.groupby(self.data["DIA_SEM"]).size()
        else:
            accidents_filtered_by_severity = self.data[self.data["UPS"] == severity]
            accidents_by_day = accidents_filtered_by_severity.groupby(
                self.data["DIA_SEM"]
            ).size()

        for index in accidents_by_day.index:
            if index not in days_portuguese:
                accidents_by_day = accidents_by_day.drop(index)
        accidents_by_day = accidents_by_day.loc[days_portuguese]
        accidents_by_day.index = days_english

        return accidents_by_day

    def get_accidents_by_hour_each_year(self, starting_year=2000, ending_year=2016):
        data_by_year = self.data.groupby(self.data["DATA_HORA"].dt.year)
        accidents_by_year = dict(quantity=[], hour=[], year=[], color=[])
        hours = [i for i in range(0, 24)]
        for index, group in enumerate(data_by_year):
            accidents_by_year["quantity"].append(
                group[1].groupby(group[1]["DATA_HORA"].dt.hour).size()
            )
            accidents_by_year["hour"].append(hours)
            accidents_by_year["year"].append(int(group[0]))
            accidents_by_year["color"].append(Category20[20][index])

        return accidents_by_year

    def get_accidents_by_time_each_day(self, year=2016, severity=5):
        days_english = np.array(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        days_portuguese = np.array(
            [
                "DOMINGO",
                "SEGUNDA-FEIRA",
                "TERCA-FEIRA",
                "QUARTA-FEIRA",
                "QUINTA-FEIRA",
                "SEXTA-FEIRA",
                "SABADO",
            ]
        )

        day_translations = pd.DataFrame(
            data={"DAY_PORTUGUESE": days_portuguese, "DAY_ENGLISH": days_english}
        )

        accidents_by_year = self.data[self.data["DATA_HORA"].dt.year == 2016]
        accidents_by_severity = accidents_by_year[accidents_by_year["UPS"] == severity]
        accidents_by_time = pd.merge(
            accidents_by_severity,
            day_translations,
            left_on="DIA_SEM",
            right_on="DAY_PORTUGUESE",
        )
        accidents_by_time["DATA_HORA"] = accidents_by_time["DATA_HORA"].dt.time

        return accidents_by_time
