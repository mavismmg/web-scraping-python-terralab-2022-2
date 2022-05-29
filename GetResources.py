import numpy as np
import pandas as pd
import requests as re

from bs4 import BeautifulSoup


class GetResources:
    html = re.get("https://www.payscale.com/research/US/Job=Software_Developer/Salary").content

    soup = BeautifulSoup(html, "html.parser")

    def __init__(self):
        self.name = "div"
        self.class_ = "tablerow__value"
        self.disallowed_chars = "$k"

    def extract_data(self, set_index):
        find_data = self.soup.find_all(name=self.name, class_=self.class_)

        raw_values = []
        for value in find_data:
            cur_value = value.text.split()
            clean = cur_value[set_index]
            raw_values.append(clean)

        alloc_temporary = []
        for index in range(len(raw_values)):
            clean = raw_values[index].replace(self.disallowed_chars[0], "")
            alloc_temporary.append(clean)

        data = []
        for index in range(len(raw_values)):
            clean = alloc_temporary[index].replace(self.disallowed_chars[1], "000")
            data.append(clean)

        data = np.array(data)

        return data

    @staticmethod
    def create_dataframe():
        min_values_data = GetResources().extract_data(0)
        max_values_data = GetResources().extract_data(2)

        data_df = pd.DataFrame(min_values_data, {"Base Salary": min_values_data[0],
                                                 "Bonus": min_values_data[1],
                                                 "Profit Sharing": min_values_data[2],
                                                 "Commission": min_values_data[3],
                                                 "Total Pay": min_values_data[4]},
                               columns=["Min"])

        data_df["Min"] = pd.to_numeric(data_df["Min"])

        temporary_df = pd.DataFrame(max_values_data, {"Base Salary": max_values_data[0],
                                                      "Bonus": max_values_data[1],
                                                      "Profit Sharing": max_values_data[2],
                                                      "Commission": max_values_data[3],
                                                      "Total Pay": max_values_data[4]},
                                    columns=["Max"])

        temporary_df["Max"] = pd.to_numeric(temporary_df["Max"])

        data_df["Max"] = temporary_df["Max"]

        return data_df
