__author__ = "Thomas Silvers"
__copyright__ = "Copyright 2024, Thomas Silvers"
__email__ = "silvers@mpiib-berlin.mpg.de"
__license__ = "MIT"

import os
from snakemake.shell import shell

revision = snakemake.params.get("revision")
profile = snakemake.params.get("profile", [])
config = snakemake.params.get("config")
resume = snakemake.params.get("resume", True) # TODO: Reasonable default? Conforms nxf to smk...
process_cache = snakemake.params.get("process_cache", 'lenient') # TODO: Reasonable default? Conforms nxf to smk...
nxf = snakemake.params.get("nxf", "") # For -log, -w, etc.
extra = snakemake.params.get("extra", "")
if isinstance(profile, str):
    profile = [profile]
if isinstance(config, str):
    config = [config]

args = []

if revision:
    args += ["-revision", revision]
if profile:
    args += ["-profile", ",".join(profile)]
if config:
    args += ["-config", ",".join(config)]
if resume:
    args += ["-resume"]
if process_cache:
    args += [f"-process.cache={process_cache}"]
print(args)

add_parameter = lambda name, value: args.append("--{} {}".format(name, value))

for name, files in snakemake.input.items():
    if isinstance(files, list):
        files = ",".join(files)
    add_parameter(name, files)
for name, value in snakemake.params.items():
    if (
        name != "pipeline"
        and name != "revision"
        and name != "profile"
        and name != "config"
        and name != "resume"
        and name != "process_cache"
        and name != "nxf"
        and name != "extra"
    ):
        add_parameter(name, value)

log = snakemake.log_fmt_shell(stdout=False, stderr=True)
args = " ".join(args)
pipeline = snakemake.params.pipeline

shell("nextflow run nf-core/{pipeline} {nxf} {args} {extra} {log}")
