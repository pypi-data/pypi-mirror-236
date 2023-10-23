from __future__ import annotations

import json
import re
import pandas as pd
from functools import cached_property
from nandai.api import NandAIClient
from nandai.constants import DEFAULT_BATCH_SIZE
from nandai.constants import DEFAULT_DF_COLUMNS
import itables as it


class NandValidator:

    @cached_property
    def client(self):
        return NandAIClient()

    @cached_property
    def itables(self):
        it.options.css = """
        .nand-source { text-decoration: line-through; background-color: #ffeef0; color: #24292e; }
        .nand-correction { font-style: oblique; background-color: #e6ffed; color: #24292e; }
        """

        it.init_notebook_mode(all_interactive=False)
        return it

    async def validate(
            self,
            df: pd.DataFrame,
            columns: list[str] = DEFAULT_DF_COLUMNS,
            context: str | list[str] = [],
            batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> pd.DataFrame:
        """Validate prompt-response pairs with context."""
        df.columns = df.columns.str.strip()
        return await self.client.batch_validate(df, context=context, batch_size=batch_size, columns=columns)

    def display(self, df: pd.DataFrame, **kwargs):
        """Display validation result."""
        if df.empty:
            return

        for col in ['response', 'Correction']:
            if col not in df.columns:
                raise ValueError(f"`{col}` column not found in dataframe")

        def highlight(row: pd.Series):
            res: str = row['response']
            corr = json.loads(row['Correction'])
            match_regex = re.compile('(' + "|".join(re.escape(m) for m in corr) + ')')
            parts = re.split(match_regex, res)
            row['response'] = ''.join([
                f'<i class="nand-source">{p}</i><i class="nand-correction">{corr[p]}</i>'
                if p in corr else p for p in parts
            ])
            return row

        df = df.apply(highlight, axis=1)
        kwargs = {'classes': 'display', **kwargs}
        self.itables.show(df, **kwargs)
