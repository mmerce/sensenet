from sensenet.constants import NUMERIC, CATEGORICAL

def get_output_exposition(model):
    if 'output_exposition' in model:
        return model['output_exposition']
    elif 'networks' in model:
        first_network = model['networks'][0]
        return get_output_exposition(first_network)
    else:
        raise ValueError('Could not locate output_exposition')

def number_of_outputs(model):
    outex = get_output_exposition(model)

    if outex['type'] == NUMERIC:
        return 1
    elif outex['type'] == CATEGORICAL:
        return len(outex['values'])
    else:
        raise ValueError('Output exposition is type "%s"' % outex['type'])
