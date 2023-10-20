<img src="./magvit2.png" width="400px"></img>

## MagViT2 - Pytorch (wip)

Implementation of MagViT2 from <a href="https://arxiv.org/abs/2310.05737">Language Model Beats Diffusion - Tokenizer is Key to Visual Generation</a> in Pytorch

The Lookup Free Quantizer proposed in the paper can be found in a <a href="https://github.com/lucidrains/vector-quantize-pytorch/blob/master/vector_quantize_pytorch/lookup_free_quantization.py">separate repository</a>. It should probably be explored for all other modalities.

## Install

```bash
$ pip install magvit2-pytorch
```

## Usage

```python
import torch
from magvit2_pytorch.magvit2_pytorch import VideoTokenizer

tokenizer = VideoTokenizer(
    image_size = 256,
    init_dim = 64,
    layers = (
        'residual',
        ('compress_space', 128),
        'residual',
        'residual',
        'attend_space',
        ('compress_time', 256),
        'attend_time'
    )
)

# get a ton of videos

videos = torch.randn(2, 3, 16 + 1, 256, 256) # (batch, channels, time, height, width)

# course it through the autoencoder

total_loss, loss_breakdown = tokenizer(videos, return_loss = True)
total_loss.backward()

# after much training above, you can get the tokenized codes

tokenizer.eval()
codes = tokenizer(videos, return_codes = True)

```

## Todo

- [ ] Magvit2 Tokenizer
    - [x] add adversarial loss
    - [x] implement the blurpool for antialiasing in discriminator
    - [x] LFQ should be able to pass loss breakdown (commitment and entropy), and forwarded to the return of the tokenizer
    - [ ] add trainer and manage discriminator training
    - [ ] completely generalize to multiple discriminators at different time scales (taking inspiration of multi-resolution discriminators from soundstream)
    - [ ] add local attention; even if not in the paper, i've seen too much not to use it

- [ ] MaskGit

## Citations

```bibtex
@misc{yu2023language,
    title   = {Language Model Beats Diffusion -- Tokenizer is Key to Visual Generation}, 
    author  = {Lijun Yu and José Lezama and Nitesh B. Gundavarapu and Luca Versari and Kihyuk Sohn and David Minnen and Yong Cheng and Agrim Gupta and Xiuye Gu and Alexander G. Hauptmann and Boqing Gong and Ming-Hsuan Yang and Irfan Essa and David A. Ross and Lu Jiang},
    year    = {2023},
    eprint  = {2310.05737},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```

```bibtex
@inproceedings{dao2022flashattention,
    title   = {Flash{A}ttention: Fast and Memory-Efficient Exact Attention with {IO}-Awareness},
    author  = {Dao, Tri and Fu, Daniel Y. and Ermon, Stefano and Rudra, Atri and R{\'e}, Christopher},
    booktitle = {Advances in Neural Information Processing Systems},
    year    = {2022}
}
```
