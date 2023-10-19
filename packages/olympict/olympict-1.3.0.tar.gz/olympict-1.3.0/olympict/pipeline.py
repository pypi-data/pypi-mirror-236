from typing import Generic, Iterable, List, Optional, TypeVar, cast

from olympipe import Pipeline

T = TypeVar("T")


class OPipeline(Generic[T]):
    def __init__(
        self,
        data: Optional[Iterable[T]] = None,
        extending: Optional["Pipeline[T]"] = None,
    ):
        assert (
            data is not None or extending is not None
        ), "You must either provide data or another pipeline"

        self.pipeline: Pipeline[T] = (
            cast(Pipeline[T], extending) if data is None else Pipeline(data)
        )
        self._data = data

    def wait_for_completion(self, debug_graph: Optional[str] = None) -> None:
        """Needed to launch and complete the pipeline.

        Args:
            debug_graph (Optional[str], optional): Path to .png file representing the pipe. Defaults to None.
        """
        return self.pipeline.wait_for_completion(debug_graph=debug_graph)

    def wait_for_results(self, debug_graph: Optional[str] = None) -> List[T]:
        """Needed to launch and complete the pipeline. Keeps the outputs at the pipeline's end as results.

        Args:
            debug_graph (Optional[str], optional): Path to .png file representing the pipe. Defaults to None.

        Returns:
            List[T]: Your last processed outputs
        """
        return self.pipeline.wait_for_results(debug_graph=debug_graph)[0]
