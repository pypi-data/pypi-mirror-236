from wordpredict.utils import (
    build_trie,
    get_autocomplete_candidates,
    update_valid_prefixes,
)


class WordPredict:
    def __init__(self, corpus_words: list[str], corpus_freq: list[int], alpha=0.62):
        self.valid_prefixes = []
        self.root = build_trie(corpus_words, corpus_freq, alpha)

    def update(self, new_char_list: list[str], max_candidates=6):
        if len(new_char_list) > 0:
            self.valid_prefixes = update_valid_prefixes(
                self.valid_prefixes,
                new_char_list,
                self.root,
            )

        return get_autocomplete_candidates(
            self.root,
            self.valid_prefixes,
            max_candidates,
        )

    def reset(self):
        """Resets the list of valid prefixes."""
        self.valid_prefixes = []

    def get_current_candidates(self, max_candidates=6):
        """
        Returns the current candidates without updating.
        """
        return get_autocomplete_candidates(
            self.root,
            self.valid_prefixes,
            max_candidates,
        )
