import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s", "--secret_store",
    help="source where secrets are retrieved from",
    type=str,
    choices=[
        "json",
        "env"
    ],
    default="env"
)

parser.add_argument(
    "-f", "--secret_file",
    help="file which secrets will be loaded from when a file-based secret store is used",
    type=str,
    default=None
)

args = parser.parse_args()

if args.secret_store in ["json"] and args.secret_file == None:
    parser.error(f"Secret store '{args.secret_store}' requires argument --secret_file")
    
print(args)