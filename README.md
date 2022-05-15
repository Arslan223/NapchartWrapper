# NapchartWrapper
#### _Simple and easy to use unofficial Napchart API Wrapper._

## Features

- Create chart and upload it to napchart
- Import chart from napchart and edit it

All the possibilities of napchart.com are implemented in this API wrapper.

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
[Documentation](https://readthedocs.org)

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

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## License

MIT
