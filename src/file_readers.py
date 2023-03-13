from abc import abstractmethod, ABC
import os

EMPTIES = [None, 0, "", " ", "  ", "   ", "    ", "     "]

cluster_profile_dictionary = {
    "Environmental Degradation": "Environmental",
    "Environmental Degradation (Forestry)": "Environmental",
    "Other Geohazard": "Geohazards",
    "Geological": "Geohazards",
    "Seismogenic": "Geohazards",
    "Volcanogenic": "Geohazards",
    "Convective-Related": "Meteorological And Hydrological",
    "Flood": "Meteorological And Hydrological",
    "Lithometeors": "Meteorological And Hydrological",
    "Marine": "Meteorological And Hydrological",
    "Precipitation-related": "Meteorological And Hydrological",
    "Temperature-related": "Meteorological And Hydrological",
    "Terrestrial": "Meteorological And Hydrological",
    "Wind-Related": "Meteorological And Hydrological",
    "Behavioural": "Societal",
    "Unrecorded Cluster": "Uncrecorded Profile",
}

hazard_profile_dictionary = {
    "Acid Rain": "Precipitation-related",
    "Avalanche": "Terrestrial",
    "Building Collapse": "Seismogenic",
    "Building Slide": "Seismogenic",
    "Climate Change": "Environmental Degradation",
    "Cloudburst": "Precipitation-related",
    "Coastal Flood": "Flood",
    "Cold Wave": "Temperature-related",
    "Cw - Cold Wave": "Temperature-related",
    "Cyclone": "Wind-Related",
    "Cyclone Wind": "Wind-Related",
    "Déficit Hídrico": "Precipitation-related",
    "Drought": "Precipitation-related",
    "Dr - Drought": "Precipitation-related",
    "Dry Spell": "Precipitation-related",
    "Earth Tremors": "Seismogenic",
    "Earthquake": "Seismogenic",
    "Eq - Earthquake": "Seismogenic",
    "Earthquake and Tsunami": "Seismogenic",
    "Electric Storm": "Convective-Related",
    "Electrique Storm": "Convective-Related",
    "Extreme Temperature": "Temperature-related",
    "Famine": "Precipitation-related",
    "Hambruna": "Precipitation-related",
    "Field Fires": "Environmental Degradation (Forestry)",
    "Fire": "Environmental Degradation (Forestry)",
    "Flash Flood": "Flood",
    "Flash Floods": "Flood",
    "Fash Flood": "Flood",
    "Flood": "Flood",
    "Floods": "Flood",
    "Fl - Flood": "Flood",
    "Inundación": "Flood",
    "Inondation": "Flood",
    "Fog": "Lithometeors",
    "Freezing Rain": "Temperature-related",
    "Gale": "Wind-Related",
    "Glacial Lake Outburst Flood": "Flood",
    "Gonu Cyclone (1 Jun 2007 - Jun 2007)": "Wind-Related",
    "Ground Vibratio": "Seismogenic",
    "Hail": "Precipitation-related",
    "Hailstorm": "Precipitation-related",
    "Hailstorms": "Precipitation-related",
    "Heavy Storm": "Precipitation-related",
    "Heavy Storms": "Precipitation-related",
    "Hippos": "Terrestrial",
    "Hail Strom": "Precipitation-related",
    "Hail Storm": "Precipitation-related",
    "Hailstone": "Precipitation-related",
    "Hail/Hailstone": "Precipitation-related",
    "Heat Wave": "Temperature-related",
    "Heavy Rain": "Precipitation-related",
    "HEAVY RAINS": "Precipitation-related",
    "Heavy Rains2": "Precipitation-related",
    "Strong Rain": "Precipitation-related",
    "pluies extreme": "Precipitation-related",
    "Heavy storm": "Precipitation-related",
    "Strong Storm": "Precipitation-related",
    "Heavy Rain Storm": "Precipitation-related",
    "Heavy Rain with Lightning": "Precipitation-related",
    "Heavy Wind": "Wind-Related",
    "Strong Wind": "Wind-Related",
    "Shark Attack": "Marine",
    "High Wind": "Wind-Related",
    "High Tide": "Marine",
    "High Wave": "Marine",
    "Hurricane": "Convective-Related",
    "Ouragan": "Convective-Related",
    "Lightning": "Convective-Related",
    "Lightening": "Convective-Related",
    "Lighting": "Convective-Related",
    "Foudre": "Convective-Related",
    "Mini Tornado": "Wind-Related",
    "Mudslide": "Seismogenic",
    "Mud Volcano": "Volcanogenic",
    "Ola De Frio": "Temperature-related",
    "Ola De Frío": "Temperature-related",
    "Olaeje": "Marine",
    "Onda Fría": "Temperature-related",
    "Ouragan": "Convective-Related",
    "Pluies Extreme": "Precipitation-related",
    "Pluvial/Flash Flood": "Flood",
    "Rain": "Precipitation-related",
    "Rains": "Precipitation-related",
    "Rain And Strong Wind": "Precipitation-related",
    "Rain Out Of Saison": "Precipitation-related",
    "Rain Storm": "Precipitation-related",
    "Rainstorm": "Precipitation-related",
    "Rainstorms": "Precipitation-related",
    "River Bank Collapse": "Other Geohazard",
    "Raudal": "Precipitation-related",
    "River Flood": "Flood",
    "Riverine Flood": "Flood",
    "Riverineflood": "Flood",
    "Riverinflood": "Flood",
    "Rock + Boulder Slide": "Seismogenic",
    "Rock Collapse": "Seismogenic",
    "Rockslide": "Seismogenic",
    "Sand Storm": "Lithometeors",
    "Sandstorm": "Lithometeors",
    "Snow": "Precipitation-related",
    "Snowfall": "Precipitation-related",
    "Heavy Snow": "Precipitation-related",
    "Riverbank Erosion": "Marine",
    "Rough Seas": "Marine",
    "Seaerosion": "Marine",
    "Severe Colds": "Temperature-related",
    "Severe Winter Condition": "Temperature-related",
    "Snowstorm": "Precipitation-related",
    "Snow Storm": "Precipitation-related",
    "Storm": "Convective-Related",
    "Storm And Heavy Rain": "Precipitation-related",
    "Storm Wind": "Wind-Related",
    "Storm+Gale": "Wind-Related",
    "Storms": "Convective-Related",
    "Stormy": "Convective-Related",
    "Ss - Storm Surge": "Convective-Related",
    "St - Severe Local Storm": "Convective-Related",
    "Stormy Rains": "Precipitation-related",
    "Stormy Rains And Hailstorm": "Precipitation-related",
    "Storm And Heavy Rains": "Precipitation-related",
    "Strong Winds": "Wind-Related",
    "Strong Winds And Bush Fire": "Wind-Related",
    "Strong Winds And Heavy Rain": "Precipitation-related",
    "Strong Winds And Heavy Rains": "Precipitation-related",
    "Strongs Winds And Heavy Rains": "Precipitation-related",
    "Strong Winds+Hailstrom": "Precipitation-related",
    "Strongwind": "Wind-Related",
    "Thunder Lighting Stroke": "Convective-Related",
    "Thunderstorm": "Convective-Related",
    "Tidal Surge": "Marine",
    "Tidal Wave": "Marine",
    "Tidal Waves": "Marine",
    "Tormenta Tropical": "Convective-Related",
    "Tornado": "Wind-Related",
    "Tornadoes": "Wind-Related",
    "Tornados": "Wind-Related",
    "Torrent": "Precipitation-related",
    "Torrential Rain": "Precipitation-related",
    "Torrential Rains": "Precipitation-related",
    "Tremblement De Terre": "Seismogenic",
    "Tormenta": "Convective-Related",
    "Tempête": "Convective-Related",
    "Storm Surge": "Marine",
    "SS - Storm Surge": "Marine",
    "Severe Local Storm": "Precipitation-related",
    "Surge": "Marine",
    "Thunder": "Convective-Related",
    "Thunder Storm": "Convective-Related",
    "Tidal Wave": "Marine",
    "Torrential Rain": "Precipitation-related",
    "Tropical Cyclone": "Wind-Related",
    "Tc - Tropical Cyclone": "Wind-Related",
    "Tsunami": "Marine",
    "Ts - Tsunami": "Marine",
    "Typoon": "Convective-Related",
    "Typhoon": "Convective-Related",
    "Urban Flood": "Flood",
    "Vague De Chaleur": "Temperature-related",
    "Vague De Froid": "Temperature-related",
    "Volcanic Activity": "Volcanogenic",
    "Volcanic Eruption": "Volcanogenic",
    "Volcano": "Volcanogenic",
    "Vo - Volcano": "Volcanogenic",
    "WF - Wild Fires": "Environmental Degradation (Forestry)",
    "Wild Fire": "Environmental Degradation (Forestry)",
    "Wildfire": "Environmental Degradation (Forestry)",
    "Wind Strom": "Wind-Related",
    "Wind Storm": "Wind-Related",
    "Wind": "Wind-Related",
    "Windstorm": "Wind-Related",
    "Windstorm With Heavy Rain": "Wind-Related",
    "Windtorm": "Wind-Related",
    "Winstrom": "Wind-Related",
    "Windstond": "Wind-Related",
    "Windstrom": "Wind-Related",
    "Wndstrom": "Wind-Related",
    "Windstrm": "Wind-Related",
    "Windom Flood": "Flood",
    "Аянга": "Convective-Related",
    "Winter Storm": "Precipitation-related",
    "бичил уурхайн давсны осол": "Behavioural",
    "": "Unrecorded Cluster",
    "Other": "Unrecorded Cluster",
    "Others": "Unrecorded Cluster",
    "Other_Ac": "Unrecorded Cluster",
    "Ot - Other": "Unrecorded Cluster",
    "Otros": "Unrecorded Cluster",
    "Bush Fire": "Environmental Degradation (Forestry)",
    "Cloud Burst": "Precipitation-related",
    "Coastal Erosion": "Marine",
    "Cold": "Temperature-related",
    "Cold Wave": "Temperature-related",
    "Cyclone  And Floods": "Flood",
    "Cyclone And Rainstorm": "Precipitation-related",
    "Cyclones": "Wind-Related",
    "Dry Spells": "Precipitation-related",
    "Earthquake And Tsunami": "Marine",
    "Electricstorm": "Convective-Related",
    "Erosion": "Marine",
    "Falshflood": "Flood",
    "Fash Floods": "Flood",
    "Fire Out Break": "Environmental Degradation (Forestry)",
    "Fire Outbreak": "Environmental Degradation (Forestry)",
    "Flashflood": "Flood",
    "Flooded Stream": "Flood",
    "Flooding": "Flood",
    "Flooding Of Bua River": "Flood",
    "Flsah Flood": "Flood",
    "Forest Fire": "Environmental Degradation (Forestry)",
    "Forest Fire  + Wild Fire": "Environmental Degradation (Forestry)",
    "Forestfire": "Environmental Degradation (Forestry)",
    "Gonu Cyclone": "Wind-Related",
    "Hailstorm And Cyclone": "Wind-Related",
    "Hailstorm And Heavy Rains": "Precipitation-related",
    "Heatwave": "Temperature-related",
    "Heavy Hailstorms And Rains": "Precipitation-related",
    "Heavy Rain With Lightnings": "Convective-Related",
    "Heavy Rains": "Precipitation-related",
    "Heavy Rains2": "Precipitation-related",
    "Heavy Rains And Hailstorm": "Precipitation-related",
    "Heavy Rains And Storm": "Precipitation-related",
    "Heavy Rains And Storms": "Precipitation-related",
    "Heavy Rains And Strong Winds": "Precipitation-related",
    "Heavy Rains And Winds": "Precipitation-related",
    "Heavy Rainstorm": "Precipitation-related",
    "Heavy Winds": "Wind-Related",
    "Heavy Winds And Rain": "Precipitation-related",
    "Heavy Winds And Rains": "Precipitation-related",
    "High Waves": "Marine",
    "High Winds": "Wind-Related",
    "Hunger+Famine": "Precipitation-related",
    "Montagne Wave": "Marine",
    "Landslide": "Geological",
    "Mass Movement (Dry)": "Geological",
    "Mass Movement (Wet)": "Geological",
    "Mass Movement": "Geological",
    "Wet Mass Movement": "Geological",
    "Dry Mass Movement": "Geological",
    "Flash Food": "Flood",
    "Erosión": "Marine",
    "Erossion": "Marine",
    "Eruption": "Volcanogenic",
    "Land Slide": "Geological",
    "Landslide": "Geological",
    "Landslides": "Geological",
    "Land Degradation": "Environmental Degradation",
    "Frost": "Temperature-related",
    "Ls - Landslide": "Geological",
    "Wf - Wild Fires": "Environmental Degradation (Forestry)",
    "Хээрийн Түймэр": "Environmental Degradation (Forestry)",
    "Incendio": "Environmental Degradation (Forestry)",
    "Incendio De Campo": "Environmental Degradation (Forestry)",
    "Incendios Forestales": "Environmental Degradation (Forestry)",
    "Inundación Gradual": "Flood",
    "Inundación Repentina": "Flood",
    "Fissures": "Volcanogenic",
    "Liquefaction": "Seismogenic",
    "Litoral": "Marine",
    "Rock Fall": "Geological",
    "Land Subsidence": "Geological",
    "Rock+Boulder Slide": "Geological",
    "Sedimentation": "Marine",
    "Subsidence": "Geological",
    "Urban + Rural Fire": "Environmental Degradation",
    "Wetland Loss+Degradation": "Environmental Degradation",
    "Spate": "Flood",
}

country_to_iso_dictionary = {
    "Afghanistan": "AFG",
    "Albania": "ALB",
    "Algeria": "DZA",
    "Andorra": "AND",
    "Angola": "AGO",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",
    "Bahamas": "BHS",
    "Bahrain": "BHR",
    "Bangladesh": "BGD",
    "Barbados": "BRB",
    "Belarus": "BLR",
    "Belgium": "BEL",
    "Belize": "BLZ",
    "Benin": "BEN",
    "Bhutan": "BTN",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "Bulgaria": "BGR",
    "Burundi": "BDI",
    "Cambodia": "KHM",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Chad": "TCD",
    "Chile": "CHL",
    "China": "CHN",
    "Colombia": "COL",
    "Columbia": "COL",
    "Comoros": "COM",
    "Congo": "COG",
    "Costa Rica": "CRI",
    "Croatia": "HRV",
    "Cuba": "CUB",
    "Cyprus": "CYP",
    "Denmark": "DNK",
    "Djibouti": "DJI",
    "Dominica": "DMA",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Equatorial Guinea": "GNQ",
    "Eritrea": "ERI",
    "Estonia": "EST",
    "Ethiopia": "ETH",
    "Fiji": "FJI",
    "Finland": "FIN",
    "France": "FRA",
    "Gabon": "GAB",
    "Gambia": "GMB",
    "Georgia": "GEO",
    "Germany": "DEU",
    "Ghana": "GHA",
    "Greece": "GRC",
    "Grenada": "GRD",
    "Guatemala": "GTM",
    "Guinea": "GIN",
    "Guinea-Bissau": "GNB",
    "Guinea Bissau": "GNB",
    "Guyana": "GUY",
    "Haiti": "HTI",
    "Honduras": "HND",
    "Hungary": "HUN",
    "Iceland": "ISL",
    "India": "IND",
    "Indonesia": "IDN",
    "Iraq": "IRQ",
    "Israel": "ISR",
    "Italy": "ITA",
    "Jamaica": "JAM",
    "Japan": "JPN",
    "Jordan": "JOR",
    "Kazakhstan": "KAZ",
    "Kenya": "KEN",
    "Kiribati": "KIR",
    "Kuwait": "KWT",
    "Kyrgyzstan": "KGZ",
    "Latvia": "LVA",
    "Lebanon": "LBN",
    "Lesotho": "LSO",
    "Liberia": "LBR",
    "Libya": "LBY",
    "Liechtenstein": "LIE",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Madagascar": "MDG",
    "Malawi": "MWI",
    "Malaysia": "MYS",
    "Maldives": "MDV",
    "Mali": "MLI",
    "Malta": "MLT",
    "Marshall Islands": "MHL",
    "Mauritania": "MRT",
    "Mauritius": "MUS",
    "Mexico": "MEX",
    "Monaco": "MCO",
    "Mongolia": "MNG",
    "Montenegro": "MNE",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Namibia": "NAM",
    "Nauru": "NRU",
    "Nepal": "NPL",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Nicaragua": "NIC",
    "Niger": "NER",
    "Nigeria": "NGA",
    "Ibadan Metropolis": "NGA",
    "Norway": "NOR",
    "Oman": "OMN",
    "Pakistan": "PAK",
    "Palau": "PLW",
    "Panama": "PAN",
    "Papua New Guinea": "PNG",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Qatar": "QAT",
    "Romania": "ROU",
    "Russian Federation": "RUS",
    "Rwanda": "RWA",
    "Samoa": "WSM",
    "San Marino": "SMR",
    "Saudi Arabia": "SAU",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Seychelles": "SYC",
    "Sierra Leone": "SLE",
    "Singapore": "SGP",
    "Slovakia": "SVK",
    "Slovenia": "SVN",
    "Solomon Islands": "SLB",
    "Somalia": "SOM",
    "South Africa": "ZAF",
    "South Sudan": "SSD",
    "Spain": "ESP",
    "Sri Lanka": "LKA",
    "Palestine": "PSE",
    "Sudan": "SDN",
    "Suriname": "SUR",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Tajikistan": "TJK",
    "Thailand": "THA",
    "Togo": "TGO",
    "Tonga": "TON",
    "Tunisia": "TUN",
    "Turkey": "TUR",
    "Turkmenistan": "TKM",
    "Tuvalu": "TUV",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Vanuatu": "VUT",
    "Yemen": "YEM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE",
    "Antigua & Deps": "ATG",
    "Antigua And Deps": "ATG",
    "Antigua & Barbuda": "ATG",
    "Antigua And Barbuda": "ATG",
    "Bolivia": "BOL",
    "Plurinational State Of Bolivia": "BOL",
    "Bosnia Herzegovina": "BIH",
    "Bosnia and Herzegovina": "BIH",
    "Bosnia & Herzegovina": "BIH",
    "Brunei": "BRN",
    "Brunei Darussalam": "BRN",
    "Burkina": "BFA",
    "Burkina Faso": "BFA",
    "Cape Verde": "CPV",
    "Central African Rep": "CAF",
    "Central African Republic": "CAF",
    "The Central African Republic": "CAF",
    "Congo": "COD",
    "Democratic Republic Of The Congo": "COD",
    "The Democratic Republic Of Congo": "COD",
    "Czech Republic": "CZE",
    "Czechia": "CZE",
    "Timor-Leste": "TLS",
    "Timor Leste": "TLS",
    "East Timor": "TMP",
    "Iran": "IRN",
    "I.R. Iran": "IRN",
    "Islamic Republic Of Iran": "IRN",
    "Ireland": "IRL",
    "Republic Of Ireland": "IRL",
    "Ivory Coast": "CIV",
    "Côte d'Ivoire": "CIV",
    "North Korea": "PRK",
    "Korea North": "PRK",
    "The Democratic People's Republic Of Korea": "PRK",
    "South Korea": "KOR",
    "Korea North": "KOR",
    "The Republic Of Korea": "KOR",
    "Kosovo": "XXK",
    "Laos": "LAO",
    "The Lao People's Democratic Republic": "LAO",
    "Macedonia": "MKD",
    "Republic Of North Macedonia": "MKD",
    "Micronesia": "FSM",
    "Federated States Of Micronesia": "FSM",
    "Moldova": "MDA",
    "The Republic Of Moldova": "MDA",
    "Myanmar": "MMR",
    "Burma": "MMR",
    "St Kitts & Nevis": "KNA",
    "St Kitts And Nevis": "KNA",
    "Saint Kitts & Nevis": "KNA",
    "Saint Kitts And Nevis": "KNA",
    "Saint Lucia": "LCA",
    "Saint Vincent And The Grenadines": "VCT",
    "Saint Vincent & The Grenadines": "VCT",
    "Sao Tome & Principe": "STP",
    "Sao Tome And Principe": "STP",
    "Swaziland": "SWZ",
    "Eswatini": "SWZ",
    "Syria": "SYR",
    "Syrian Arab Republic": "SYR",
    "Taiwan": "TWN",
    "Taiwan (Province of China)": "TWN",
    "Tanzania": "TZA",
    "Tanzania, United Republic Of": "TZA",
    "United Republic Of Tanzania": "TZA",
    "Trinidad and Tobago": "TTO",
    "Trinidad & Tobago": "TTO",
    "Trinidad And Tobago": "TTO",
    "Vatican City": "VAT",
    "Holy See": "VAT",
    "The Holy See": "VAT",
    "Venezuela": "VEN",
    "Bolivarian Republic Of Venezuela": "VEN",
    "Vietnam": "VNM",
    "Viet Nam": "VNM",
    "New Caledonia": "NCL",
    "American Samoa": "ASM",
    "Niue": "NIU",
    "Cook Islands": "COK",
    "Wallis And Futuna": "WLF",
    "Northern Mariana Islands": "MNP",
    "Guam": "GUM",
    "Tokelau": "TKL",
    "French Polynesia": "PYF",
}


profiles_that_appear = set()
clusters_that_appear = set()
hazards_that_appear = set()


class FileReader(ABC):
    def __init__(self, file_path, target):
        self.file_path = file_path
        self.data = self.read_file()
        self.target = target

        self.parse_data()
        self.data = []

    def read_file(self):
        try:
            with open(self.file_path, "r") as file:
                data = file.readlines()
            file.close()
            return data
        except IsADirectoryError:
            pass

    @abstractmethod
    def parse_data(self):
        pass


class IFRCFileReader(FileReader):
    def parse_data(self):
        # country ios3,  end-date, disaster-type name, num-beneficiaries
        hazards_to_be_sorted = set()
        for line in self.data[1:]:
            event = line.split(",")
            """
            country iso3,disaster-type name,start-date,num-beneficiaries
            event[0] iso of country where disaster occurred
            event[1] name of disaster type
            event[2] date of appeal
            event[3] number of beneficiaries (effected???)
            """
            if event[2] not in EMPTIES:
                country = self.target.create_child_node_instance(event[0])
                month = country.create_child_node_instance(event[2].split("/")[1])
                year = month.create_child_node_instance(event[2].split("/")[-1])
                try:
                    cluster_type = hazard_profile_dictionary[
                        event[1].title().strip("\n")
                    ]
                    profile = year.create_child_node_instance(
                        cluster_profile_dictionary[cluster_type]
                    )
                    cluster = profile.create_child_node_instance(cluster_type)
                    hazard_type = cluster.create_child_node_instance(
                        event[1].strip("\n")
                    )
                    hazard_type.add_data(None, event[3].strip("\n"), 0)
                except KeyError:
                    hazards_to_be_sorted.add(event[1].title().strip("\n"))
        event = []

        """
        USED FOR INITIAL DICTIONARY COMPLETION
        print("IFRC Hazards to be sorted:")
        print(hazards_to_be_sorted)
        """


class IDMCFileReader(FileReader):
    def parse_data(self):
        # ISO3,Date of event (start),Disaster Internal Displacements,Hazard Type
        hazards_to_be_sorted = set()
        for line in self.data[1:]:
            event = line.split(",")
            """
            event[0] iso of country where disaster occurred
            event[1] date of disaster
            event[2] displacements
            event[3] hazard type
            """
            if event[2] not in EMPTIES:
                country = self.target.create_child_node_instance(event[0])
                month = country.create_child_node_instance(event[1].split("/")[1])
                year = month.create_child_node_instance(event[1].split("/")[-1])
                try:
                    cluster_type = hazard_profile_dictionary[
                        event[3].title().strip("\n")
                    ]
                    profile = year.create_child_node_instance(
                        cluster_profile_dictionary[cluster_type]
                    )
                    cluster = profile.create_child_node_instance(cluster_type)
                    hazard_type = cluster.create_child_node_instance(
                        event[3].strip("\n")
                    )
                    hazard_type.add_data(None, event[2].strip("\n"), 0)
                except KeyError:
                    hazards_to_be_sorted.add(event[3].title().strip("\n"))
        event = []

        """
        USED FOR INITIAL DICTIONARY COMPLETION
        print("IDMC Hazards to be sorted:")
        print(hazards_to_be_sorted)
        """


class EMDATFileReader(FileReader):
    def parse_data(self):
        # Disaster Group,Disaster Type,ISO,Start Year,Start Month,Total Deaths,Total Affected
        hazards_to_be_sorted = set()
        for line in self.data[1:]:
            event = line.split(",")
            """
            event[0] Disaster Type
            event[1] ISO of country where disaster occured
            event[2] Start Year
            event[3] Start Month
            event[4] Total Deaths
            event[5] Total Affected
            """
            if not ((event[4] in EMPTIES) or (event[5] in EMPTIES)):
                country = self.target.create_child_node_instance(event[1])
                month = country.create_child_node_instance(event[3])
                year = month.create_child_node_instance(event[2])
                try:
                    cluster_type = hazard_profile_dictionary[
                        event[0].title().strip("\n")
                    ]
                    profile = year.create_child_node_instance(
                        cluster_profile_dictionary[cluster_type]
                    )
                    cluster = profile.create_child_node_instance(cluster_type)
                    hazard_type = cluster.create_child_node_instance(
                        event[0].title().strip("\n")
                    )
                    hazard_type.add_data(event[4], event[5].strip("\n"), 2)
                except KeyError:
                    hazards_to_be_sorted.add(event[0].title().strip("\n"))
        event = []

        """
        USED FOR INITIAL DICTIONARY COMPLETION
        print("EMDAT Hazards that need to be sorted:")
        print(hazards_to_be_sorted)
        """


class DesInventarFileReader(FileReader):
    def parse_data(self):
        directory = os.fsencode(self.file_path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename == ".DS_Store":
                continue
            country_directory = f"{self.file_path}/{filename}"
            with open(country_directory, "r") as f:
                data = f.readlines()
            for line in data[1:]:
                event = line.split(",")
                """
                event[0] Event
                event[1] Date (YMD)
                event[2] Deaths
                event[3] Directly affected
                event[4] Indirectly Affected
                --- Pacific Islands Only ---
                event[5] Country
                """
                # remove leading and trailing whitespace
                for i in range(len(event)):
                    event[i] = event[i].strip("\n")
                    event[i] = event[i].lstrip(" ")
                    event[i] = event[i].rstrip(" ")
                    event[i] = event[i].title()
                try:
                    temp = hazard_profile_dictionary[event[0].title().strip("\n")]
                except KeyError as e:
                    # hazards we have disgregarded
                    continue
                if not (
                    (event[2] in EMPTIES)
                    or (event[3] in EMPTIES)
                    or (event[4] in EMPTIES)
                ):
                    if "India" in filename:
                        filename = "India.csv"

                    if "Pacific Islands" in filename:
                        country = self.target.create_child_node_instance(
                            country_to_iso_dictionary[event[5].title()]
                        )
                    else:
                        country = self.target.create_child_node_instance(
                            country_to_iso_dictionary[
                                ".".join(filename.split(".")[:-1]).title()
                            ]
                        )

                    try:
                        month = country.create_child_node_instance(
                            event[1].split("/")[1]
                        )
                    except Exception as e:
                        print(e)
                        print(event)
                        print(filename)
                    year = month.create_child_node_instance(event[1].split("/")[0])

                    cluster_type = hazard_profile_dictionary[
                        event[0].title().strip("\n")
                    ]
                    profile = year.create_child_node_instance(
                        cluster_profile_dictionary[cluster_type]
                    )
                    cluster = profile.create_child_node_instance(cluster_type)
                    hazard_type = cluster.create_child_node_instance(
                        event[0].title().strip("\n")
                    )
                    try:
                        effected = int(event[3].strip("\n")) + int(event[4].strip("\n"))
                    except:
                        effected = event[3].strip("\n")
                    try:
                        hazard_type.add_data(event[2], effected, 3)
                    except Exception as e:
                        print(e)
                        print(event)
