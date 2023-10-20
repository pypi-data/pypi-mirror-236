# album_colours

Color your favorite albums into seaborn or matplotlib plots

## Installation

```bash
$ pip install album_colours 
```

## Usage

Use this way into your notebook or script:

```python
from album_colours import palette_generator

palette = palette_generator.color_gradient_generator('<palette>', 2)
```

We currently support the following albums:

* `devendra` [Flying Wig](https://pitchfork.com/reviews/albums/devendra-banhart-flying-wig/) - Devendra Banhart
* `alvaro_diaz` [Felicilandia](https://open.spotify.com/intl-es/album/7jg09IJJXi1eigVLZja2hN) - Álvaro Díaz
* `alvaro_diaz2` [Single Llori Pari](https://open.spotify.com/intl-es/album/4jG7eBaWlLUjRRS1ajTCJ3) - Álvaro Díaz
* `aventura` [The Last](https://en.wikipedia.org/wiki/The_Last_(album)) - Aventura
* `bad_bunny` [Un verano sin ti](https://open.spotify.com/intl-es/album/3RQQmkQEvNCY4prGKE6oc5) - Bad Bunny
* `frank_ocean` [Blonde](https://open.spotify.com/intl-es/album/3mH6qwIy9crq0I9YQbOuDf) - Frank Ocean
* `kanye` [The life of pablo](https://open.spotify.com/intl-es/album/7gsWAHLeT0w7es6FofOXk1) - Kanye West
* `kendrick` [DAMN](https://en.wikipedia.org/wiki/Damn_(Kendrick_Lamar_album)) - Kendrick Lamar
* `kendrick2` [good kid, m.A.A.d city](https://en.wikipedia.org/wiki/Good_Kid,_M.A.A.D_City) - Kendrick Lamar
* `kendrick3` [Mr. Morale & the Big Steppers](https://open.spotify.com/intl-es/album/79ONNoS4M9tfIA1mYLBYVX) - Kendrick Lamar
* `radiohead` [Kid A](https://en.wikipedia.org/wiki/Kid_A) - Radiohead
* `rosalia` [El Mal Querer](https://open.spotify.com/intl-es/album/355bjCHzRJztCzaG5Za4gq) - Rosalía
* `rosalia2` [Motomami](https://open.spotify.com/intl-es/album/6jbtHi5R0jMXoliU2OS0lo) - Rosalía
* `sen_senra` [Sensaciones](https://open.spotify.com/intl-es/album/7Hr8FOf7NQIe7UhLcllXq9) - Sen Senra
* `soda_stereo` [Nada Personal](https://es.wikipedia.org/wiki/Nada_personal_(%C3%A1lbum)) - Soda Stereo


- Please see the [example notebook](examples_plots.ipynb).

## Development

Some of the palettes look like this: 

![gradient-kid-a](example_images/gradients/gd4.png "Kid A")

`bad_bunny` [Un verano sin ti](https://open.spotify.com/intl-es/album/3RQQmkQEvNCY4prGKE6oc5) - Bad Bunny

![gradient-un-verano-sin-ti](example_images/gradients/gd5.png "Un verano sin ti")

* `rosalia2` [Motomami](https://open.spotify.com/intl-es/album/6jbtHi5R0jMXoliU2OS0lo) - Rosalía

![gradient-motomami](example_images/gradients/gd6.png "Motomami")

`alvaro_diaz` [Felicilandia](https://open.spotify.com/intl-es/album/7jg09IJJXi1eigVLZja2hN) - Álvaro Díaz

![gradient-felicilandia](example_images/gradients/gd1.png "Felicilandia")

`kanye` [The life of pablo](https://open.spotify.com/intl-es/album/7gsWAHLeT0w7es6FofOXk1) - Kanye West

![gradient-life-of-pablo](example_images/gradients/gd2.png "Life of Pablo")

`kendrick3` [Mr. Morale & the Big Steppers](https://open.spotify.com/intl-es/album/79ONNoS4M9tfIA1mYLBYVX) - Kendrick Lamar

![gradient-mr-morale](example_images/gradients/gd3.png "Mr. Morale")

`radiohead` [Kid A](https://en.wikipedia.org/wiki/Kid_A) - Radiohead

## Plot examples

TBD by MJ

## License

`album-colours` was created by Majo Castañeda, Dante Bazaldua. It is licensed under the terms of the MIT license.