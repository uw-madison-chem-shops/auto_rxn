# recipes

CSV file.
Here's a simple example including some discrete hardware.

| Control Point ID    | mymotor | myfurnace | discrete | discrete.fallback_position |
| ------------------- | ------- | --------- | -------- | -------------------------- |
| RECIPE_STARTS_BELOW |         |           |          |                            |
| 0.1                 | 10      | 100       | red      | blue                       |
| 0.1                 | 20      | 200       | yellow   | blue                       |
| 0.2                 | 30      | 300       | orange   | red                        |
| 0                   | 10      | 100       | green    | red                        |

