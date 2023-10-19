import click
import json
from . import fcm

cli = click.Group()


@cli.command()
@click.option("--t", required=True, help="Enter push token.")
@click.option("--c", type=click.Path(exists=True), default='credentials.json',
              required=False, help="Enter credentials path.")
@click.option("--n", type=click.Path(exists=True), default='notification.json',
              required=False, help="Enter credentials path.")
def send(t, c, n):
    fcm.setup(c)
    data = {
        "push-message": json.dumps(json.load(open(n)))
    }
    fcm.send_message(t, data)
    click.secho("Completed!", fg='green')
