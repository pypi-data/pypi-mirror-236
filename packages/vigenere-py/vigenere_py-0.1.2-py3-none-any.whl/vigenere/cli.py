import sys
from typing import Optional, TextIO

import click

from .cipher import Cipher, generate_key_alphabet_label

# make help available at -h as well as default --help
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


ALIASES = {
    "d": "dec",
    "decrypt": "dec",
    "e": "enc",
    "encrypt": "enc",
    "genkey": "keygen",
}


class AliasedGroup(click.Group):
    # @typing.override  # python 3.12+
    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        if cmd_name in ALIASES:
            cmd_name = ALIASES[cmd_name]
        return super().get_command(ctx, cmd_name)


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option(package_name="vigenere-py")
def cli() -> None:
    """Vigenère cipher encryption for Python"""


@cli.command(name="enc")
@click.argument("input", type=click.File("r"), required=False)
@click.option("-o", "--output", help="Output file", type=click.File("w"))
@click.option("-k", "--key-file", help="Key file", type=click.File("r"))
@click.option("-b", "--batch", help="Non-interactive mode", is_flag=True, default=False)
def encrypt(
    input: Optional[TextIO],
    key_file: Optional[TextIO],
    output: Optional[TextIO],
    batch: bool,
) -> None:
    """
    Encrypt text with a Vigenère cipher.

    Read plaintext from INPUT file or from stdin if not provided.

    For example:

        vigenere enc -o out.txt input.txt

    """

    if not input:
        input = sys.stdin

    # If output is a TTY, highlight spaces in ANSI inverted colors
    if output:
        ansi_invert_spaces = False
    else:
        ansi_invert_spaces = sys.stdout.isatty()

    c = Cipher(key_file=key_file, batch=batch)

    if input.isatty():
        click.echo("Text to encrypt:", err=True)

    ciphertext = c.encrypt(input.read())

    if output:
        output.write(ciphertext)
    else:
        if input.isatty():
            click.echo("Ciphertext:", err=True)

        if ansi_invert_spaces:
            ciphertext = ciphertext.replace(" ", "\033[7m \033[27m")

        click.echo(ciphertext, nl=False)


@cli.command(name="dec")
@click.argument("input", type=click.File("r"), required=False)
@click.option("-o", "--output", help="Output file", type=click.File("w"))
@click.option("-k", "--key-file", help="Key file", type=click.File("r"))
@click.option("-b", "--batch", help="Non-interactive mode", is_flag=True, default=False)
def decrypt(
    input: Optional[TextIO],
    key_file: Optional[TextIO],
    output: Optional[TextIO],
    batch: bool,
) -> None:
    """Decrypt Vigenère ciphertext"""

    if not input:
        input = sys.stdin

    c = Cipher(key_file=key_file, batch=batch)

    if input.isatty():
        click.echo("Enter ciphertext...", err=True)

    plaintext = c.decrypt(input.read())

    if output:
        output.write(plaintext)
    else:
        if input.isatty():
            click.echo("Plaintext:", err=True)
        click.echo(plaintext, nl=False)


@cli.command()
@click.argument("length", type=int)
@click.option("-o", "--output", help="Write key to given file", type=click.File("w"))
def keygen(
    length: int,
    output: Optional[TextIO],
) -> None:
    """
    Generate a random key, suitable for use as a one time pad.
    """

    key = generate_key_alphabet_label(length=length, alphabet_name="printable")
    if output:
        output.write(key)
    else:
        ansi_invert_spaces = sys.stdout.isatty()
        if ansi_invert_spaces:
            key = key.replace(" ", "\033[7m \033[27m")

        click.echo(key)
