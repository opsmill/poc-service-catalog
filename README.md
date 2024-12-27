# Blog post 2024

## TODO

- [ ] Handle service status in generator

## spin

```bash
infrahubctl schema load schemas/base
infrahubctl schema load schemas/location_minimal
infrahubctl schema load schemas/vlan
infrahubctl schema load schemas/service

infrahubctl run schemas/data.py
```

## Abstract

- Got base, circuit and location minimal from schema library
- Created a small script to get some data in
- Created a service schema
- **Clear service definition (catalog)**

## Questions

- Should we create an "implementation" kind of concept
