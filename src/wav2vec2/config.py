import json
import os
from dataclasses import asdict, dataclass, field


@dataclass
class Wav2Vec2Config:
    vocab_size: int = 32
    dropout: int = 0.1
    hidden_size: int = 768
    num_heads: int = 12
    num_layers: int = 12
    intermediate_size: int = 3072
    is_gelu_approx: bool = False
    layer_norm_eps: float = 1e-5
    layer_drop: float = 0.1
    pad_id: int = 0
    loss_reduction: str = field(
        default="sum", metadata={"help": "Possible values are `mean` & `sum`"}
    )

    # positional embedding
    num_conv_pos_embeddings: int = 128
    num_conv_pos_embedding_groups: int = 16

    # feature extractor
    filter_sizes: list = field(
        default_factory=lambda: [512, 512, 512, 512, 512, 512, 512]
    )
    kernal_sizes: list = field(default_factory=lambda: [10, 3, 3, 3, 3, 2, 2])
    strides: list = field(default_factory=lambda: [5, 2, 2, 2, 2, 2, 2])
    conv_bias: bool = False

    # spec augmentation arguments
    apply_spec_augment: bool = False  # TODO: fix this
    mask_time_prob: float = 0.05
    mask_time_length: int = 10

    def __post_init__(self):
        if not (len(self.filter_sizes) == len(self.kernal_sizes) == len(self.strides)):
            raise ValueError("len of filter_sizes, kernal_sizes, strides must match")
        if self.hidden_size % self.num_heads != 0:
            raise ValueError("Hidden size must be perfect multiple of num_heads")

        assert self.loss_reduction in [
            "mean",
            "sum",
        ], "Possible values of `loss_reduction` are `mean` & `sum`"

    def save_pretrained(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, "config.json"), "w") as f:
            json.dump(asdict(self), f)

    @classmethod
    def from_json(cls, path: str):
        with open(path, "r") as f:
            config_dict = json.load(f)
        return cls(**config_dict)


if __name__ == "__main__":
    """Testing area"""

    config = Wav2Vec2Config()
    print(config)
    config.save_pretrained("dummy")
