import dataclasses
import json
import pathlib
from typing import Optional

import click
from loguru import logger
from tabulate import tabulate
from tqdm import tqdm

import gevulot
from gevulot import model
from gevulot.metadata import repository


@click.group(name="wormhole", invoke_without_command=False)
def gevulot_cli():
    pass


@gevulot_cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.PurePosixPath)
)
@click.option(
    "--capacity",
    required=False,
    type=int,
    default=None,
    help="Defines a maximum number of commits a stream can hold",
)
def touch(path: pathlib.PurePosixPath, capacity: Optional[int] = None):
    """ 
    Creates a stream at PATH. Capacity defines a maximum number of commits a stream can hold.
    When capacity is exceeded, datums older commits point to will be removed.
    """

    logger.debug(f"touch(path={path}, capacity={capacity})")

    graph = gevulot.Gevulot.new_instance()

    stream = graph.touch(path, capacity)

    logger.debug(f"Created stream at {path}:\n{stream.model_dump_json(indent=2)}")


@gevulot_cli.command()
@click.argument(
    "prefix",
    type=click.Path(path_type=pathlib.PurePosixPath),
    required=False,
    default=pathlib.PurePosixPath("/")
)
def ls(prefix: pathlib.PurePosixPath):
    """
    List all streams that match given path prefix.
    """

    logger.debug(f"ls(path={prefix})")

    graph = gevulot.Gevulot.new_instance()

    streams = graph.find(prefix)

    for stream in streams:
        click.echo(stream.path)


@gevulot_cli.command()
@click.argument(
    "src",
    type=click.Path(path_type=pathlib.PurePosixPath)
)
@click.argument(
    "dest",
    type=click.Path(path_type=pathlib.PurePosixPath)
)
@click.option(
    "--buffer-size",
    type=int,
    required=False,
    default=10 * 1024 * 1024,
    help="Copy buffer size",
)
def cp(src: pathlib.PurePosixPath, dest: pathlib.PurePosixPath, buffer_size: int):
    """
    Put a datum defined by src to dest. src and dest can point to either local
    file system or to gevulot (protocols gevulot:// and file:// respectively).
    If no file system is specified, gevulot is assumed by default.
    """

    logger.debug(f"cp(src={src}, dest={dest}, buffer_size={buffer_size})")

    graph = gevulot.Gevulot.new_instance()

    with \
        graph.start(), \
        graph.open(src, "rb") as src_io, \
        graph.open(dest, "wb") as dest_io \
    :
        progress_bar = tqdm(
            desc=f"Copying from {src} to {dest}",
            total=len(src_io),
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        )

        with progress_bar:
            while buffer := src_io.read(buffer_size):
                dest_io.write(buffer)
                progress_bar.update(n=len(buffer))

                from time import sleep
                sleep(1e-2)


@gevulot_cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.PurePosixPath)
)
def log(path: pathlib.PurePosixPath):
    """
    Similar to git's log. Prints a history of stream's commits.
    """

    logger.debug(f"log(path={path})")

    graph = gevulot.Gevulot.new_instance()

    commits = graph.log(path)

    [stream, *_] = graph.find(path)

    header = ["Full path", "Created at", "Type"]
    rows = []
    for commit in commits:
        full_path = pathlib.PurePosixPath(f"gevulot:{stream.path}") / f"#{commit.id}"

        datum = graph.resolve(full_path)

        if isinstance(datum, gevulot.Blob):
            blob: gevulot.Blob = datum
            extra_value = _format_bytes(blob.size)
            extra_header = "Size"
        elif isinstance(datum, gevulot.Run):
            run: gevulot.Run = datum
            extra_value = run.status.name
            extra_header = "Status"

        rows.append([
            full_path,
            commit.created_at.strftime('%m/%d/%Y, %H:%M:%S'),
            datum.unit_name,
            extra_value,
        ])

    header.append(extra_header)

    click.echo(tabulate(rows, headers=header))


def _format_bytes(bytes_num) -> str:
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""

    bytes_num = float(bytes_num)
    kb = float(1024)
    mb = float(kb**2)  # 1,048,576
    gb = float(kb**3)  # 1,073,741,824
    tb = float(kb**4)  # 1,099,511,627,776

    if bytes_num < kb:
        return "{0}{1}".format(bytes_num, "Bytes" if 0 == bytes_num > 1 else "Byte")
    elif kb <= bytes_num < mb:
        return "{0:.2f}KB".format(bytes_num / kb)
    elif mb <= bytes_num < gb:
        return "{0:.2f}MB".format(bytes_num / mb)
    elif gb <= bytes_num < tb:
        return "{0:.2f}GB".format(bytes_num / gb)
    elif tb <= bytes_num:
        return "{0:.2f}TB".format(bytes_num / tb)


@gevulot_cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.PurePosixPath)
)
def stat(path: pathlib.PurePosixPath):
    """
    Prints general information about a datum referenced by a path.
    If path has no information about commit to be used within a given stream,
    HEAD commit is used by default.
    """

    logger.debug(f"stat(path={path})")

    graph = gevulot.Gevulot.new_instance()

    datum = graph.resolve(path)

    datum_params = datum.model_dump()

    if isinstance(datum, gevulot.Blob):
        blob: gevulot.Blob = datum
        
        datum_params["id"] = str(blob.id)
        datum_params["size"] = _format_bytes(blob.size)
    elif isinstance(datum, gevulot.Run):
        run: gevulot.Run = datum

        datum_params["id"] = str(run.id)
        datum_params["status"] = run.status.name

    click.echo(json.dumps(datum_params, indent=2))


@gevulot_cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.PurePosixPath)
)
def trace(path: pathlib.PurePosixPath):
    """
    Prints upstream and downstream usage information of a datum referenced by path.
    Message objects are used to figure out relationships between different datum objects.
    """

    logger.debug(f"ls(path={path})")

    graph = gevulot.Gevulot.new_instance()

    datum = graph.resolve(path)
    click.secho(f"DATUM: {datum.unit_name}", bold=True)
    click.echo(datum.model_dump_json(indent=2))

    click.echo("".join(["="] * 80))

    upstream_datums = graph.upstream(path)    
    if any(upstream_datums):
        header = ["Full path", "Type"]
        rows = []
        for upstream_datum in upstream_datums:
            full_path = graph.which(upstream_datum)

            if isinstance(upstream_datum, gevulot.Blob):
                blob: gevulot.Blob = upstream_datum
                extra_value = _format_bytes(blob.size)
                extra_header = "Size"
            elif isinstance(upstream_datum, gevulot.Run):
                run: gevulot.Run = upstream_datum
                extra_value = run.status.name
                extra_header = "Status"

            rows.append([
                full_path,
                datum.unit_name,
                extra_value,
            ])
        
        header.append(extra_header)

        click.secho("UPSTREAM:", bold=True)
        click.echo(tabulate(rows, headers=header))
    else:
        click.secho("UPSTREAM: None", bold=True)

    click.echo("".join(["="] * 80))

    downstream_datums = graph.downstream(path)
    if any(downstream_datums):
        header = ["Full path", "Type"]
        rows = []
        for downstream_datum in downstream_datums:
            full_path = graph.which(downstream_datum)

            if isinstance(downstream_datum, gevulot.Blob):
                blob: gevulot.Blob = downstream_datum
                extra_value = _format_bytes(blob.size)
                extra_header = "Size"
            elif isinstance(downstream_datum, gevulot.Run):
                run: gevulot.Run = downstream_datum
                extra_value = run.status.name
                extra_header = "Status"

            rows.append([
                full_path,
                datum.unit_name,
                extra_value,
            ])
        
        header.append(extra_header)

        click.secho("DOWNSTREAM:", bold=True)
        click.echo(tabulate(rows, headers=header))
    else:
        click.secho("DOWNSTREAM: None", bold=True)


@gevulot_cli.command()
def clean(path: Optional[pathlib.PurePosixPath] = None):
    """
    Remove all data and metadata from the current storage
    """

    graph = gevulot.Gevulot.new_instance()

    graph.clean()

    logger.debug(f"Metadata and data backends have been nullified")


@gevulot_cli.command()
@click.argument(
    "path",
    type=click.Path(path_type=pathlib.PurePosixPath),
    required=False,
    default=None,
)
def run(path: Optional[pathlib.PurePosixPath] = None):
    graph = gevulot.Gevulot.new_instance()

    with graph.start(path):
        with graph.open("/some/path.parquet", "rb") as blob_io:
            pass

        with graph.open("/some/path.parquet", "wb") as blob_io:
            pass
    
    with graph.start("/danger/zone"):
        raise ValueError("Something went wrong")


@gevulot_cli.command()
def test():
    run = model.Run.new_instance(
        status=model.RunStatus.Running,
        error="",
    )

    print(f"Original datum type: {type(run)}")
    print(json.dumps(dataclasses.asdict(run), indent=2, default=lambda v: str(v)))

    metadata = model.Metadata.from_unit(run)

    print(f"Original metadata type: {type(metadata)}")
    print(json.dumps(dataclasses.asdict(metadata), indent=2, default=lambda v: str(v)))

    repo = repository.InProcMetadataRepository.new_instance()

    repo.set(run)

    run_recovered = repo.get(run.id)

    print(f"Recovered datum type: {type(run_recovered)}")
    print(json.dumps(dataclasses.asdict(run_recovered), indent=2, default=lambda v: str(v)))

    repo.delete(run)
    logger.debug(f"Run {run.id} was removed")

    obj_after_removal = repo.get(run.id)

    print(f"Obj after removal: {obj_after_removal}")

    from gevulot.metadata import config
    cfg = config.MetadataConfig.new_instance()

    print(cfg)


@gevulot_cli.command()
def clear():
    repo = repository.MetadataRepository.new_instance()

    repo.clean()


# @gevulot_cli.command()
# def test_minio():
#     logger.info("stat")

#     # s3_client = boto3.resource(
#     #     "s3",
#     #     endpoint_url="https://localhost:9000",
#     #     aws_access_key_id="94Don906btI9rikCagN4",
#     #     aws_secret_access_key="CIXrKjWSxBI916uAtf1iANonf2CcQYcWW0J2nwhe",
#     #     aws_session_token=None,
#     #     config=boto3.session.Config(signature_version="s3v4"),
#     #     verify=False,
#     # )
#     #
#     # for bucket in s3_client.buckets.all():
#     #     print(bucket.name)

#     # http_client = urllib3.PoolManager(
#     #     # cert_reqs="CERT_REQUIRED",
#     #     # ca_certs="/home/sn/projects/wormhole/wormhole/blackbox/secrets/tls/certs/ca-chain.cert.pem",
#     # )
#     minio_client = minio.Minio(
#         "localhost:9000",
#         access_key="94Don906btI9rikCagN4",
#         secret_key="CIXrKjWSxBI916uAtf1iANonf2CcQYcWW0J2nwhe",
#         secure=False,
#         # http_client=http_client,
#     )

#     for bucket in minio_client.list_buckets():
#         print(bucket.name)

# @gevulot_cli.command()
# def test_dynamodb():
#     # 1 - Create Client
#     ddb = boto3.resource('dynamodb',
#                          endpoint_url='http://localhost:8000',
#                          region_name='dummy',
#                          aws_access_key_id='dummy',
#                          aws_secret_access_key='dummy')
#     # 2 - Create the Table
#     ddb.create_table(TableName='Transactions',
#                      AttributeDefinitions=[
#                          {
#                              'AttributeName': 'TransactionId',
#                              'AttributeType': 'S'
#                          }
#                      ],
#                      KeySchema=[
#                          {
#                              'AttributeName': 'TransactionId',
#                              'KeyType': 'HASH'
#                          }
#                      ],
#                      ProvisionedThroughput= {
#                          'ReadCapacityUnits': 10,
#                          'WriteCapacityUnits': 10
#                      }
#                      )
#     print('Successfully created Table')

#     table = ddb.Table('Transactions')

#     input = {'TransactionId': '9a0', 'State': 'PENDING', 'Amount': 50}

#     #3 - Insert Data
#     table.put_item(Item=input)
#     print('Successfully put item')

#     #4 - Scan Table
#     scanResponse = table.scan(TableName='Transactions')
#     items = scanResponse['Items']
#     for item in items:
#         print(item)

if __name__ == "__main__":
    gevulot_cli()
