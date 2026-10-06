# Cahuil Simulation

This repository contains the files to perform the Cahuil simulation. 
There are two code options available depending on the implementation strategy: 
* separate split where there are not intersection bewteen both domains
* split with a delta where are a zone common because a sponge zone is nedded using the linear embedding.

## Folder Structure

```
cahuil-simulation/
├── split-exact/
└── split-delta/
```

## Folder Description

inspect.py create config.json and bathy.txt, is already in folders. waves.txt for sea domain is a jonswap energy spectrum
