# Standards adoption

- Reviewed standards SHA: `26946e9075503633c16fb1b0f7380d0101ed7b45`
- Standard: https://github.com/eigger/hass-repo-standards/tree/26946e9075503633c16fb1b0f7380d0101ed7b45
- Profile: integration / ha; repository eigger/hass-melk-light; default branch master; domain melk_light.
- Scope and implementation plan: [docs/adoption-plan.md](docs/adoption-plan.md).
- Evidence and completion status: [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md). No approved exceptions.
- Minimum HA remains 2025.11.0. Current tests use HA 2026.10.2 independently of support policy.
- blesession>=0.9.0 uses public session APIs and keeps the 30-second idle reuse policy. Both current and exact floor modes run in each HA environment. Minimum HA constrains pycares<5 because its aiodns 3.x requires result types removed in pycares 5; this does not raise support minimum.
- Product category: lighting, based on the physical RGB MELK light bar and its lighting controls. Category evidence is in .hass-standards.json; no category is inferred merely from platform names.
- Domain, config-entry data/schema, device identifiers and entity unique IDs remain unchanged. No data migration is needed. Failed writes now surface as service errors; successful writes still represent assumed state without hardware acknowledgement.
- HACS remains Custom. PR #4 was reviewed and squash merged at 3dabcba755a5d3c41d29a8fb14d6f1b9603777e1. Downloads counts all release assets. ZIP deployment starts with the next separately requested release; no release/tag was created for this adoption.
- Reviewed release standards SHA: `fd4162c0b93fbe8e109f99c787773ae09ba157e1`
- Release action retains reviewed release standards SHA fd4162c0b93fbe8e109f99c787773ae09ba157e1 from PR #4; it is scoped independently of the full adoption SHA.
- No imagespec, payload examples, polling coordinator, authentication, options flow or custom services exist; these conditional requirements are N/A.
