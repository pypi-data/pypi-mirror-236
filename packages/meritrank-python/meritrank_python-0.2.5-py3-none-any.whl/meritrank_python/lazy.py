from meritrank_python.rank import IncrementalMeritRank


class LazyMeritRank(IncrementalMeritRank):
    """
    This is a basic lazy-calculated variant of IncrementalMeritRank.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # The set of egos for which MeritRank has already been calculated
        self.__egos = set()

    def __maybe_add_ego(self, ego):
        if ego not in self.__egos:
            self.logger.debug("LazyMeritRank: Adding new ego: %s", ego)
            self.calculate(ego)
            self.__egos.add(ego)

    def get_ranks(self, ego, *args, **kwargs):
        self.__maybe_add_ego(ego)
        return super().get_ranks(ego, *args, **kwargs)

    def get_node_score(self, ego, *args, **kwargs):
        self.__maybe_add_ego(ego)
        return super().get_node_score(ego, *args, **kwargs)

