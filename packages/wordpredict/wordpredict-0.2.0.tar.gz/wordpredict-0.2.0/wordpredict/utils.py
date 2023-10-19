class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}

        # only leaf nodes have this attribute
        self.prob_and_word: tuple[float, str] | None = None

    def get_all_leaf_nodes(self) -> list["TrieNode"]:
        leaf_nodes = [self] if self.prob_and_word else []

        for child in self.children.values():
            leaf_nodes.extend(child.get_all_leaf_nodes())

        return leaf_nodes


def build_trie(
    corpus_words: list[str], corpus_freq: list[int], alpha: float
) -> TrieNode:
    root = TrieNode()
    word_freq = dict(zip(corpus_words, corpus_freq))

    for word, freq in word_freq.items():
        node = root
        for i, char in enumerate(word):
            node = node.children.setdefault(char, TrieNode())

            if i == len(word) - 1:  # leaf node
                prob = (alpha ** (len(word) - i)) * freq
                node.prob_and_word = (prob, word)

    return root


def find_node_for_prefix(root: TrieNode, prefix: str) -> TrieNode | None:
    node = root
    for char in prefix:
        if char not in node.children:
            return None
        node = node.children[char]
    return node


def update_valid_prefixes(
    old_valid_prefixes: list[str], new_char_list: list[str], root: TrieNode
):
    if len(old_valid_prefixes) == 0:
        return [char for char in new_char_list if char in root.children]

    new_valid_prefixes = [
        valid_prefix + new_char
        for valid_prefix in old_valid_prefixes
        for new_char in new_char_list
        if new_char in find_node_for_prefix(root, valid_prefix).children
    ]
    return new_valid_prefixes


def get_autocomplete_candidates(
    root: TrieNode, valid_prefixes: list[str], max_candidates: int
) -> list[str]:
    prob_and_word_list = [
        leaf.prob_and_word
        for prefix in valid_prefixes
        for leaf in find_node_for_prefix(root, prefix).get_all_leaf_nodes()
    ]

    prob_and_word_list.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in prob_and_word_list[:max_candidates]]
