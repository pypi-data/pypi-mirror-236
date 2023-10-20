import asyncio
import numpy as np
import pandas as pd
import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from mlserver.codecs import PandasCodec, NumpyCodec, StringCodec
from pydantic import BaseModel
from typing import Any, List, Optional, Union

from mlserver.types.dataplane import InferenceRequest, RequestInput

from cortex_cli import __version__

class InferenceResponse(BaseModel):
    outputs: List[Any]


def decode(inference: InferenceRequest):
    content_type = inference.parameters.content_type
    if content_type == 'pd':
        return PandasCodec.decode_request(inference)
    elif content_type == 'np':
        return NumpyCodec.decode(inference)
    elif content_type == 'str':
        return StringCodec.decode(RequestInput(**inference.inputs[0]))
    else:
        raise ValueError(f"Unsupported content type: {content_type}")


def encode(output: Union[pd.DataFrame, np.ndarray, str]):
    input_type = type(output)
    if input_type == pd.DataFrame:
        return PandasCodec.encode_outputs(output)
    elif input_type == np.ndarray:
        return NumpyCodec.encode_output('output-0', output)
    elif input_type == str:
        return StringCodec.encode(output)
    else:
        raise ValueError(f"Unsupported content type: {InferenceRequest.parameters.content_type}")


class MLServerFastAPI:
    model_instance = None


    def __init__(self, model_instance):
        self.version = __version__

        self.app = FastAPI(
            title="MLServerFastAPI",
            description='A FastAPI wrapper for MLServer architecture - supporting Nearly Human Cortex models.',
        )
        self.serving_task: Optional[asyncio.Task] = None

        self.model_instance = model_instance

    async def serve(self):
        app: FastAPI = self.app

        @app.post("/infer")
        async def infer(inputs: InferenceRequest) -> Union[InferenceResponse, JSONResponse]:
            infer_input = decode(inputs)
            try:
                infer_output = self.model_instance.predict(infer_input)
            except Exception as e:
                return JSONResponse(status_code=500, content={"error": str(e)})
            
            return InferenceResponse(outputs=encode(infer_output))

        # serve
        config = uvicorn.Config(app, host="127.0.0.1", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
