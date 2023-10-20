import ast
import contextlib
import json
import sys
from functools import lru_cache
from io import StringIO
from typing import Optional

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...dataset.manager import Manager


class Query(BaseModel):
    code: str
    start: Optional[int] = None
    end: Optional[int] = None
    byImage: bool = False
    cached: bool = False


@contextlib.contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def build_queries_router(params, manager: Manager, meta_serving: bool = False):
    queries_router = r = APIRouter(tags=["Dataset: Dataframe queries"])

    df = manager.anno_df.copy()

    if manager.task in ["classification", "multilabel_classification"]:
        df["type"] = "image"

    elif manager.task in ["detection", "box_classification", "box_multilabel_classification"]:
        df["type"] = "box"

    elif manager.task == "instance_segmentation":
        df["type"] = "mask"

    elif manager.task == "keypoints_detection":
        df["type"] = "keypoints"

    gdict = {"pd": pd, "ast": ast}
    ldict = {"df": df}

    meta_df = None
    if meta_serving:
        meta_df = manager.meta_df.copy()
        meta_df.rename(columns={"file_name": "image_hash"}, inplace=True)
        ldict["meta_df"] = meta_df

    @lru_cache(maxsize=5)
    def run_query(code: str):
        with capture() as out:
            try:
                exec(code, gdict, ldict)
            except Exception as e:
                raise HTTPException(status_code=409, detail=str(e))

            res = ldict.get("res")

            if res is None:
                raise HTTPException(status_code=409, detail="res variable is not found in query code")

            if isinstance(res, pd.Series):
                res = res.to_frame("data")

            if isinstance(res, pd.DataFrame):
                if res.index.names[0] is not None:
                    res = res.reset_index()

                return {"log": out[0].getvalue(), "res": res}

            raise HTTPException(status_code=409, detail="res variable is not DataFrame or Series")

    @r.post("/queries", summary="Query the annotation dataframe")
    async def query_r(query: Query):
        if query.cached:
            res = run_query(query.code)
        else:
            res = run_query.__wrapped__(query.code)

        res_df = res["res"]
        if query.byImage and "image_hash" in res_df.columns:
            hashes = res_df["image_hash"].unique()
            start = query.start or 0
            end = query.end or len(hashes)
            size = len(hashes)
            res_slice = res_df[res_df["image_hash"].isin(hashes[start:end])]
        else:
            start = query.start or 0
            end = query.end or len(res_df)
            size = len(res_df)
            res_slice = res_df[start:end]

        return {
            "log": res["log"],
            "result": {
                "header": res_slice.columns.values.tolist(),
                "data": json.loads(res_slice.to_json(orient="values")),
                "size": size,
            },
        }

    return queries_router, df, meta_df
