from nodes import *
from file_readers import *
from file_writers import *
from source_analyser import *
from sys import platform


class Main:
    def __init__(self) -> None:
        self.readers = []
        self.writers = []
        self.sources = [
            "data/EMDAT-data.csv",
            "data/IFRC-data.csv",
            "data/IDMC-data.csv",
            "data/NEW-DesInventar-data/out",
        ]

        self.root = RootNode()
        self.file_prefix = ""
        if platform != "win32" or platform != "win64":
            self.file_prefix += "../"

    def run(self):
        self.readers.append(
            EMDATFileReader(file_prefix + "data/EMDAT-data.csv", self.root)
        )
        self.readers.append(
            IFRCFileReader(file_prefix + "data/IFRC-data.csv", self.root)
        )
        self.readers.append(
            IDMCFileReader(file_prefix + "data/IDMC-data.csv", self.root)
        )
        self.readers.append(
            DesInventarFileReader(
                file_prefix + "data/NEW-DesInventar-data/out", self.root
            )
        )
        self.writers.append(FileWriter(file_prefix + "data/data.csv"))

        for writer in self.writers:
            writer.write_data(self.root)

        self.analyse_sources(self.sources)

    # https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    def powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]

    def analyse_sources(self, sources):
        # clear the data in the info file
        with open(file_prefix + "analysis/analysis.csv", "w") as file:
            pass
        for subset in self.powerset(sources):
            if len(subset) > 0:
                root = RootNode()
                print(subset)
                analysis = SourceAnalyser(subset)
                analysis.analyse(root)


if __name__ == "__main__":
    main = Main()
    main.run()
