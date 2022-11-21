import io
import uuid
import contextlib
import traceback
import typing

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse


router_ui = APIRouter(tags=["ui"])


@router_ui.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return request.state.templates.TemplateResponse("base.html", {
        "request": request
    })


@router_ui.get("/kernels/cell", response_class=HTMLResponse)
async def get_cell(request: Request):
    return request.state.fragments.TemplateResponse("cell.html", {
        "request": request,
        "cell_uuid": uuid.uuid4().hex
    })


import ast

def my_exec(script, globals=None, locals=None):
    '''Execute a script and return the value of the last expression'''
    stmts = list(ast.iter_child_nodes(ast.parse(script)))
    if not stmts:
        return None
    if isinstance(stmts[-1], ast.Expr):
        # the last one is an expression and we will try to return the results
        # so we first execute the previous statements
        if len(stmts) > 1:
            exec(compile(ast.Module(body=stmts[:-1], type_ignores=[]), filename="<ast>", mode="exec"), globals, locals)
        # then we eval the last one
        return eval(compile(ast.Expression(body=stmts[-1].value), filename="<ast>", mode="eval"), globals, locals)
    else:
        # otherwise we just execute the entire code
        return exec(script, globals, locals)


@router_ui.post("/kernels/cell", response_class=HTMLResponse)
async def post_cell(request: Request, cell: typing.Optional[str] = Form(None)):
    try:
        stderr = io.StringIO()
        stdout = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(contextlib.redirect_stderr(stderr))
            stack.enter_context(contextlib.redirect_stdout(stdout))
            result = my_exec(cell)
        stdout = stdout.getvalue()
        stderr = stderr.getvalue()
    except Exception as e:
        stdout = stdout.getvalue()
        stderr = stderr.getvalue()
        result = traceback.format_exc()

    return request.state.fragments.TemplateResponse(
        "cell_output.html", {
            "request": request,
            "stdout": stdout,
            "stderr": stderr,
            "result": result,
        })


@router_ui.delete("/kernels/cell", response_class=HTMLResponse)
async def post_cell(request: Request):
    return ""
