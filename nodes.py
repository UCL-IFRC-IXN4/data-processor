from abc import abstractmethod, ABC


months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


class ParentNode(ABC):
    def __init__(self, name):
        self.children = set()
        self.name = name

    @abstractmethod
    def create_child_node_instance(self, child_name):
        pass

    def add_child(self, child):
        self.children.add(child)


class DataNode(ABC):
    def __init__(self, name):
        self.data = [None] * 4  # [IFRC, IDMC, EMDAT, DI]
        self.name = name

    @abstractmethod
    def add_data(self, deaths, effected, index):
        pass


class RootNode:
    def __init__(self):
        self.countries = set()

    def create_child_node_instance(self, country_name):
        for country in self.countries:
            if country.name == country_name:
                return country
        else:
            node = CountryNode(country_name)
            self.countries.add(node)
            return node


class CountryNode(ParentNode):
    def create_child_node_instance(self, month=1):
        if month.isdigit():
            # 0 : Jan
            # 11 : Dec
            month = months[int(month) % 12 - 1]

        for child in self.children:
            if child.name == month:
                return child
        else:
            node = MonthNode(month)
            self.add_child(node)
            return node


class MonthNode(ParentNode):
    def create_child_node_instance(self, year):
        for child in self.children:
            if child.name == year:
                return child
        else:
            node = YearNode(year)
            self.add_child(node)
            return node


class YearNode(ParentNode):
    def create_child_node_instance(self, profile):
        for child in self.children:
            if child.name == profile:
                return child
        else:
            node = ProfileNode(profile)
            self.add_child(node)
            return node


class ProfileNode(ParentNode):
    # e.g. METRO. AND HYDRO.
    def create_child_node_instance(self, cluster):
        for child in self.children:
            if child.name == cluster:
                return child
        else:
            node = ClusterNode(cluster)
            self.add_child(node)
            return node


class ClusterNode(ParentNode):
    # e.g. Precipitation
    def create_child_node_instance(self, type):
        for child in self.children:
            if child.name == type:
                return child
        else:
            node = TypeNode(type)
            self.add_child(node)
            return node


class TypeNode(DataNode):
    # e.g. Torrential Rains
    def __init__(self, name):
        self.data = [None] * 4  # [IFRC, IDMC, EMDAT, DI]
        self.count = 0
        self.name = name

    def add_data(self, deaths, effected, index):
        self.count += 1
        if deaths is not None:
            deaths = int(deaths)
        if effected is not None:
            effected = int(effected)

        if self.data[index] is None:
            self.data[index] = [deaths, effected]
        else:
            if deaths is not None:
                self.data[index][0] += deaths
            if effected is not None:
                self.data[index][1] += effected
