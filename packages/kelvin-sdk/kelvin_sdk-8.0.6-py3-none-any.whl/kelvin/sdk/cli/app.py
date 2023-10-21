"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""
from __future__ import annotations

import asyncio
import os
from typing import Dict, List, Optional

import click
from click import Choice
from colorama import Fore

from kelvin.sdk.lib.configs.general_configs import GeneralConfigs, KSDKHelpMessages
from kelvin.sdk.lib.models.apps.common import ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour, ProjectType
from kelvin.sdk.lib.utils.click_utils import AppNameWithVersionType, KSDKCommand, KSDKGroup
from kelvin.sdk.lib.utils.logger_utils import logger


@click.group(cls=KSDKGroup)
def app() -> None:
    """
    Create, build and manage applications.

    """


@app.command(cls=KSDKCommand)
def samples() -> None:
    """
    Opens Kelvin's code samples GitHub repo.

    """
    import webbrowser

    logger.info(
        f"""Kelvin code samples are available here:
        {Fore.GREEN}{GeneralConfigs.code_samples_url}{Fore.RESET}
    """
    )
    webbrowser.open_new_tab(GeneralConfigs.code_samples_url)


@app.command(cls=KSDKCommand)
@click.argument("app_name", nargs=1, type=click.STRING, required=False)
@click.option("--description", required=False, default="", type=click.STRING, help=KSDKHelpMessages.app_description)
@click.option(
    "--app-type",
    required=False,
    default=ProjectType.kelvin.value,
    type=Choice(ProjectType.app_types_as_str()),
    help=KSDKHelpMessages.app_type,
)
@click.option(
    "--app-dir",
    type=click.Path(),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
def create(
    app_name: str,
    description: str,
    app_type: Optional[ProjectType],
    app_dir: str,
) -> bool:
    """
    Create a new application based on the specified parameters.

    """
    from kelvin.sdk.interface import app_create_from_parameters

    app_type = ProjectType(app_type)
    kelvin_app_lang = ApplicationLanguage.python

    if not app_name:
        app_name = input("Please provide a name for the application: ")

    return app_create_from_parameters(
        app_dir=app_dir or ".",
        app_name=app_name,
        app_description=description,
        app_type=app_type,
        app_flavour=ApplicationFlavour.default,
        kelvin_app_lang=kelvin_app_lang,
    ).success


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option("--fresh", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.fresh)
@click.option("--build-arg", type=str, multiple=True, help="docker build-args", default=[])
def build(app_dir: str, fresh: bool, build_arg: List[str]) -> bool:
    """
    Build a local application into a packaged image.

    """
    from kelvin.sdk.interface import app_build

    build_args_dict: Dict[str, str] = dict(x.split("=") for x in build_arg)  # type: ignore

    return app_build(app_dir=app_dir, fresh_build=fresh, build_args=build_args_dict).success


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option("--fresh", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.fresh)
def deploy(app_dir: str, fresh: bool) -> bool:
    """
    Deploy a registry application to the Kelvin Cloud (based on a local app.yaml).

    """
    from kelvin.sdk.interface import app_deploy

    return app_deploy(app_dir, fresh).success


def split_assets(_, __, value: str) -> List[str]:  # type: ignore
    if value is None:
        return []

    return value.split(",")


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    help=KSDKHelpMessages.app_dir,
)
@click.option("--name", type=click.STRING, required=False, help=KSDKHelpMessages.app_name)
@click.option("--version", type=click.STRING, required=False, help=KSDKHelpMessages.app_version)
@click.option(
    "--assets", type=click.STRING, required=False, help=KSDKHelpMessages.app_assets_array, callback=split_assets
)
def undeploy(app_dir: str, name: str, version: str, assets: List[str]) -> bool:
    """
    Undeploy an application.
    Undeploy info can be either extracted from an existing app.yaml file or passed by paramaters.
    """
    from kelvin.sdk.interface import app_undeploy

    return app_undeploy(app_dir, name, version, assets).success


@app.command(cls=KSDKCommand)
@click.option(
    "--app-dir",
    type=click.Path(exists=True),
    required=False,
    default=".",
    help=KSDKHelpMessages.app_dir,
)
@click.option(
    "--upload-datatypes",
    default=False,
    is_flag=True,
    show_default=True,
    help=KSDKHelpMessages.appregistry_upload_datatypes_upload,
)
def upload(app_dir: str, upload_datatypes: bool = False) -> bool:
    """
    Upload an application to the platform's Application Registry.

    e.g. kelvin appregistry upload --app-dir="."
    """
    from kelvin.sdk.interface import appregistry_upload

    return appregistry_upload(app_dir=app_dir, upload_datatypes=upload_datatypes).success


@app.group(cls=KSDKGroup)
def images() -> None:
    """
    Management and display of local images on the Local Application Registry.

    """


@images.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all locally built applications.

    """
    from kelvin.sdk.interface import app_images_list

    return app_images_list(should_display=True).success


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True))
def remove(app_name_with_version: str) -> bool:
    """
    Remove an application from the local applications list.\n

    e.g. kelvin app images remove "test-app:1.0.0"

    """
    from kelvin.sdk.interface import app_image_remove

    return app_image_remove(app_name_with_version=app_name_with_version).success


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True))
@click.option(
    "--container-dir",
    type=click.Path(),
    required=False,
    default=None,
    help=KSDKHelpMessages.app_images_unpack_container_dir,
)
@click.option(
    "--output-dir",
    type=click.Path(),
    required=True,
    help=KSDKHelpMessages.app_images_unpack_output_dir,
)
def unpack(app_name_with_version: str, container_dir: str, output_dir: str) -> bool:
    """
    Extract the content of an application from its built image into the specified directory.\n

    e.g. kelvin app images unpack "test-app:1.0.0" --output-dir=my_output_dir

    """
    from kelvin.sdk.interface import app_image_unpack

    return app_image_unpack(
        app_name_with_version=app_name_with_version, container_dir=container_dir, output_dir=output_dir
    ).success


@images.command(cls=KSDKCommand)
@click.argument("app_name_with_version", nargs=1, type=AppNameWithVersionType(version_required=True))
@click.argument("output_dir", nargs=1, type=click.Path())
def config(app_name_with_version: str, output_dir: str) -> bool:
    """
    Extract the app configuration file (app.yaml) from a built image into a specific directory.\n

    e.g. kelvin app images config "test-app:1.0.0" my_output_dir/

    """
    from kelvin.sdk.interface import app_image_config

    return app_image_config(app_name_with_version=app_name_with_version, output_dir=output_dir).success


@app.group(cls=KSDKGroup)
def test() -> None:
    """
    Test local applications.
    """


async def start_publisher(
    config: str,
    period: float,
    min: float,
    max: float,
    rand: bool,
    asset_count: int,
    asset_parameter: List[str],
) -> None:
    from kelvin.app.stream import KelvinStreamConfig
    from kelvin.publisher import Publisher, PublisherServer

    port = KelvinStreamConfig().port
    if not os.path.exists(config):
        logger.error(
            "Unable to locate the application configuration file (default 'app.yaml'). Please make sure you are in the application directory or specify the path using the --config option."
        )
        return

    publisher = Publisher(
        app_yaml=config,
        rand_min=min,
        rand_max=max,
        random=rand,
        asset_count=asset_count,
        parameters_override=asset_parameter,
    )
    pubserver = PublisherServer(period, publisher)
    server = await asyncio.start_server(pubserver.new_client, "127.0.0.1", port)

    logger.relevant("Publisher started. You can now test your application.")

    async with server:
        await server.serve_forever()


@test.command(cls=KSDKCommand)
@click.option(
    "--config",
    required=True,
    default="app.yaml",
    type=click.STRING,
    show_default=True,
    help="Path to the app config file",
)
@click.option(
    "--period", required=True, default=5.0, type=click.FLOAT, show_default=True, help="Publish period in seconds"
)
@click.option("--min", default=0.0, type=click.FLOAT, show_default=True, help="Minimum value to publish")
@click.option("--max", default=100.0, type=click.FLOAT, show_default=True, help="Maximum value to publish")
@click.option(
    "--random/--counter", "rand", default=True, show_default=True, help="Publish random values or incremental"
)
@click.option(
    "--asset-count",
    default=1,
    type=click.INT,
    show_default=True,
    help="Number of test assets from 'test-asset-1' to 'test-asset-N'",
)
@click.option(
    "--asset-parameter",
    type=click.STRING,
    help="Override asset parameters eg --asset-parameters kelvin_closed_loop=true  (Can be set multiple times)",
    multiple=True,
)
def simulator(
    config: str,
    period: float,
    min: float,
    max: float,
    rand: bool,
    asset_count: int,
    asset_parameter: List[str],
) -> None:
    """
    Starts a simulator server where Kelvin applications can connect to.
    The server publishes data to all app inputs and log received messages.
    """
    asyncio.run(start_publisher(config, period, min, max, rand, asset_count, asset_parameter))
