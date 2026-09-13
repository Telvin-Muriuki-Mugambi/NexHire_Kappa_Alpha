"""Start the NexHire command-line application."""

from CLI_commands.Auth_CLI import run_cli


def main(argv=None):
    """Run the authentication CLI with the supplied command-line arguments."""
    return run_cli(argv)

if __name__ == "__main__":
    raise SystemExit(main())