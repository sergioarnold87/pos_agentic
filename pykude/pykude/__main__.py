import sys


def cli():
    try:
        import click
    except ImportError:
        print("CLI requires click. Install with: pip install pykude[cli]")
        sys.exit(1)

    _build_cli(click)


def _get_kude_class(name):
    """Get KuDE class and config by command name."""
    mapping = {
        "kude-fe": ("pykude.kude_fe", "KudeFe"),
        "kude-nce": ("pykude.kude_nce", "KudeNce"),
        "kude-nde": ("pykude.kude_nde", "KudeNde"),
        "kude-afe": ("pykude.kude_afe", "KudeAfe"),
        "kude-nre": ("pykude.kude_nre", "KudeNre"),
        "kude-cre": ("pykude.kude_cre", "KudeCre"),
    }
    mod_path, class_name = mapping[name]
    import importlib

    mod = importlib.import_module(mod_path)
    return getattr(mod, class_name)


def _build_cli(click):
    from pykude.kude_fe.config import KudeFeConfig

    @click.group()
    @click.version_option()
    def app():
        """ParaguayFiscalReport - Generate KuDE PDFs from SIFEN XML."""
        pass

    for cmd_name in ["kude-fe", "kude-nce", "kude-nde", "kude-afe", "kude-nre", "kude-cre"]:

        def make_cmd(name):
            @app.command(name=name)
            @click.argument("xml_file", type=click.Path(exists=True))
            @click.option("-o", "--output", default=None, help="Output PDF file path")
            @click.option("--logo", default=None, help="Path to logo image")
            @click.option(
                "--format",
                "paper_format",
                type=click.Choice(["carta", "ticket"]),
                default="carta",
                help="Paper format",
            )
            @click.option("--test", is_flag=True, help="Test environment (watermark)")
            def cmd(xml_file, output, logo, paper_format, test, _name=name):
                """Generate KuDE PDF from XML file."""
                with open(xml_file, "r", encoding="utf-8") as f:
                    xml = f.read()

                if paper_format == "ticket":
                    from pykude.kude_ticket import (
                        KudeTicket,
                        KudeTicketConfig,
                    )

                    config = KudeTicketConfig(logo=logo, ambiente=2 if test else 1)
                    kude = KudeTicket(xml=xml, config=config)
                else:
                    klass = _get_kude_class(_name)
                    config = KudeFeConfig(logo=logo, ambiente=2 if test else 1)
                    kude = klass(xml=xml, config=config)

                if output is None:
                    base = xml_file.rsplit(".", 1)[0]
                    output = f"{base}_kude.pdf"

                kude.output(output)
                click.echo(f"Generated: {output}")

            return cmd

        make_cmd(cmd_name)

    @app.command()
    @click.argument("xml_file", type=click.Path(exists=True))
    @click.option("-o", "--output", default=None, help="Output PDF file path")
    @click.option("--logo", default=None, help="Path to logo image")
    @click.option("--test", is_flag=True, help="Test environment (watermark)")
    def auto(xml_file, output, logo, test):
        """Auto-detect document type and generate KuDE."""
        from pykude import auto_kude

        with open(xml_file, "r", encoding="utf-8") as f:
            xml = f.read()

        config = KudeFeConfig(logo=logo, ambiente=2 if test else 1)
        kude = auto_kude(xml=xml, config=config)

        if output is None:
            base = xml_file.rsplit(".", 1)[0]
            output = f"{base}_kude.pdf"

        kude.output(output)
        click.echo(f"Generated: {output}")

    app()


if __name__ == "__main__":
    cli()
