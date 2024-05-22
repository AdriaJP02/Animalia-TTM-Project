def extract_labels_animals(features_extracted):
    labels_animals = []
    unique_animals = set()

    label_count = 0
    animal_label_map = {}

    for file in features_extracted.keys():
        animal_name, _ = file.split('_', 1)
        _,animal_name = animal_name.split('segments/',1)
        unique_animals.add(animal_name)


        if animal_name not in animal_label_map:
            animal_label_map[animal_name] = label_count
            label_count += 1

        labels_animals.append(animal_label_map[animal_name])

    print("TOTAL LABELS: ", len(labels_animals))
    print("UNIQUE ANIMALS: ", unique_animals)
    return labels_animals, list(unique_animals)
