from subprocess import call
from sys import argv
from os import getenv, getuid

(_, generator, generator_tag, openapi_file, openapi_url, output_folder, config_file, template_dir, *args) = argv

cmd = f"docker run -u {getuid()} --rm --workdir /github/workspace -v {getenv('GITHUB_WORKSPACE')}:/github/workspace"
cmd = f"{cmd} openapitools/openapi-generator-cli:{generator_tag} generate"
cmd = f"{cmd} -g {generator} -o /github/workspace/{output_folder}"

if openapi_url == "UNSET":
    if not openapi_file.startswith("/"):
        openapi_file = f"/github/workspace/{openapi_file}"
    cmd = f"{cmd} -i {openapi_file}"
else:
    cmd = f"{cmd} -i {openapi_url}"

if config_file != "UNSET":
    if not config_file.startswith("/"):
        config_file = f"/github/workspace/{config_file}"
    cmd = f"{cmd} -c {config_file}"

if template_dir != "UNSET":
    if not template_dir.startswith("/"):
        template_dir = f"/github/workspace/{template_dir}"
    cmd = f"{cmd} -t {template_dir}"

if args:
    cmd = f"{cmd} {' '.join(args)}"

# Call the command and return the exit code
exit(call(cmd, shell=True))
