import sys
from lib.find_object import find_object
from lib.geocoder import get_coordinates
from lib.distancee import distancee
from lib.shop_map import show_map


def main():
    searching = ' '.join(sys.argv[1:])
    dolgota, shirota = get_coordinates(searching)
    address_ll = f'{dolgota},{shirota}'
    span = '0.005,0.005'

    spisok = []
    for i in range(10):
        try:
            pharmacy = find_object(address_ll, span, 'аптека')['features'][i]
        except:
            break
        pharmacy_dolgota = float(pharmacy['geometry']['coordinates'][0])
        pharmacy_shirota = float(pharmacy['geometry']['coordinates'][1])

        try:
            yes = pharmacy['properties']['CompanyMetaData']['Hours']
        except Exception:
            yes = False

        if yes:
            try:
                hours = pharmacy['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['TwentyFourHours']
            except Exception:
                hours = False
            try:
                everyday = pharmacy['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['Everyday']
            except Exception:
                everyday = False

        if not yes:
            a = 'gr'
        elif yes and hours and everyday:
            a = 'gn'
        else:
            a = 'bl'

        point_param = f'pt={pharmacy_dolgota},{pharmacy_shirota},pm2{a}l'
        points_param = point_param + f'~{address_ll},pm2rdl'

        name = pharmacy['properties']['CompanyMetaData']['name']
        address = pharmacy['properties']['CompanyMetaData']['address']
        time = pharmacy['properties']['CompanyMetaData']['Hours']['text']
        distance = round(distancee((dolgota, shirota), (pharmacy_dolgota, pharmacy_shirota)))
        out = f'{name}\n{address}\n{time}\n{distance}м.'
        print(out)
        spisok.append(points_param[3:])

    show_map(params=spisok)


if __name__ == '__main__':
    main()
