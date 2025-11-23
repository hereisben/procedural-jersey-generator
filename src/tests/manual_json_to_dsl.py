from src.interpreter.json_to_dsl import jersey_json_to_dsl

data = {
    "team": "Juventus",
    "player": "VLAHOVIC",
    "number": 9,
    "sponsor": "Jeep",
    "font": "Sport Scholars Outline",
    "primary": "#fefefe",
    "secondary": "#000000",
    "tertiary": "#d4a856",
    "pattern": {
        "type": "stripes",
        "args": [9, 18]
    },
    "patternColor": "#000000",
    "source": {
        "fromText": True,
        "fromImage": True,
        "imageAnalysisConfidence": 0.78
    },
    "approximationNote": "Approximation of the Juventus 23/24 away kit using flat stripes and simple colors."
}

dsl = jersey_json_to_dsl(data)
print(dsl)
