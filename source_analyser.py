from nodes import *
from file_readers import *
from file_writers import *
from sys import platform

file_prefix = ""
if platform != "win32" or platform != "win64":
    file_prefix += "../"


class SourceAnalyser:
    def __init__(self, sources) -> None:
        # list of sources to analyse
        self.sources = sources

    def analyse(self, root):
        total_records = 0
        readers = []
        analysis_header = ""

        with open(file_prefix + "analysis/analysis.csv", "a") as file:

            # add data from sources to file
            for source in self.sources:
                data_source = (
                    source.strip("data/")
                    .strip("-data.csv")
                    .strip("-data/out")
                    .strip("NEW-")
                )
                analysis_header += data_source + ", "
                if source == "data/EMDAT-data.csv":
                    readers.append(EMDATFileReader(file_prefix + source, root))
                elif source == "data/IFRC-data.csv":
                    readers.append(IFRCFileReader(file_prefix + source, root))
                elif source == "data/IDMC-data.csv":
                    readers.append(IDMCFileReader(file_prefix + source, root))
                elif source == "data/NEW-DesInventar-data/out":
                    readers.append(DesInventarFileReader(file_prefix + source, root))
                else:
                    print("Source not recognised")
                    return

            analysis_header += "\n"

            file.write(analysis_header)

            # count number of records in each country and total records
            for child in root.countries:
                country_total = 0
                for month in child.children:
                    for year in month.children:
                        for profile in year.children:
                            for cluster in profile.children:
                                for type in cluster.children:
                                    total_records += 1
                                    country_total += 1
                file.write(f"{child.name}, {country_total}\n")
            file.write(f"Total records, {total_records}\n")
            file.write("\n")
