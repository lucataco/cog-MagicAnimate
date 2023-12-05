# magic-research / magic-animate Cog model

This is an implementation of [magic-research / magic-animate](https://github.com/magic-research/magic-animate) as a [Cog](https://github.com/replicate/cog) model.

## Development

Follow the [model pushing guide](https://replicate.com/docs/guides/push-a-model) to push your own model to [Replicate](https://replicate.com).

## Basic Usage

Download weights first

    cog run script/download-weights

Then for predictions,

    cog predict -i image=@demo4.png -i video=@demo4.mp4

