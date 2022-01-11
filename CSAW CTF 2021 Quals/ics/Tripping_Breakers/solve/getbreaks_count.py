#!/usr/bin/env python3

class Substation:

    def __init__(self, ip_address, devices):
        self.devices = []
        for device in devices:
            self.add_device(device)

    def add_device(self, device):
        self.devices.append({'dst':device[0],  'count':device[1]})
    
    def __len__(self):
        total = 0
        for device in self.devices:
            total += device['count']
        return total


def main():
    substation_b = Substation('10.95.101.81', [(9, 5), (8, 7), (20, 12), (15, 19)])
    substation_c = Substation('10.95.101.82', [(14, 14), (9, 16), (15, 4), (12, 5)])
    substation_d = Substation('10.95.101.83', [(20, 17), (16, 8), (8, 14)])

    substation_f = Substation('10.95.101.85', [(1, 4), (3, 9)])

    substation_h = Substation('10.95.101.87', [(4, 1), (10, 9), (13, 6), (5, 21)])
    substation_i = Substation('10.95.101.88', [(14, 13), (19, 2), (8, 6), (17, 8)])

    substations = (substation_b, substation_c, substation_d, substation_f, substation_h, substation_i)
    
    print("Total Breakers: {}".format(sum(len(s) for s in substations)))

if __name__ == '__main__':
    main()