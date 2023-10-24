from typing import Mapping, Sequence

from permchain.channels.base import BaseChannel
from permchain.pregel.read import PregelBatch, PregelInvoke


def validate_chains_channels(
    chains: Mapping[str, PregelInvoke | PregelBatch],
    channels: Mapping[str, BaseChannel],
    input: str | Sequence[str],
    output: str | Sequence[str],
) -> None:
    subscribed_channels = set[str]()
    for chain in chains.values():
        if isinstance(chain, PregelInvoke):
            subscribed_channels.update(chain.channels.values())
        elif isinstance(chain, PregelBatch):
            subscribed_channels.add(chain.channel)
        else:
            raise TypeError(
                f"Invalid chain type {type(chain)}, expected Channel.subscribe_to() or Channel.subscribe_to_each()"
            )

    for chan in subscribed_channels:
        if chan not in channels:
            raise ValueError(f"Channel {chan} is subscribed to, but not initialized")

    if isinstance(input, str):
        if input not in subscribed_channels:
            raise ValueError(f"Input channel {input} is not subscribed to by any chain")
    else:
        if all(chan not in subscribed_channels for chan in input):
            raise ValueError(
                f"None of the input channels {input} are subscribed to by any chain"
            )

    if isinstance(output, str):
        if output not in channels:
            raise ValueError(f"Output channel {output} is not initialized")
    else:
        for chan in output:
            if chan not in channels:
                raise ValueError(f"Output channel {chan} is not initialized")
