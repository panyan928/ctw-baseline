with open("labelmap.prototxt", 'w') as f:
        for i in range(0, 2501):
            name = 'background' if i == 0 else str(i)
            f.write('item {\n')
            f.write('  name: "{:s}"\n'.format(name))
            f.write('  label: {:d}\n'.format(i))
            f.write('  display_name: "{:s}"\n'.format(name))
            f.write('}\n')
