import requests
import json


class Element:
    """
    Element class

    Attributes:
        _id (int): Element id
        color (str): Element color
        start (int): Element start time in minutes
        end (int): Element end time in minutes
        lane (int): Element lane id
        text (str): Element text
    """

    def __init__(self, _id: str, color: str, start: int, end: int, lane: int, text=""):
        """
        Constructor
        :param _id: Element id
        :param color: Element color
        :param start: Element start time in minutes
        :param end: Element end time in minutes
        :param lane: Element lane id
        :param text: Element text
        """
        self.color = color
        self.start = start
        self.end = end
        self.lane = lane - 1
        self.id = _id
        self.text = text

    def get_json(self) -> dict:
        """
        Get Element as json
        :return: dictionary
        """
        return {
            "color": self.color,
            "start": self.start,
            "end": self.end,
            "lane": self.lane,
            "text": self.text,
        }


class Chart:
    """
    Chart class

    Attributes:
        colorTags (dict): Dict of color tags
        elements (dict): Dict of elements
    """
    colorTags = {
        "red": "",
        "blue": "",
        "brown": "",
        "green": "",
        "gray": "",
        "yellow": "",
        "purple": "",
        "pink": "",
    }

    def __init__(self, lanes_count, shape="circle",
                 name="Sample Chart", description="Sample Description"):
        """
        Constructor
        :param lanes_count: Number of lanes
        :param shape: Shape of chart(circle, wide, line)
        :param name: Chart title
        :param description: Chart description
        """
        self.elements = dict()
        self.name = name
        self.description = description
        self.lanes_count = lanes_count
        self.shape = shape
        self.lanes_config = {}
        for i in range(lanes_count):
            self.lanes_config[str(i + 1)] = {
                "locked": False,
            }

    def add_element(self, element: Element):
        """
        Add element to chart
        :param element: Element to be added
        :return: None
        """
        self.elements[element.id] = element

    def remove_element(self, element_id: str):
        """
        Remove element from chart
        :param element: Element to be removed
        :return: None
        """
        del self.elements[element_id]

    def lock_lane(self, lane: int):
        """
        Lock lane
        :param lane: id of lane to be locked
        :return: None
        """
        self.lanes_config[str(lane)]["locked"] = True

    def unlock_lane(self, lane: int):
        """
        Unlock lane
        :param lane: id of lane to be unlocked
        :return: None
        """
        self.lanes_config[str(lane)]["locked"] = False

    def lock_all_lanes(self):
        """
        Lock all lanes
        :return: None
        """
        for lane in range(self.lanes_count):
            self.lock_lane(lane)

    def unlock_all_lanes(self):
        """
        Unlock all lanes
        :return: None
        """
        for lane in range(self.lanes_count):
            self.unlock_lane(lane)

    def _get_tags_json(self) -> list:
        ret_dict = []
        for color in self.colorTags:
            if self.colorTags[color] != "":
                ret_dict.append({
                    "color": color,
                    "tag": self.colorTags[color]
                })
        return ret_dict

    def _get_json(self) -> dict:
        """
        Get chart as json
        :return: result dictionary
        """
        return {
            "title": self.name,
            "description": self.description,
            "chartData": {
                "lanes": self.lanes_count,
                "shape": "circle",
                "elements": [element.get_json() for element in self.elements.values()],
                "colorTags": self._get_tags_json(),
                "lanesConfig": self.lanes_config,
            },
        }

    def upload(self) -> str:
        """
        Upload chart to server
        :return: link of uploaded chart
        """
        url = "https://api.napchart.com/v1/createSnapshot"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        data = json.dumps(self._get_json())
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["publicLink"]
        else:
            raise Exception("Error while uploading chart. Status code: {}, Response: {}".format(response.status_code,
                                                                                                response.text))


def simplify_time(hours: int, minutes: int) -> int:
    """
    Simplify time to minutes
    :param hours: hours
    :param minutes: minutes
    :return: time in minutes
    """
    return hours * 60 + minutes


def format_time(time: str) -> int:
    """
    Format time to minutes
    Example: "23:30" -> 730
    :param time: time in format "HH:MM"
    :return: time in minutes
    """
    hours, minutes = time.split(":")
    return simplify_time(int(hours), int(minutes))


def _generate_chart(chart_document) -> Chart:
    """
    Generate chart from document
    :param chart_document: dictionary with document data
    :return: resulting Chart object
    """
    chart_data = chart_document["chartData"]
    new_chart = Chart(lanes_count=chart_data["lanes"], shape=chart_data["shape"], name=chart_document["title"],
                      description=chart_document["description"])
    for lane in chart_data["lanesConfig"]:
        if chart_data["lanesConfig"][lane]["locked"]:
            new_chart.lock_lane(int(lane))

    element_id = 1
    for element in chart_data["elements"]:
        new_element = Element(str(element_id), element["color"], element["start"], element["end"], element["lane"] + 1,
                              text=element["text"])
        new_chart.add_element(new_element)
        element_id += 1

    for color in chart_data["colorTags"]:
        new_chart.colorTags[color["color"]] = color["tag"]

    return new_chart


def import_chart(id_: str) -> Chart:
    """
    Import chart from site
    :param id_: id of chart from the end of url (for example 'da3eo3DA')
    :return:
    """
    url = "https://api.napchart.com/v1/getChart/" + id_
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return _generate_chart(response.json()["chartDocument"])
    else:
        raise Exception("Error while importing chart. Status code: {}, Response: {}".format(response.status_code,
                                                                                            response.text))
