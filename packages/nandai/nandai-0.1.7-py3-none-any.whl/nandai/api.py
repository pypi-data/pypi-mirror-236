from __future__ import annotations
import json
import httpx
import pandas as pd
import os

from nandai.constants import DEFAULT_BATCH_SIZE
from nandai.constants import DEFAULT_DF_COLUMNS
from nandai.utils import batch_async


transport = httpx.AsyncHTTPTransport(retries=2)
http_client = httpx.AsyncClient(transport=transport, timeout=120)


class NandAIClient:
    def __init__(
            self,
            url: str | None = None,
            api_key: str | None = None,
    ):
        self.url = url or os.getenv('NANDAI_API_URL') or 'https://llmeval.nand.ai/api'
        self.api_key = api_key or os.getenv('NANDAI_API_KEY') or ''

        if not self.url:
            raise ValueError('NANDAI_API_URL is not set as an environment variable or passed as an argument')

        if not self.api_key:
            raise ValueError('NANDAI_API_KEY is not set as an environment variable or passed as an argument')

    async def batch_validate(
            self,
            input: pd.DataFrame,
            columns: list[str] = DEFAULT_DF_COLUMNS,
            context: str | list[str] = [],
            batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> pd.DataFrame:
        data = self._process_data(input, columns)
        context = self._process_additional_context(context)

        async def func(row: pd.Series):
            res = await self.validate(
                prompts=[row['prompt']],
                responses=[row['response']],
                context=context if 'context' not in row else row['context'] + '\n\n' + context,
               )
            row['NandScore'] = res[0]['NandScore']
            row['FactualInaccuraciesFound'] = res[0]['FactualInaccuraciesFound']
            row['Correction'] = res[0]['Correction']
            return row

        rows = [row for _, row in data.iterrows()]
        return pd.DataFrame(await batch_async(rows, func, batch_size)).sort_values(by='NandScore')

    def _process_data(self, data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Prepare data for validation. Context column is optional."""
        ctx_col = 'context' if len(columns) == 2 else columns[2]
        columns = columns[:2]
        if ctx_col in data.columns:
            columns += [ctx_col]
        return data[columns].rename(columns=dict(zip(columns, ['prompt', 'response', 'context'])))

    def _process_additional_context(self, context: str | list[str]) -> str:
        if isinstance(context, str):
            context = [context]
        return '\n\n'.join(context)

    async def validate(self, prompts: list[str], responses: list[str], context: str):
        res = await http_client.post(
            url= f'{self.url}/llmeval',
            json={
                'prompt': prompts,
                'response': responses,
                'context': context,
                'excludes': [],
            },
            headers={
                'x-api-key': self.api_key,
            },
        )
        res = res.json()
        return [
            {
                'NandScore': r['nandscore'],
                'FactualInaccuraciesFound': not r['factuality'],
                'Correction': json.dumps(r['correction'])
            } for r in res
        ]
