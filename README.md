# NapchartWrapper
#### _Simple and easy to use unofficial Napchart API Wrapper._

## Features

- Create chart and upload it to napchart
- Import chart from napchart and edit it

All the possibilities of napchart.com are implemented in this API wrapper.

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## License

MIT

## Installation
```sh
pip3 install napchart
```
or
```sh
git clone https://github.com/Arslan223/NapchartWrapper.git
cd NapchartWrapper
./setup.py install
```

## Usage
Example 1
```python
from napchart import Chart, Element, format_time

chart = Chart(name="Test name", description="Test description", lanes_count=1)

chart.add_element(Element(
    _id="1",
    color="red",
    start=format_time("23:00"),
    end=format_time("7:00"),
    lane=1,
    text="Core",
))

chart.colorTags['red'] = "Sleep"

print(chart.upload())
```
Result: https://napchart.com/snapshot/ZYFc3ZDlI

Example 2
```python
from napchart import Chart, Element, format_time, import_chart

chart = import_chart("ZYFc3ZDlI")

chart.add_element(Element(
    _id="2",
    color="blue",
    start=format_time("13:00"),
    end=format_time("13:30"),
    lane=1,
    text="Nap",
))

chart.colorTags['red'] = "Core"
chart.colorTags['blue'] = "Nap"

print(chart.upload())
```
Result: https://napchart.com/snapshot/ZMcUeWxNo
## How to use
### Colors
There are 8 colors supported: red, blue, brown, green, gray, yellow, purple, pink.

### Shapes
There are 3 shapes supported: circle, wide, line

### Classes
##### Element
```python
from napchart import Element

element = Element(
    "1", # id for element (can be any unique str) (required)
    color='red', # you can use any from 8 supported colors (required)
    start=0, # start time for element in minutes. You better use format_time("HH:MM") (required)
    end=60, # end time for element in minutes. You better use format_time("HH:MM") (required)
    lane=1, # id of the lane the element should be at (required)
    text="hello" # text label for element (default="")
)
```

##### Chart
```python
from napchart import Chart, Element

chart = Chart(
    lanes_count=1, # count of lanes in the chart. (required)
    shape='circle', # choose the shape of the chart you want. (default="circle")
    name='Sample', # choose the title of the chart. (default="Sample Chart")
    description='Sample' # choose the description of the chart. (default="Sample Description")
)
```
###### Chart methods
add_element
```python
chart.add_element(element) # element (Element) to add to the chart [see Example 1]
```

remove_element
```python
chart.remove_element(element_id) # (str) id of Element to be removed from the chart [see Example 1]
```

lock_lane
```python
chart.lock_lane(lane_id) # (int) locks the lane with id=lane_id
```

unlock_lane
```python
chart.unlock_lane(lane_id) # (int) unlocks the lane with id=lane_id
```

lock_all_lanes
```python
chart.lock_all_lanes() # locks all lanes in the chart
```

unlock_all_lanes
```python
chart.lock_all_lanes() # unlocks all lanes in the chart
```

upload
```python
url = chart.upload() # uploads chart to napchart.com and returns url
```

## Functions
simplify_time
```python
>>> simplify_time(5, 15) # turns hours&minutes format to minutes
315
```

format_title
```python
>>> format_time("13:37") # turns string in format "HH:MM" to minutes (int)
817
```

import_chart
```python
chart = import_chart("ZYFc3ZDlI") # gets chart id (you can find it in the end of url) and turns it into Chart
```