import requests
import uuid
import json


def get_solar_system_planets():
    endpoint = 'https://api.le-systeme-solaire.net/rest/bodies/'
    data = '?data=englishName,mass[[,massValue,massExponent]],vol[[,volValue,volExponent]],gravity,discoveryDate'
    filters = '&filter[]=isPlanet,cs,1&filter[]=aphelion,le,7376124302'
    order = '&order=aphelion,asc'
    r = requests.get(endpoint + data + filters + order)
    return r.json()


def set_unique_id(planets_object):
    def set_unique_id_to_body(body):
        body['uid'] = str(uuid.uuid4())
        return body

    pl_list = planets_object['bodies']
    pl_list = [set_unique_id_to_body(x) for x in pl_list]
    planets_object['bodies'] = pl_list
    return planets_object


def set_position_by_volume(planets_object):
    def calc_float_volume(body):
        body['vol_float'] = body['vol']['volValue'] * (10 ** body['vol']['volExponent'])
        return body

    def set_order_field(body, position, len_struc):
        body['volume_rank'] = len_struc - position
        return body

    def remove_field(body, field_name):
        body.pop(field_name, None)
        return body

    pl_list = planets_object['bodies']
    pl_list = [calc_float_volume(x) for x in pl_list]
    pl_list = sorted(pl_list, key=lambda x: x['vol_float'])
    len_structure = len(pl_list)
    pl_list = [set_order_field(x, ind, len_structure) for ind, x in enumerate(pl_list)]
    pl_list = [remove_field(x, 'vol_float') for x in pl_list]
    planets_object['bodies'] = pl_list
    return planets_object


if __name__ == '__main__':
    planets = get_solar_system_planets()
    planets = set_position_by_volume(planets)
    planets = set_unique_id(planets)

    json_object = json.dumps(planets, indent=4)
    print(json_object)
