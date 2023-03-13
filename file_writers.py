class FileWriter:
    def __init__(self, file_path) -> None:
        self.file = file_path

    def write_data(self, root):
        with open(self.file, "w") as file:
            file.write("Country,Year,Month,Profile,Cluster,Type,Data,Frequency\n")
            for child in root.countries:
                for month in child.children:
                    for year in month.children:
                        for profile in year.children:
                            for cluster in profile.children:
                                for type in cluster.children:
                                    empty_source = 0
                                    for source in type.data:
                                        if source is None:
                                            empty_source += 1
                                    if (
                                        empty_source < 4
                                    ):  # for seeing data that appears numerous times
                                        file.write(
                                            f"{child.name}, {year.name}, {month.name}, {profile.name}, {cluster.name}, {type.name}, {type.data}, {type.count}\n"
                                        )
        file.close()
