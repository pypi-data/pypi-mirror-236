import dataclasses
import inspect
from typing import Any, Dict, Iterator, List, Optional, Type

import fiddle
from fiddle import config
from fiddle import daglish
from fiddle.experimental import serialization


def _has_nested_builder(value: Any, state=None) -> bool:
    state = state or daglish.MemoizedTraversal.begin(_has_nested_builder, value)
    return isinstance(value, config.Buildable) or (
        state.is_traversable(value) and any(state.flattened_map_children(value).values)
    )


def _path_str(path: daglish.Path) -> str:
    """Formats path in a way customized to this file.

    In the future, we may wish to consider a format that is readable for printing
    more arbitrary collections.

    Args:
      path: A path, which typically starts with an attribute.

    Returns:
      String representation of the path.
    """
    path_str = daglish.path_str(path)
    return path_str[1:] if path and isinstance(path[0], daglish.Attr) else path_str


@dataclasses.dataclass(frozen=True)
class _LeafSetting:
    """Represents a leaf configuration setting."""

    path: daglish.Path
    annotation: Optional[Type[Any]]
    value: Any


def as_flattened_dict(
    cfg: config.Buildable, include_buildable: bool = True
) -> Dict[str, Any]:
    """Returns a flattened dict of cfg's paths (dot syntax) and values.

    Default values and tags won't be included in the flattened dict.

    Args:
      cfg: A buildable to generate a flattened dict representation for.

    Returns: A flattened Dict representation of `cfg`.
    """

    def dict_generate(value, state=None) -> Iterator[_LeafSetting]:
        state = state or daglish.BasicTraversal.begin(dict_generate, value)

        if not _has_nested_builder(value):
            yield _LeafSetting(state.current_path, None, value)
        else:
            # value must be a Buildable or a traversable containing a Buildable.
            assert state.is_traversable(value)
            if isinstance(value, config.Buildable) and include_buildable:
                module = inspect.getmodule(value.__fn_or_cls__).__name__  # type: ignore
                name = value.__fn_or_cls__.__qualname__
                ctor_name = f"{module}:{name}"
                yield _LeafSetting(
                    state.current_path + (daglish.Attr("__ctor__"),), None, ctor_name
                )
            for sub_result in state.flattened_map_children(value).values:
                yield from sub_result

    args_dict = {}
    for leaf in dict_generate(cfg):
        args_dict[_path_str(leaf.path)] = leaf.value

    return args_dict


def basic_callable(a: int = 1):
    pass


@dataclasses.dataclass
class ExperimentConfig:
    fn: Any
    seed: int
    name: str
    test: bool
    nest: Dict
    list_: List
    unset: int = 1


if __name__ == "__main__":
    import wandb

    wandb.init(project="lxm3", mode="disabled")

    cfg = fiddle.Config(
        ExperimentConfig,
        fn=fiddle.Partial(basic_callable, a=2),
        seed=42,
        name="test",
        test=True,
        nest={"a": 1, "b": 2},
        list_=[1, 2, 3],
    )

    # artifact.add_file("config.json", serialization.dump_json(cfg))
    dumped = serialization.dump_json(cfg)
    artifact = wandb.Artifact(name="config", type="fiddle_config")
    with artifact.new_file("config.json", "wt") as f:
        f.write(dumped)
    wandb.log_artifact(artifact)
    flat = as_flattened_dict(cfg)
    print(flat)
