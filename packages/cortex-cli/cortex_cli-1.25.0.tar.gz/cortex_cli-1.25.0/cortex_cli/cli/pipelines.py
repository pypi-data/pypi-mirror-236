import asyncio
import plumbum.cli
import requests
import mlflow
import os
import traceback

from pydoc import locate

from cortex_cli.cli.cli_api_base import CliApiBase
from cortex_cli.core.deployment.mlserver_fastapi import MLServerFastAPI
from cortex_cli.core.mlflow.mlflow_cortex import get_input_example, load_model


class PipelinesCli(plumbum.cli.Application):
    NAME = 'pipelines'


class PipelinesBase(CliApiBase):
    def main(self, *args):
        args_list = self._check_args_not_empty(args)
        action    = args_list[0]
        tracking  = args_list[1]
        self._id  = path = args_list[2]
        self._error_message = None

        try:
            if tracking:
                response = self._get_pipeline()
                response = self._deploy_cortex(action, response['modelId'])
            else:
                self._deploy_local(action, path)
        except:
            if not self._error_message:
                self._error_message = traceback.format_exc()
        finally:
            if self._error_message:
                raise Exception(self._error_message)
            else:
                self._pass(f'Completed Cortex Pipeline {action.title()}ment')


    def _get_pipeline(self) -> dict:
        return self._handle_api_response(requests.get(
            url     = f'{self._endpoint}/{self._id}',
            headers = self._headers
        ))


@PipelinesCli.subcommand('deploy')
class PipelinesDeploy(PipelinesBase):
    _tracking = plumbum.cli.Flag(
        names=['-t', '--tracking'],
        default=True
    )

    _path = plumbum.cli.SwitchAttr(
        names     = ['-p','--path'], 
        argtype   = str
    )

    _id = plumbum.cli.SwitchAttr(
        names     = ['-i','--id'],
        argtype   = str
    )


    def main(self, *args):
        if self._id and self._path:
            self._fail('Cannot specify both --id and --path')

        # Handle Cortex training
        if self._id:
            return super().main('deploy', self._tracking, self._id)
        
        # Handle local training
        model = load_model(self._path)
        fastapi = MLServerFastAPI(model)
        asyncio.run(fastapi.serve())
        #return super().main('deploy', self._tracking, self._path)

@PipelinesCli.subcommand('undeploy')
class PipelinesUndeploy(PipelinesBase):
    _tracking = plumbum.cli.Flag(
        names=['-t', '--tracking']
    )

    _path = plumbum.cli.SwitchAttr(
        names     = ['-p','--path'], 
        argtype   = str,
        mandatory = True
    )

    _id = plumbum.cli.SwitchAttr(
        names     = ['-i','--id']
    )


    def main(self, *args):
        if self._id and self._path:
            self._fail('Cannot specify both --id and --path')

        if self._id:
            return super().main('undeploy', self._tracking, self._id)

        self._fail('Cannot specify --path or --tracking when undeploying')
