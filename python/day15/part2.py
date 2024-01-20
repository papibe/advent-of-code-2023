from typing import Dict, List


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()[0]

    box: List[Dict[str, int]] = [{} for _ in range(256)]

    for seq in data.split(","):
        value: int = 0
        if seq.endswith("-"):
            label: str = seq[:-1]
            for char in label:
                value += ord(char)
                value *= 17
                value %= 256

            # remove lens with label if it's there
            if label in box[value]:
                del box[value][label]

        else:
            lens: int = int(seq[-1])
            label = seq[:-2]
            for char in label:
                value += ord(char)
                value *= 17
                value %= 256

            # replace labeled lens with new one ig it's there
            if label in box[value]:
                box[value][label] = lens
            else:
                box[value][label] = lens

    total: int = 0
    for index, label_lens in enumerate(box):
        if label_lens:
            slot: int = 1
            for label, lens in label_lens.items():
                value = (index + 1) * slot * lens
                total += value
                slot += 1

    return total


if __name__ == "__main__":
    print(solution("./example.txt"))  # 145
    print(solution("./input.txt"))  # 244981
