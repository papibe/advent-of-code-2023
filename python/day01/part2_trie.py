DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}

STIGID = {
    "eno": 1,
    "owt": 2,
    "eerht": 3,
    "ruof": 4,
    "evif": 5,
    "xis": 6,
    "neves": 7,
    "htgie": 8,
    "enin": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.word = ""


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_word = True
        current.word = word

    def search(self, word, start, end, step):
        current = self.root
        for index in range(start, end, step):
            char = word[index]
            if char not in current.children:
                return False, ""
            current = current.children[char]
            if current.is_word:
                return True, current.word
        return current.is_word, ""


def solution(filename: str) -> int:
    # forward search tree
    search_trie: Trie = Trie()
    for word in DIGITS:
        search_trie.insert(word)

    # reverse search tree
    reverse_trie: Trie = Trie()
    for word in STIGID:
        reverse_trie.insert(word)

    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    addition: int = 0
    for _ in range(10_000):

        for line in data:
            line_len: int = len(line)

            for index in range(line_len):
                is_word, first_digit = search_trie.search(line, index, line_len, 1)
                if is_word:
                    break

            for index in range(line_len - 1, -1, -1):
                is_word, last_digit = reverse_trie.search(line, index, -1, -1)
                if is_word:
                    break

            addition += (DIGITS[first_digit] * 10) + STIGID[last_digit]

    return addition


if __name__ == "__main__":
    # print(solution("./example2.txt"))  # 281
    print(solution("./input.txt"))  # 54203
