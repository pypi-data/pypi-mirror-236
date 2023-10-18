"""
Low-level update commands.
"""
import logging

import click
import yaml

from opthub_client_cli.util import AliasedGroup, DateTimeTz, StrLength, execute

_logger = logging.getLogger(__name__)

Q_UPDATE = """
mutation(
  $pk_columns: {0}_pk_columns_input!
  $set: {0}_set_input
) {{
  update_{0}_by_pk(
    pk_columns: $pk_columns
    _set: $set
  ) {{
    id
    updated_at
  }}
}}
"""


def mutation(table, ctx, kwargs):
    """Build a GQL mutation document.

    :param table: Table name on OptHub
    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    return execute(
      ctx,
      Q_UPDATE.format(table),
      {
        "pk_columns": {"id": kwargs.pop("id_to_update")},
        "set": {k: v for k, v in kwargs.items() if v is not None},
      },
    )


@click.group(cls=AliasedGroup, help="Update an object.")
def update():
    """Update an object."""


@update.command(help="Update a problem.")
@click.argument("id-to-update", type=StrLength(min=2))
@click.option("-i", "--id", type=StrLength(min=2), help="New ID.")
@click.option("-t", "--image", type=StrLength(min=1), help="New Docker image tag.")
@click.option("--public/--private", default=None, help="New visibility.")
@click.option(
    "-e", "--description_en", type=StrLength(min=1), help="New description in English."
)
@click.option(
    "-j", "--description_ja", type=StrLength(min=1), help="New description in Japanese."
)
@click.pass_context
def problem(ctx, **kwargs):
    """Update a problem.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug("update.problem(%s)", kwargs)
    mutation("problems", ctx, kwargs)


@update.command(help="Update an indicator.")
@click.argument("id-to-update", type=StrLength(min=2))
@click.option("-i", "--id", type=StrLength(min=2), help="New ID.")
@click.option("-t", "--image", type=StrLength(min=1), help="New Docker image tag.")
@click.option(
    "-e", "--description_en", type=StrLength(min=1), help="New description in English."
)
@click.option(
    "-j", "--description_ja", type=StrLength(min=1), help="New description in Japanese."
)
@click.option("--public/--private", default=None, help="New visibility.")
@click.pass_context
def indicator(ctx, **kwargs):
    """Update an indicator.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug("update.indicator(%s)", kwargs)
    mutation("indicators", ctx, kwargs)


@update.command(help="Update an environment.")
@click.argument("id-to-update", type=click.IntRange(min=1))
@click.option("-m", "--match", "match_id", type=click.IntRange(min=1), help="New match ID.")
@click.option("-k", "--key", type=StrLength(min=1), help="New key.")
@click.option("-v", "--value", type=yaml.safe_load, help="New value.")
@click.option("--public/--private", default=None, help="New visibility.")
@click.pass_context
def environment(ctx, **kwargs):
    """Update an environment.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug("update.environment(%s)", kwargs)
    mutation("environments", ctx, kwargs)


@update.command(help="Update a match.")
@click.argument("id-to-update", type=click.IntRange(min=1))
@click.option("-n", "--name", type=StrLength(min=2), help="New name.")
@click.option("-c", "--competition", "competition_id", type=StrLength(min=2), help="New competition ID.")
@click.option("-p", "--problem", "problem_id", type=StrLength(min=2), help="New problem ID.")
@click.option("-i", "--indicator", "indicator_id", type=StrLength(min=2), help="New indicator ID.")
@click.option("-b", "--budget", type=click.IntRange(min=1), help="New budget.")
@click.option("--public/--private", default=None, help="New visibility.")
@click.pass_context
def match(ctx, **kwargs):
    """Update a match.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug("update.match(%s)", kwargs)
    mutation("matches", ctx, kwargs)


@update.command(help="Update a competition.")
@click.argument("id-to-update", type=StrLength(min=2))
@click.option("-i", "--id", type=StrLength(min=2), help="New ID.")
@click.option("-o", "--open-at", type=DateTimeTz(), help="New open date.")
@click.option("-c", "--close-at", type=DateTimeTz(), help="New close date.")
@click.option(
    "-e", "--description_en", type=StrLength(min=1), help="New description in English."
)
@click.option(
    "-j", "--description_ja", type=StrLength(min=1), help="New description in Japanese."
)
@click.option("--public/--private", default=None, help="New visibility.")
@click.pass_context
def competition(ctx, **kwargs):
    """Update a competition.

    :param ctx: Click context
    :param kwargs: GraphQL variables
    """
    _logger.debug("update.competition(%s)", kwargs)
    mutation("competitions", ctx, kwargs)
