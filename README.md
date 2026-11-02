# wifi-channel-analyzer

Pick the least congested Wi-Fi channel per band from a scan CSV: channels with fewer, weaker neighbouring networks score better.

## How to run

```sh
python3 main.py scan.csv
```

## Example output

```
2.4GHz: use channel 2 (0 network(s) there, congestion score 0)
5GHz: use channel 44 (0 network(s) there, congestion score 0)
```

Standard library only. Run the tests with `python3 -m unittest discover`.
