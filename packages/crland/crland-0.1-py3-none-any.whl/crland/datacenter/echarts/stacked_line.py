from typing import Dict, Any, Union, List

def stack_line(inputs: Union[Dict[str, Any], List[Any]], 
        labels: Dict[str, str]) -> Dict[str, Any]:
    """ translate dataformat to echart format for bar
        :param inputs: Data from database（x, y）
        :param labels: Identify labels of Data (title)
        :return option: echart format
    """
    x = []
    y = {}
    legend = labels["y"]
    if isinstance(legend, str):
        legend = [legend]
    if isinstance(inputs, List):
        xlabel = labels['x']
        for i in inputs:
            x.append(i[xlabel])
            for j in legend:
                if j not in y:
                    y[j] = []
                y[j].append(i[j])
    series = [
        {
            "name": x,
            "type": 'line',
            #"stack": 'Total',
            "data": y[x]
        } for x in legend
    ]
    option = {
        "title": {
            "text": labels["title"],
        },
        "tooltip": {
            "trigger": 'axis'
        },
        "legend": {
            "data": legend
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": {
            "type": 'category',
            "boundaryGap": False,
            "data": x
        },
        "yAxis": {
            "type": 'value'
        },
        "series": series
    }
    return option